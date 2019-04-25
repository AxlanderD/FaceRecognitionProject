import  lmdb
import  os
import  face_comm

class face_lmdb:
    def __init__(self):
        self.db_file=os.path.abspath(face_comm.get_conf('lmdb','lmdb_path'))
    def add_embed_to_lmdb(self,id,vector):
        if type(id) is not 'string':
            id = str(id)
        evn = lmdb.open(self.db_file)
        wfp = evn.begin(write=True)
        wfp.put(key=id.encode(), value=face_comm.embed_to_str(vector).encode())
        wfp.commit()
        evn.close()

if __name__=='__main__':
    #插入数据
    embed = face_lmdb()