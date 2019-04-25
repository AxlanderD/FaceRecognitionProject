#coding=utf-8

import  configparser
import  demjson
#处理数据和数据转换的模块
#读取配置文件
def get_conf(key,value):
    cf = configparser.ConfigParser()
    cf.read('config.ini',encoding='utf-8')
    return cf.get(key,value)

#将向量转换为字符串
def embed_to_str(vector):
    new_vector = [str(x) for x in vector]
    return ','.join(new_vector)

#将字符串转换为向量
def str_to_embed(str):
    str_list = str.split(',')
    return [float(x) for x in str_list]


def fmt_data(arrData):
    str= demjson.encode(arrData)
    str_len=len(str)
    str_len="%04d"%str_len
    return str_len+str

def trans_string(retData):
    fp=open('json_tmp.txt','w')
    print >> fp, retData
    fp.close()
    return get_json_data()

def get_json_data(path):
    f = open(path)
    line = f.readline()
    f.close()
    str_len = len(line)-1
    str_len = "%04d" % str_len
    return str_len + line
