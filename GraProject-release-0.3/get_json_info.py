#coding=utf-8

'''
通过id作为唯一主键查询该id所属的Name
'''
import face_comm
import json
import demjson
import os
import sys
json_path = face_comm.get_conf('json','json_path')
def get_person_name(id):
    if type(id) is not 'string':
        id = str(id)
    with open(json_path,'r',encoding='UTF-8') as f:
        lines = f.read()
        lines = json.loads(lines)
    for i in lines:
        if i['id'] == id:
            return i['name']
    return False
def write_person_name(id,name):
    if type(id) is not 'string':
        id = str(id)
    with open(json_path,'r',encoding='UTF-8') as f:
        lines = f.read()
        lines = json.loads(lines)
        for i in  lines:
            if i['id'] == id:
                print('have existed')
                return False
        write_info = [{'id':id,'name':name}]
        new_content = lines+ write_info     
    with open(json_path,'w',encoding='UTF-8') as f:
        write_info_json = json.dumps(new_content)
        if f.write(write_info_json):
            print('write suc')
            return True
        else:
            print('failed')
            return False
           


if __name__ =='__main__':
    id = 2
    write_person_name(id,'网上男子')
    
    retData = get_person_name(id)
    if retData:
        print('Name:',retData)
    else:
        print('No Data')
    