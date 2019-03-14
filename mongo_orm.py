from pymongo import MongoClient

Client = MongoClient()
db = Client.proxy


class Model(object):

    @classmethod
    def find(cls, **kwargs):
        d_list = []
        cls_name = cls.__name__
        result = db[cls_name].find(dict(kwargs))
        for o in result:
            o.pop('_id')
            d_list.append(o)
        return d_list

    def save(self):
        cls_name = self.__class__.__name__
        db[cls_name].insert_one(self.__dict__)

    def __repr__(self):
        cls_name = self.__class__.__name__
        info = self.__dict__
        return cls_name + '<' + str(info) + '>'

    def update(self, **kwargs):
        cls_name = self.__class__.__name__
        d = dict(kwargs)
        k, v = d.items()
        attr, value = k[0], v[0]
        v = getattr(self, attr)
        print(v)
        db[cls_name].update_one(
            {attr: v},
            {'$set': {attr: value}}
        )

    def to_json(self):
        j = self.__dict__.copy()
        return j

    @classmethod
    def all(cls):
        return cls.find()
