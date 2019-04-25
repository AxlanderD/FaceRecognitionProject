#coding=utf-8
import  face_comm
from annoy import AnnoyIndex
import  lmdb
import  os
import get_json_info
import face_lmdb

class face_annoy:

    def __init__(self):
        self.f                = int(face_comm.get_conf('annoy','face_vector'))
        self.annoy_index_path = os.path.abspath(face_comm.get_conf('annoy','index_path'))
        self.lmdb_file        =os.path.abspath(face_comm.get_conf('lmdb','lmdb_path'))
        self.num_trees        =int(face_comm.get_conf('annoy','num_trees'))
        self.annoy = AnnoyIndex(self.f)
        if os.path.isfile(self.annoy_index_path):
            self.annoy.load(self.annoy_index_path)
        self.vector_list = []
        for x in range(self.annoy.get_n_items()):
            self.vector_list.append(self.annoy.get_item_vector(x))
    #从lmdb文件中建立annoy索引
    def create_index_from_lmdb(self):
        # 遍历
        lmdb_file = self.lmdb_file
        if os.path.isdir(lmdb_file):
            evn = lmdb.open(lmdb_file)
            wfp = evn.begin()
            annoy = self.annoy
            for key, value in wfp.cursor():
                key = int(key.decode())
                value = face_comm.str_to_embed(value.decode())
                annoy.add_item(key,value)

            annoy.build(self.num_trees)
            annoy.save(self.annoy_index_path)

    #重新加载索引
    def reload(self):
        self.annoy.unload()
        self.annoy.load(self.annoy_index_path)

    #根据人脸特征找到相似的
    def query_vector(self,face_vector):
        n=int(face_comm.get_conf('annoy','num_nn_nearst'))
        search_k = int(face_comm.get_conf('annoy','search_k'))
        return self.annoy.get_nns_by_vector(face_vector,n,search_k=search_k,include_distances=True)

    def add_info_reload(self,id,name,vector):
        if get_json_info.write_person_name(id,name):
            facelmdb = face_lmdb.face_lmdb()
            facelmdb.add_embed_to_lmdb(id,vector)
        self.annoy.unload()
        self.create_index_from_lmdb()
        self.reload()
    def add_id_vector(self,pics,input_ids,input_names):
        import face_encoder
        import  face_alignment
        import face_detect
        import cv2
        encoder = face_encoder.Encoder()
        dir_path = 'D:/Program File/Jupyter-NoteBook/Graduation Project/GraProject-release-0.3/alignface/'
        for pic,input_id,input_name in zip(pics,input_ids,input_names):
            opic_array = cv2.imread(dir_path+pic)
            vector = encoder.generate_embedding(opic_array)
            self.add_info_reload(input_id,input_name,vector)
            self.annoy.unload()
            self.create_index_from_lmdb()
            self.reload()
            print(self.annoy.get_n_items())


if __name__=='__main__':
    annoy  = face_annoy()
    '''
    import face_encoder
    import  face_alignment
    import face_detect
    import cv2
    encoder = face_encoder.Encoder()
    dir_path = 'D:/Program File/Jupyter-NoteBook/Graduation Project/GraProject-release-0.3/alignface/'''
    pic_path = ['1556128499_94.png','1556129371_24.png','1556129379_64.png','1556129394_53.png','1556129399_95.png']
    make_id  = [10,11,12,13,14]
    names    = ['董伟健']*5
    annoy.add_id_vector(pic_path,make_id,names)

    ''' 
    for pic,get_id,name in pic_path,make_id,names:
        opic_array = cv2.imread(pic_path)
        vector = encoder.generate_embedding(opic_array)
        annoy.add_info_reload(get_id,name,vector)
        annoy.annoy.unload()
        annoy.create_index_from_lmdb()
        annoy.reload()
        print(annoy.annoy.get_n_items())'''

