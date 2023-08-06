import types
import hashlib

from pymysql import connections
from collections import OrderedDict

def jump_hash(key, num_buckets):
	b, j = -1, 0
	key = int(hashlib.md5(key.encode()).hexdigest(), 16)
	while j < num_buckets:
		b = int(j)
		key = ((key * int(2862933555777941757)) + 1) & 0xFFFFFFFFFFFFFFFF
		j = float(b + 1) * (float(1 << 31) / float((key >> 33) + 1))
	return int(b)

class MultiIterator:
	q = None

	def __init__(self):
		self.q = []

	def add(self, _iter):
		self.q.append(_iter)

	def __iter__(self):
		return self

	def __next__(self):
		while(self.q):
			try:
				return next(self.q[-1])
			except StopIteration as ex:
				self.q.pop()
		raise StopIteration

class Attribute(object):
	_type = None

	def __init__(self, _type, **kwargs):
		self._type = _type
		self.__dict__.update(kwargs)

class Model(object):
	#class level
	_attrs = None
	_pk_attrs = None

	#instance level
	__is_new = True
	_pending_updates = {}

	_inserted_id = None
	_init = False

	_json = None

	def get_custom_dict(self, path, dict_obj):

		_init = True

		class DictObj(dict):
			def __setitem__(this, k, v):
				if(not _init):
					new_path = path + "." + k
					self._pending_updates[new_path] = v
					if(isinstance(v, dict)):
						v = self.get_custom_dict(new_path, v)
				super(DictObj, this).__setitem__(k, v)

		ret = DictObj(**dict_obj)
		_init = False
		return ret

	def __setattr__(self, k, v):
		if(k in self.__class__._attrs):
			_attr_type_obj = self.__class__._attrs[k]
			if(_attr_type_obj._type == dict and isinstance(v, dict)):
				v = self.get_custom_dict(k, v)

			if(not self._init):
				self._pending_updates[k] = v
		self.__dict__[k] = v

	def to_json(self):
		self._json = _json = self._json or {}
		for k in self.__class__._attrs:
			if(k in self.__dict__):
				_json[k] = getattr(self, k , None)
		return _json

	def pk(self):
		ret = {}
		for k in self.__class__._pk_attrs.keys():
			ret[k] = getattr(self, k)
		return ret

	@classmethod
	def get_instance_from_document(cls, doc):
		ret = cls()
		ret.__is_new = False
		ret._init = True
		for k, v in cls._attrs.items():
			ret.__dict__[k] = None # set all initial attributes to None
		for k, v in doc.items():
			setattr(ret, k, v)
		ret._init = False
		return ret

	@classmethod
	def create_doc(cls, **values):
		ret = cls()
		ret._pending_updates.update(cls.get_default_values())
		for k, v in cls._attrs.items():
			ret.__dict__[k] = None # set all initial attributes to None
		for k, v in values.items(): # set the given values
			setattr(ret, k, v)
		return ret

	@classmethod
	def get_default_values(cls):
		ret = {}
		for k, v in cls._attrs.items():
			default = getattr(v, "default", None)
			if(default):
				if(isinstance(default, types.FunctionType)):
					default = default()
				ret[k] = default
		return ret

	@classmethod
	def get_shard_key_from_query(cls, _query):
		_shard_keys = cls._shard_keys_
		if(not _shard_keys):
			return ""
		ret = []
		for k in cls._shard_keys_:
			ret.append(_query[k]) # must exist
		return "__".join(ret)

	def get_shard_key(self):
		_shard_keys = self.__class__._shard_keys_
		if(not _shard_keys):
			return ""
		ret = []
		for k in _shard_keys:
			ret.append(getattr(self, k))
		return "__".join(ret)

	@classmethod
	def update(cls, _query, update_values):
		return get_shard(cls, cls.get_shard_key_from_query(_query)).update(_query, update_values) # , hint=cls._pk_attrs)

	@classmethod
	def query(cls, _query, sort=None, projection=None):
		ret = get_shard(cls, cls.get_shard_key_from_query(_query)).find(_query, projection)
		if(sort):
			ret = ret.sort(sort)
		return map(cls.get_instance_from_document, ret)

	@classmethod
	def query_multiple_shards(cls, _query, shard_keys_array, sort=None, projection=None):
		collections_map = {}
		for _shard_keys in shard_keys_array:
			_collection = None
			if(isinstance(_shard_keys, str)): # assuming single primary key
				_collection = get_shard(cls, _shard_keys)
			else:
				_collection = get_shard(cls, "__".join(_shard_keys))
			collections_map[id(_collection)] = _collection

		multi_iterator = MultiIterator()
		for _temp, _collection in collections_map.items():
			ret = _collection.find(_query, projection)
			if(sort):
				ret = ret.sort(sort)
			multi_iterator.add(ret)

		return map(cls.get_instance_from_document, multi_iterator)

	def commit(self, force=False):
		committed = False
		if(self.__is_new): # try inserting
			self.__is_new = False
			try:
				self._inserted_id = get_shard(self.__class__, self.get_shard_key()).insert_one(self._pending_updates)
				committed = True
			except DuplicateKeyError as ex:
				if(not force):
					raise(ex) # re reaise

				# try remove the primary key from pending updates
				if("_id" in self._pending_updates):
					del self._pending_updates["_id"]

				for k in list(self._pending_updates.keys()):
					if(k in self.__class__._pk_attrs):
						del self._pending_updates[k]

		if(not self.__is_new and not committed and self._pending_updates):  # try updated
			get_shard(self.__class__, self.get_shard_key()).update(self.pk(), {"$set": self._pending_updates}) # , hint=self.__class__._pk_attrs)

		self._pending_updates.clear()
		return self

	def delete(self):
		get_shard(self.__class__, self.get_shard_key()).delete_one(self.pk())


