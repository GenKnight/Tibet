#coding:utf-8


# def singleton(cls):
#     instance = cls()
#     instance.__call__ = lambda : instance
#     return instance


def singleton(cls):
    instances = {}

    def _singleton( *args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

class Singleton(object):
    @classmethod
    def instance(cls,*args,**kwargs):
        if not hasattr(cls,'handle'):
            cls.handle = cls(*args,**kwargs)
        return cls.handle

class ObjectCreateHelper(object):
    def __init__(self,func,*args,**kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def create(self):
        return self.func(*self.args,**self.kwargs)

class Instance(object):
    def __init__(self):
        self.handle = None
        self.helper = None

    def set(self,handle):
        self.handle = handle

    def __getattr__(self, item):
        return getattr(self.handle, item)

        # if self.handle:
        #     return getattr(self.handle,item)
        # if  self.helper:
        #     v = self.helper.create()
        #     return v


    def get(self):
        return self.handle


def hash_object(obj,key_prefix='',excludes=()):
    attrs = [s for  s in dir(obj) if not s.startswith('__')  ]
    kvs={}
    for k in attrs:
        attr = getattr(obj, k)
        if not callable(attr):
            if k in excludes:
                continue
            if key_prefix:
                k = key_prefix + k
            kvs[k] = attr


    return kvs

def object_assign(obj,values,add_new=False):
    """将values的key对应的value赋给对象obj的属性"""
    attrs = [s for  s in dir(obj) if not s.startswith('__')  ]
    kvs={}
    for k,v in values.items():
        if not add_new:
            if k in attrs:
                setattr(obj,k,v)
        else:
            setattr(obj,k,v)

def get_config_item(root,path,default=None):
    """根据配置路径 x.y.z ,获取配置项"""
    ss = path.split('.')
    conf = root
    try:
        for s in ss:
            conf = conf.get(s)
            if not conf:
                break
    except:
        conf = default
    return conf

def list_item_match(list_,name,value):
    """return first item which matched"""
    matched = filter(lambda x:x.get(name)==value,list_)
    if matched:
        return matched[0]
    return None


class ObjectBuilder(object):
    @staticmethod
    def create(data):
        """
        从 dict 数据生成 object 对象
        :param data:dict
        :return:
        """
        class _Object:pass
        if not isinstance(data,dict):
            return data
        newobj = _Object()
        for k,v in data.items():
            setattr( newobj,str(k),v)
        return newobj