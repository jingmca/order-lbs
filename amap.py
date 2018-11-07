# encoding:utf-8
import json
import threading
import time

import requests

key = "7c14bb24c08b17f99078b7dada1364ea"


def addr2geo(addrs=[], batch_size=10):
    """
    addrs = [
        {'addr': string, 'city': string (optional)},
        ...]
    """
    result = []
    pages = (len(addrs) / batch_size)+1
    for page in xrange(pages):
        items = addrs[page*batch_size: (page+1)*batch_size]
        if len(items) > 1:
            query = '|'.join([i['addr'] for i in items])
            batch = 'true'
        else:
            query = items[0]['addr']
            batch = 'false'
        try:
            res = requests.get("https://restapi.amap.com/v3/geocode/geo?key=%s&address=%s&batch=%s" %
                               (key, query, batch))
            resp = res.json()
        except:
            print("amap geo failed , query:[%s]\n" % query)
        finally:
            if int(resp['status']) == 1:
                result.extend(resp['geocodes'])

    return result


def distance4geo(startpoints=(), endpoint=(), mode=0, sorted=False):
    """
    startpoints = ((lon, lat) ... ) geo pairs format with .6f
                   in mode 2, geo pairs must less than 20  [via public traffic]
                   in mode 0, geo pairs must less than 100 [just liner distance]
    endpioint = (lon, lat) only one endpoint
    mode = 0, liner distance
           2, public traffic eg bus / metro
    sorted = False (defalut) / True, shortest first if true
    """
    result = []
    batch_size = 20 if mode is 2 else 100
    batch = (len(startpoints) / batch_size) + 1
    endstr = "%s,%s" % endpoint
    for page in xrange(batch):
        items = startpoints[page*batch_size: (page+1)*batch_size]
        if len(items) > 1:
            query = '|'.join(["%s,%s" % i for i in items])
        else:
            query = "%s,%s" % items[0]
        try:
            res = requests.get(
                "http://restapi.amap.com/v3/distance?key=%s&origins=%s&destination=%s&type=%s" %
                (key, query, endstr, str(mode)))
            resp = res.json()
        except:
            print("amap distance failed , query:[%s]\n" % query)
        finally:
            if resp['info'] == 'OK':
                if mode != 0:
                    result.extend([ds['duration'] for ds in resp['results']])
                else:
                    result.extend([ds['distance'] for ds in resp['results']])
            else:
                print(resp['info'])

    result = list(enumerate(result))
    if sorted:
        result.sort(key=lambda x:int(x[1]))
    return result
        

aa = distance4geo(((116.481028,39.989643), (114.481028,39.989643), (115.481028,39.989643)), endpoint=(114.465302,40.004717), mode=1, sorted=True)
print(aa)