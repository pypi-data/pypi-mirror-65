import json
from ..operators import *
from .. import cryptopidb as crdb
from ..status import error,success,info
import os

def openjson(file_path,key=None):
     if key is None:
       with open(f"{file_path}.json") as f:j_data = json.load(f)
       return j_data 
     else:
       data = crdb.decrypt_file(file_path,key.encode())
       return json.loads(data)

def writejson(file_path,data,key=None):
     if key is None:
      with open(f"{file_path}.json", 'w') as f:json.dump(data, f)
      return True
     else:
      jsdata = json.dumps(data);crdb.encrypt_file(file_path,key.encode(),jsdata)
      return True

def extract_kwargs(kw_dic):
     if len(kw_dic):
      if 'FIRST' in kw_dic:return {"f_a":None,"l_a":kw_dic['FIRST']}
      if 'LAST' in kw_dic:return {"f_a":-kw_dic['LAST'],"l_a":None}
      if 'FROM' in kw_dic:kw_dic["f_a"] = kw_dic['FROM']
      else:kw_dic["f_a"]=None
      if 'TO' in kw_dic:kw_dic["l_a"] = kw_dic['TO']
      else:kw_dic["l_a"]=None
      return kw_dic
     else:return {"f_a":None,"l_a":None}

def keys_extractor(dic):
  data,current_pair,bool = {"keys":[],"sub_keys":[None],"value":[]},dic,True
  while bool:
   for x in current_pair:
     try:
      if len(current_pair.keys()) > 1:data['sub_keys'],bool,data['value'] = list(current_pair.keys()),False,list(current_pair.values());break
      else:data['keys'].append(x);current_pair[x].keys();current_pair = current_pair[x]    
     except:bool,data['value'] = False ,list(current_pair.values())
  return data

def operator_fil(js_data,F_data,value,op_action,action,word_len):
  r_data = []
  if op_action == LET:
   if js_data < value:r_data.append(F_data)  
  if op_action == GRT:
   if js_data > value:r_data.append(F_data) 
  if action == "fr_skip": 
   if js_data[word_len:] == value:r_data.append(F_data) 
  if action == "ba_skip":
   if js_data[:word_len] == value:r_data.append(F_data) 
  if action == "all_skip":
   if value in js_data:r_data.append(F_data) 
  else:
   if js_data == value:r_data.append(F_data)
  try:return r_data[0]
  except:pass

def andfilter(command_tup,config,all_files):
  r_data,enc_key = [],config['secret-key']
  for command in list(command_tup):
   op_action = None
   if isinstance(command_tup[command],tuple):
    value,op_action = command_tup[command][1],command_tup[command][0]
    if not isinstance(value,int):return error.e5(op_action)
   else:value = command_tup[command]
   action,word_len = None,0
   if isinstance(value,str):
    if value[-2:] == '**' and value[:2] == '**':word_len,value,action = len(value[2:-2]),value[2:-2],"all_skip"
    if value[-2:] == '**':word_len,value,action = len(value[:-2]),value[:-2],"ba_skip"
    if value[:2] == '**':word_len,value,action = -int(len(value[2:])),value[2:],"fr_skip"
   if isinstance(value,str) or isinstance(value,int):
    if not r_data:
     for x in all_files:
       F_data = openjson(x[:-len(config['enc_type'])-1],enc_key)
       try:
        fr_data = operator_fil(F_data[command],F_data,value,op_action,action,word_len)
        if fr_data:r_data.append(fr_data)
       except:pass
     if not r_data:return []
    else:
     dup_data,r_data = r_data,[]
     for x in dup_data:
       F_data = x
       try:
        fr_data = operator_fil(F_data[command],F_data,value,op_action,action,word_len)
        if fr_data:r_data.append(fr_data)
       except:pass
     if not r_data:return []
   if isinstance(value,dict):
    keys_extract = keys_extractor(value)
    for s_k in enumerate(keys_extract['sub_keys']):
     if s_k[1] is None:key_tup,value = f"F_data['{command}']"+str([[x] for x in keys_extract['keys']])[1:-1].replace(', ',""),keys_extract['value'][0]
     else:key_tup,value = f"F_data['{command}']"+str([[x] for x in keys_extract['keys']])[1:-1].replace(', ',"")+f"['{s_k[1]}']",keys_extract['value'][s_k[0]]
     if not r_data:
      for x in all_files:
       F_data = openjson(x[:-len(config['enc_type'])-1],enc_key)
       try:
        exec('global globalfilter; globalfilter = %s' % key_tup)
        fr_data = operator_fil(globalfilter,F_data,value,op_action,action,word_len)
        if fr_data:r_data.append(fr_data)     
       except:pass
      if not r_data:return []
     else:
      dup_data,r_data = r_data,[]
      for x in dup_data:   
       F_data = x
       try:
        exec('global globalfilter; globalfilter = %s' % key_tup)
        fr_data = operator_fil(globalfilter,F_data,value,op_action,action,word_len)
        if fr_data:r_data.append(fr_data)
       except:
        pass
      if not r_data:return []
  return r_data

def create_coll(path):
  if not os.path.exists(path):os.mkdir(path)