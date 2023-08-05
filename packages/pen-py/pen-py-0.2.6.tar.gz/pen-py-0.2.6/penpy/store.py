import datetime
import os

from google.cloud import datastore, redis

from .dicplus import DicPlus


class Store():
    def __init__(self, kind, lookup=None, default_entity=None, credentials=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), project=os.getenv('GOOGLE_CLOUD_PROJECT')):
        if not credentials:
            raise Exception(
                "No Google credentials provided or set up in env GOOGLE_APPLICATION_CREDENTIALS")
        else:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
        if not project:
            raise Exception(
                "No Google project provided or set up in env GOOGLE_CLOUD_PROJECT")
        else:
            os.environ['GOOGLE_CLOUD_PROJECT'] = project
        self.ds_client = datastore.Client(project=project)
        self.kind = kind
        if default_entity != None:
            self.entity = default_entity
        elif lookup is None:
            newkey = self.ds_client.key(kind)
            self.entity = datastore.Entity(key=newkey)
            self.update({"created": datetime.datetime.utcnow()})
        else:
            lookup_k = lookup.split(':')[0]
            lookup_v = lookup.split(':')[1]
            if lookup_k == "id":
                mykey = self.ds_client.key(kind, int(lookup_v))
                self.entity = self.ds_client.get(mykey)
            else:
                query = self.ds_client.query(kind=kind)
                query.add_filter(lookup_k, "=", lookup_v)
                found = list(query.fetch())
                if len(found) > 0:
                    self.entity = list(query.fetch())[0]
                else:
                    self.entity = None
            if self.entity is None:
                self.entity = datastore.Entity(key=self.ds_client.key(kind))
                self.update(
                    {lookup_k: lookup_v, "created": datetime.datetime.utcnow()})

    def update(self, dic):
        self.entity.update(dic)
        self.save()

    @property
    def key_id(self):
        return self.entity.key.id

    def empty(self):
        return (not 'created' in dict(self.entity))

    def __str__(self):
        return str(dict(self.entity))

    def save(self):
        self.ds_client.put(self.entity)

    def delete(self):
        self.ds_client.delete(self.entity.key)

    @property
    def data(self):
        return self.toDM(json_datetime=True)

    def toDP(self, json_datetime=False):
        return self.ds_to_dp(self.entity, json_datetime=json_datetime)

    def toDM(self, json_datetime=False):
        return self.ds_to_dp(self.entity, json_datetime=json_datetime)

    def ds_to_dp(self, entity, is_list=False, json_datetime=False):  # to re-format
        dp = DicPlus()
        if is_list:
            new_list = []
            for el in entity:
                new_list.append(self.ds_to_dp(el, json_datetime=json_datetime))
            return new_list
        for k, v in dict(entity).items():
            if type(v) == datastore.entity.Entity:
                dp[k] = self.ds_to_dp(v, json_datetime=json_datetime)
            elif type(v) == list:
                dp[k] = self.ds_to_dp(
                    v, is_list=True, json_datetime=json_datetime)
            elif type(v) == datetime.datetime:
                if json_datetime:
                    dp[k] = v.strftime("%Y-%m-%dT%H:%M:%S")
                else:
                    dp[k] = v.replace(tzinfo=None)
            else:
                dp[k] = v
        return dp

    @classmethod
    def findAll(cls, kind, filters):
        ''' Use this template:
        Store.findAll('message', [['test', 'test2']])
        '''
        try:
            ds_client = datastore.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
            query = ds_client.query(kind=kind)
            for f in filters:
                if len(f) == 2:
                    query.add_filter(f[0], "=", f[1])
                else:
                    query.add_filter(f[0], f[1], f[2])
            results = list(query.fetch())
            results_objs = []
            for obj in results:
                results_objs.append(cls(kind, default_entity=obj))
            return results_objs
        except Exception as e:
            return None

    @classmethod
    def findOne(cls, kind, filters):
        ''' Use this template:
        Store.findAll('message', [['test', 'test2']])
        '''
        list_found = cls.findAll(kind, filters)
        if list_found == None:
            return None
        elif len(list_found) > 0:
            return list_found[0]
        else:
            return None