class Connection:

	collections = {}
	pool = None

	def __init__(self, host="localhost", port=3606, db_name=None, user_name=None, password=None):
		self.pool = Queue()

		self.host = host
		self.port = port
		self.db_name = db_name
		self.user_name = user_name
		self.password = password

		for cls in Model.__subclasses__():
			self.inititalize(cls)

	def get_connection(self, conn):
		ret = self.pool.get(block=False)
		cur_time = time.time()
		if(not ret):
			conn = connections.Connection(host=self.host, port=self.port, user=self.user,
											 password=self.password, database=self.db_name
										)
			last_used_timestamp = cur_time

		if(last_used_timestamp < cur_time - 10) # unused for 10 sec
			conn.ping(reconnect=True)

		return conn

	def release_connection(self, conn):
		self.pool.put( (time.time(), conn) )


	def get_shard(self, Model): # cache and get collection? needed?
		ret = self.collections.get(Model)
		if(not ret):
			self.collections[Model] = ret = self.db[Model._collection_name_]
		return ret

	'''	Add all necessary class level attributes to the model, 
		should be done before you do anything with the table '''
	def inititalize(self, Model):
		if(isinstance(Model, list)):
			for _m in Model:
				self.inititalize(_m)
			return

		Model._attrs = _model_attrs = {}
		Model._pk_attrs = None

		attrs_to_name = {}
		for k, v in Model.__dict__.items():
			if(isinstance(v, Attribute)):
				_model_attrs[k] = v
				attrs_to_name[v] = k
				attrs_to_name[k] = k # dumb , but it's one time thing and also helps converting if any given attributes as strings

		# ensure indexes created and all collections loaded to memory
		_model_indexes = getattr(Model, "_index_", [])
		Model._shard_keys_ = getattr(Model, "_shard_keys_", ())
		Model._cluster_ = getattr(Model, "_cluster_", "default")

		_pymysql_indexes_to_create = []
		for _index in _model_indexes:
			pymysql_index = []
			if(not isinstance(_index, tuple)):
				_index = (_index,)
			for _a in _index:
				_attr_name = _a
				_ordering = 1 # ascending
				if(isinstance(_a, tuple)):
					_a, _ordering = _a
				if(isinstance(_a, Attribute)):
					_attr_name = attrs_to_name[_a]

				pymysql_index.append((_attr_name, _ordering))


			if(not Model._pk_attrs): # create _pk_attrs from the first index
				Model._pk_attrs = _pk_attrs = OrderedDict()
				for i in pymysql_index: # first unique index
					_pk_attrs[i[0]] = 1

			_pymysql_indexes_to_create.append(pymysql_index)

		# set collection name to include shard_keys
		if(Model._shard_keys_):
			Model._table_name_ = Model._table_name_ + "_shard_" + ("__".join(map(lambda x: attrs_to_name[x], Model._shard_keys_)))
		# create indices in mysql

		#Left here , create table and create indexes if not exists on all shards
		for pymysql_index in _pymysql_indexes_to_create:
			self.get_shard(Model).create_index(pymysql_index, unique=True)

		if(not Model._pk_attrs): # create default _pk_attrs
			Model._pk_attrs = OrderedDict(_id=True)


_mongo_clusters = {}
def init_mongo_cluster(nodes, cluster="default"):
	if(not isinstance(nodes, list)):
		nodes = [nodes]
	db_nodes = []
	for node in nodes:
		if(isinstance(node, dict)):
			node = Connection(**node)
		db_nodes.append(node)
	_mongo_clusters[cluster] = db_nodes

def get_shard(Model, shard_key):
	cluster_nodes = _mongo_clusters[Model._cluster_]
	_node_with_data = jump_hash(shard_key, len(cluster_nodes))
	return cluster_nodes[_node_with_data].get_shard(Model)



# - Supports client-side sharding,
# - Doesn't autoshardi, you have to redistribute data if you add more db's later.

# - You can Configure mongo as a sharded cluster. Just pass the configuration server to 
# - init_mongo_cluster({"host": "", "port": 27017, "db_name": "yourdb", "user_name": "", "password": ""})
