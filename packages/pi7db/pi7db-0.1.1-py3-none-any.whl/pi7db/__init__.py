import os,errno
import shutil
import glob
import hashlib
from .status import error,success,info
from .functions.functions import *
from .functions.subclass import subclass
from .operators import *


class pi7db:
  def __init__(self,db_name,db_path=os.getcwd()):
   self.db_np,self.db_name = os.path.join(db_path,db_name),db_name
   self.config_file,self.coll_name = os.path.join(self.db_np,db_name),None
   if not os.path.exists(self.db_np):os.makedirs(self.db_np)
   if not os.path.exists(f"{self.config_file}.json"):
    self.config = {'secret-key':None,'enc_type':'json'}
    writejson(self.config_file,self.config)
   else:self.config=openjson(self.config_file)
     
  def __getattr__(self, attrname):
   path=self.coll_name=os.path.join(self.db_np,attrname)
   SubClass = type(attrname,(subclass,),{'coll_name':self.coll_name,'config':self.config,'db_name':self.db_name})
   SubClass = SubClass()
   if not os.path.exists(path):os.mkdir(path)
   return SubClass
  
  def key(self,password):
   key = hashlib.md5(password.encode()).hexdigest()
   if self.config['secret-key'] is not None: 
    if key != self.config['secret-key']:raise ValueError(error.e0)
   else:
     self.config = {'secret-key':key,'enc_type':'pi7db'}
     writejson(self.config_file,self.config)

  def changekey(self,old_key,New_key):
   files,old_key,New_key = glob.glob(f"{self.db_np}/*/*."),hashlib.md5(old_key.encode()).hexdigest(),hashlib.md5(New_key.encode()).hexdigest()
   if old_key == openjson(self.config_file)['secret-key']:
    for x_js in files:
     writejson(x_js[:-len(self.config['enc_type'])-1],openjson(x_js[:-len(self.config['enc_type'])-1],old_key),New_key)
     if os.path.exists(x_js):os.remove(x_js)
    writejson(self.config_file,{'secret-key':New_key})
   else:raise ValueError(error.e1)

  def write(self,coll_name,file_name,data=None):
   try:
      path = os.path.join(self.db_np,coll_name);create_coll(path)
      writejson(f"{path}/{file_name}",data,self.config['secret-key'])
      return success.s0(file_name, self.coll_name)
   except Exception as e:return error.e4
  
  def update(self,coll_name,file_name,data_arg):
   try:
    js_data=openjson(f"{self.db_np}/{coll_name}/{file_name}",self.config['secret-key']) 
    if isinstance(data_arg,dict):js_data.update(data_arg)
    else:return error.e2
    writejson(f"{self.db_np}/{coll_name}/{file_name}",js_data,self.config['secret-key'])
    return success.s1(file_name)
   except OSError as e:
    if e.errno == errno.ENOENT:return error.e3(file_name)
    else:return e
  
  def read(self,coll_name=None,file_name=None,key_name=None,**kwargs):
   kwargs = extract_kwargs(kwargs)
   if key_name is not None:return {"data":openjson(f"{self.db_np}/{coll_name}/{file_name}",self.config['secret-key'])[key_name],"status":1}
   elif file_name is not None:data_files=[f"{self.db_np}/{coll_name}/{file_name}*"]
   else:data_files = glob.glob(f"{self.db_np}/*/*.{self.config['enc_type']}")[kwargs['f_a']:kwargs['l_a']]
   r_data = {"data":[],"status":1}
   for x_file in data_files:r_data['data'].append(openjson(x_file[:-len(self.config['enc_type'])-1],self.config['secret-key']))
   return r_data  
    
  def trash(self,coll_name,file_name=None,key_name=None):
   if key_name is not None:
     tr_data = openjson(f"{self.db_np}/{coll_name}/{file_name}",self.config['secret-key']);tr_data.pop(key_name)
     writejson(f"{self.db_np}/{coll_name}/{file_name}",tr_data,self.config['secret-key'])
     return success.s2(key_name,file_name)
   elif file_name is not None:
     os.remove(f"{self.db_np}/{coll_name}/{file_name}.{self.config['enc_type']}")
     return success.s3(file_name)
   else:
     shutil.rmtree(f"{self.db_np}/{coll_name}", ignore_errors=False, onerror=None)
     return success.s4(coll_name)
 
  def sort(self,coll_name,command_tup=None,order=False,**kwargs):
   kwargs = extract_kwargs(kwargs)
   if isinstance(coll_name,set):all_files=glob.glob(f"{self.db_np}/*/*")[kwargs['f_a']:kwargs['l_a']]
   else:all_files = glob.glob(f"{self.db_np}/{coll_name}/*")[kwargs['f_a']:kwargs['l_a']]
   r_data = {"data":[],"status":1}
   for x_file in all_files:r_data['data'].append(openjson(x_file[:-len(self.config['enc_type'])-1],self.config['secret-key']))
   if isinstance(command_tup,set):
    key_tup = "i"+str([[x] for x in command_tup])[1:-1].replace(', ',"")
    r_data['data'] = sorted(r_data['data'], key = lambda i:(exec('global s;s = %s' % key_tup),s),reverse=order)
   else: 
    if isinstance(command_tup,str):r_data['data'] = sorted(r_data['data'],key = lambda i: i[command_tup],reverse=order)
   return r_data  
   
  def filter(self,*command_tup,**kwargs):
   kwargs = extract_kwargs(kwargs)
   if isinstance(command_tup[0],str):command_tup,all_files = list(command_tup[1:]),glob.glob(f"{self.db_np}/{command_tup[0]}/*")[kwargs['f_a']:kwargs['l_a']]
   else:all_files = glob.glob(f"{self.db_np}/*/*")[kwargs['f_a']:kwargs['l_a']]
   r_data,command_arr= {"data":[],'status':1},[]
   if OR in command_tup:
    for x_p in command_tup:
      if x_p != OR:command_arr.append(x_p)
    for command in command_arr:
     data_get = andfilter(command,self.config,all_files)
     for x in data_get:
      if x not in r_data['data']:r_data['data'].append(x)
    return r_data
   else:
    for x_r in andfilter(command_tup[0],self.config,all_files):r_data['data'].append(x_r)
    return r_data
    
    
