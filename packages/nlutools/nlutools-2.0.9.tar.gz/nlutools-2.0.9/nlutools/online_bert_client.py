import os
try:
    from bert_serving.client import BertClient
except Exception:
    print('Installing bert-serving-client... Please try again!')
    os.system('pip install bert-serving-client==1.9.6')


class bert_vector(object):

    def __init__(self, ip='192.168.7.221'):
        try:
            self.bc_wwm_ext = BertClient(ip=ip, port=1246, port_out=5551, check_version=False)
        except Exception as e:
            print('Error!','failed to connect bert service with wwm_ext client, detail info followed as: ', e)
        try:
            self.bc_cv = BertClient(ip=ip, port=1247, port_out=5552, check_version=False)
        except Exception as e:
            print('Error!','failed to connect bert service with cv client, detail info followed as: ', e)
    
    def parse(self, texts, mode):
        if mode == 'wwm_ext':
            return self.bc_wwm_ext.encode(texts)
        elif mode == 'cv':
            return self.bc_cv.encode(texts)
        else:
            return {"err_msg": "Only support mode `wwm_ext` or `cv`"}
        
    def close(self, mode):
        if mode == 'wwm_ext':
            self.bc_wwm_ext.close()
        elif mode == 'cv':
            self.bc_cv.close()
