

import requests
import json


class ApplyQuery():
    def __init__(self, url):
        self.url = url
        self.product_id = None

    def get_url(self):
        return self.url
    
    def query_post(self, id, flag='c', product_id=None):
        self.product_id = product_id
        if flag == 'c' and self.product_id:
            payload = {
                'product_id':str(self.product_id),
                'count':'-1'
            }
            r = requests.post(self.url+'/'+str(id)+'/data', payload)
            datas = json.loads(r.text)
            return self.parse_data(datas=datas, keys=['key', 'cart_id'])

    def query_get(self, id, flag='p'):
        if flag == 'p':
            r = requests.get(self.url+'/'+str(id)+'/data')
            datas = json.loads(r.text)[0]
            return self.parse_data(datas=datas, keys=['product_mfd', 'product_epd'])
        elif flag == 'c':
            r = requests.get(self.url+'/'+str(id)+'/data')
            datas = json.loads(r.text)[1]
            return self.parse_data(datas=datas, keys=['key', 'cart_id'])
        elif flag == 'com':
            r = requests.get(self.url+'/'+str(id)+'/data')
            datas = json.loads(r.text)[1]
            return self.parse_data(datas=datas, keys=['key', 'cart_id'])['completed']

    def completed(self, id):
        payload = {
            'completed': True
        }
        r = requests.post(self.url+'/'+str(id)+'/completed', payload)
        print(json.loads(r.text))
    
    def parse_data(self, datas, keys=None):
        data_dict = dict()
        for data in datas:
            for key, value in data.items():
                if keys!= None and key in keys:
                    continue
                if key in data_dict.keys():
                    data_dict[key].append(str(value))
                else:
                    data_dict[key] = list([str(value)])
        return data_dict
#self.query.query_get(id=1,flag='com')