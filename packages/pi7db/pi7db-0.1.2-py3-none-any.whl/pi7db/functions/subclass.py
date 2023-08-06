from .functions import *
import glob
import os,errno
import shutil
import glob
from ..status import error,success,info
from ..operators import *

class subclass:
  def __init__(self):
      pass
  
  def write(self,file_name,data):
   try:
      writejson(os.path.join(self.db_name,self.coll_name,file_name),data,self.config['secret-key'])
      return success.s0(file_name, self.coll_name)
   except Exception as e:return error.e4
  
  def update(self,file_name,*data_arg):
   try: 
    file_path=os.path.join(self.coll_name,file_name);js_data=openjson(file_path,self.config['secret-key']) 
    for data in data_arg:     
     if isinstance(data,dict):js_data.update(data)
     else:return error.e2
    writejson(file_path,js_data,self.config['secret-key'])
    return success.s1(file_name)
   except OSError as e:
    if e.errno == errno.ENOENT:return error.e3(self.coll_name)
    else:return e
  
  def read(self,file_name=None,key_name=None,**kwargs):
   kwargs = extract_kwargs(kwargs)   
   if key_name is not None:return {"data":openjson(f"{self.coll_name}/{file_name}",self.config['secret-key'])[key_name],"status":1}
   elif file_name is not None:data_files=glob.glob(f"{self.coll_name}/{file_name}.{self.config['enc_type']}")
   else:data_files = glob.glob(f"{self.coll_name}/*")[kwargs['f_a']:kwargs['l_a']]
   r_data = {"data":[],"status":1}
   for x_file in data_files:r_data['data'].append(openjson(x_file[:-len(self.config['enc_type'])-1],self.config['secret-key']))
   return r_data  

  def trash(self,file_name=None,key_name=None):
   if key_name is not None:
     tr_data = openjson(f"{self.coll_name}/{file_name}",self.config['secret-key']);tr_data.pop(key_name)
     writejson(f"{self.coll_name}/{file_name}",tr_data,self.config['secret-key'])
     return success.s2(key_name,file_name)
   elif file_name is not None:os.remove(f"{self.coll_name}/{file_name}.{self.config['enc_type']}");return success.s3(file_name)
   else:shutil.rmtree(self.coll_name, ignore_errors=False, onerror=None);return success.s4(self.coll_name)
  
  def sort(self,command_tup,order=False,**kwargs):
   kwargs=extract_kwargs(kwargs)
   all_files,r_data= glob.glob(f"{self.coll_name}/*")[kwargs['f_a']:kwargs['l_a']],{"data":[],"status":1}
   for x_file in all_files:r_data['data'].append(openjson(x_file[:-len(self.config['enc_type'])-1],self.config['secret-key']))
   if isinstance(command_tup,set):
    key_tup = "i"+str([[x] for x in command_tup])[1:-1].replace(', ',"")
    r_data['data'] = sorted(r_data['data'], key = lambda i:(exec('global s;s = %s' % key_tup),s),reverse=order)
   else: 
    if isinstance(command_tup,str):r_data['data'] = sorted(r_data['data'],key = lambda i: i[command_tup],reverse=order)
   return r_data  
  
  def filter(self,*command_tup,**kwargs):
   kwargs = extract_kwargs(kwargs)
   r_data,command_arr,all_files= {"data":[],'status':1},[],glob.glob(f"{self.coll_name}/*")
   if OR in command_tup:
    for x_p in command_tup:
      if x_p != OR:command_arr.append(x_p)
    for command in command_arr:
     data_get = andfilter(command,self.config,all_files)
     for x in data_get[kwargs['f_a']:kwargs['l_a']]:
      if x not in r_data['data']:r_data['data'].append(x)
    return r_data
   else:
    for x_r in andfilter(command_tup[0],self.config,all_files)[kwargs['f_a']:kwargs['l_a']]:r_data['data'].append(x_r)
    return r_data

    
    