from p4_dumper import *
from json_decoder import *
import re
import json

class action_dependency_identify:
    def __init__(self, p4_text):
	#self.action_function_name = action_function_name
	self.p4_dumper = p4_dumper()
	self.p4_dumper.MAT_to_json(p4_text)
	self.json_decoder = json_decoder()
	##self.primitive_action_definition = "./primitives.json"
	self.p4_table = self.p4_dumper.P4Table
	self.p4_action_function = self.p4_dumper.P4ActionFunction
	##self.num_of_primitive_action = len(self.p4_action_function[action_function_name])	
	##self.primitive_action_list = [(self.p4_action_function[action_function_name][i])for i in range(self.num_of_primitive_action)]
	pass
    '''
    def primitive_action_access(self):
	primitive_file = open(self.primitive_action_definition, 'r')
	primitive_obj = json.load(primitive_file)
	#primitives_dict = self.json_decoder.decode_dict(primitive_obj)
	primitive_file.close()
	return self.json_decoder.decode_dict(primitive_obj) 
    '''
    def dependency_identify(self, action_function_name, primitive_action_param_access_attr):
        #get len of action function
        num_of_primitive_action = len(self.p4_action_function[action_function_name]) 
	primitive_action_list = [self.p4_action_function[action_function_name][i]for i in range(num_of_primitive_action)]
	dependency_of_primitive_action = [[0 for x in range(num_of_primitive_action)]for y in range(num_of_primitive_action)]
	## initial param 
	num_args_of_primitive_action = [(len(primitive_action_list[i])-1) for i in range(num_of_primitive_action)]  ## now, we don't process default param
	primitive_action_name = [primitive_action_list[i][0] for i in range(num_of_primitive_action)]
	primitive_action_param = [primitive_action_list[i][1:len(primitive_action_list[i])] for i in range(num_of_primitive_action)]
	#primitive_dict = self.primitive_action_access()
	access_attr_list = {}
	for i in range(num_of_primitive_action):
	    access_attr_list[i] = {}
	    if num_args_of_primitive_action[i] == 0:
		print '%s%s\n'%(action_function_name,primitive_action_list[i])
		access_attr_list[i] = {None}
		continue
	    else:
	        for j in range(num_args_of_primitive_action[i]):
		    print '%s%s\n'%(action_function_name,primitive_action_list[i])
		    access_attr_list[i][j] = primitive_action_param_access_attr[primitive_action_name[i]]['properties'][primitive_action_param_access_attr[primitive_action_name[i]]['args'][j]]['access']
 
	    ##access_attr_list = [(primitive_dict[primitive_action_name[i]]['properties'][primitive_dict[primitive_action_name[i]]['args'][x]]['access'])for x in range(num_args_of_primitive_action[i])]

        ##access_attr_list = [[primitive_action_param_access_attr[primitive_action_name[i]]['properties'][primitive_action_param_access_attr[primitive_action_name[i]]['args'][x]]['access']for x in range(num_args_of_primitive_action[i])]for i in range(num_of_primitive_action)]

        for i in range(num_of_primitive_action):
	    if access_attr_list[i] == {None}:
		continue
	    else:	
	        for j in range(num_args_of_primitive_action[i]):
		    if access_attr_list[i][j] == 'write':
		        for k in range(i+1, num_of_primitive_action):## for primitive action after the ith action
			    if re.match(r'register*', primitive_action_name[i]) != None and re.match(r'register*', primitive_action_name[k]) != None:  # register read and write primitive action 
			        if primitive_action_name[i] == 'register_read' and primitive_action_name[k] == 'register_read':
				    if primitive_action_param[i][0] == primitive_action_param[k][0]:
				        dependency_of_primitive_action[i][k] = 3
				        pass
			        elif primitive_action_name[i] == 'register_read' and primitive_action_name[k] == 'register_write':
				    if primitive_action_param[i][0] == primitive_action_param[k][2]:
				        dependency_of_primitive_action[i][k] = 2
				        pass
				    if primitive_action_param[i][1] == primitive_action_param[k][0] and primitive_action_param[i][2] == primitive_action_param[k][1]:
				        dependency_of_primitive_action[i][k] = 1
				        pass
			        elif primitive_action_name[i] == 'register_write' and primitive_action_name[k] =='register_read':
				    if primitive_action_param[i][0] == primitive_action_param[k][1] and primitive_action_param[i][1] == primitive_action_param[k][2]:
				        dependency_of_primitive_action[i][k] = 2
				        pass
				    if primitive_action_param[i][2] == primitive_action_param[k][0]:
				        dependency_of_primitive_action = 1
				        pass
			        elif primitive_action_name[i] =='register_write' and primitive_action_name[k] == 'register_write':
				    if primitive_action_param[i][0] == primitive_action_param[k][0] and primitive_action_param[i][1] == primitive_action_param[k][1]:
				        dependency_of_primitive_action[i][k] = 3
				        pass
			    else:
			        for l in range(num_args_of_primitive_action[k]):
			            if primitive_action_param[k][l] == primitive_action_param[i][j]:
				        if access_attr_list[k][l] == 'read': # read-after-write
				            dependency_of_primitive_action[i][k] = 2
				        elif access_attr_list[k][l] == 'write': #write-after-write
				            dependency_of_primitive_action[i][k] = 3
				        else:
				            print '%s %s of %s access attr error'%(primitive_action_name[k],prmitive_action_param[l],action_function_name)
			            else:
				        continue
		    elif access_attr_list[i][j] == 'read':
		        for k in range(i+1, num_of_primitive_action):
			    if re.match(r'register*', primitive_action_name[i]) != None and re.match(r'register*', primitive_action_name[k]) != None:  # register read and write primitive action 
			        if primitive_action_name[i] == 'register_read' and primitive_action_name[k] == 'register_read':
				    if primitive_action_param[i][0] == primitive_action_param[k][0]:
				        dependency_of_primitive_action[i][k] = 3
				        pass
			        elif primitive_action_name[i] == 'register_read' and primitive_action_name[k] == 'register_write':
				    if primitive_action_param[i][0] == primitive_action_param[k][2]:
				        dependency_of_primitive_action[i][k] = 2
				        pass
				    if primitive_action_param[i][1] == primitive_action_param[k][0] and primitive_action_param[i][2] == primitive_action_param[k][1]:
				        dependency_of_primitive_action[i][k] = 1
				        pass
			        elif primitive_action_name[i] == 'register_write' and primitive_action_name[k] =='register_read':
				    if primitive_action_param[i][0] == primitive_action_param[k][1] and primitive_action_param[i][1] == primitive_action_param[k][2]:
				        dependency_of_primitive_action[i][k] = 2
				        pass
				    if primitive_action_param[i][2] == primitive_action_param[k][0]:
				        dependency_of_primitive_action = 1
				        pass
			        elif primitive_action_name[i] =='register_write' and primitive_action_name[k] == 'register_write':
				    if primitive_action_param[i][0] == primitive_action_param[k][0] and primitive_action_param[i][1] == primitive_action_param[k][1]:
				        dependency_of_primitive_action[i][k] = 3
				        pass
			    else:
		                for l in range(num_args_of_primitive_action[k]):
			            if primitive_action_param[k][l] == primitive_action_param[i][j]:
				        if access_attr_list[k][l] == 'read':   
                                        # read-after-read no dependency
				        ##dependency_of_primitive_action[i][k] = 0
				            pass
				        elif access_attr_list[k][l] == 'write': # write-after-read
				            dependency_of_primitive_action[i][k] = 1
				        else:
				            print '%s %s of %s access attr error'%(primitive_action_name[k],prmitive_action_param[l],action_function_name)
			            else:
				        continue
		    else:  
	                print '%s %s of %s access attr error'%(primitive_action_name[i],prmitive_action_param[j],action_function_name)

	return dependency_of_primitive_action

    def p4_access(self, p4_text):
	self.p4_dumper.MAT_to_json(p4_text)
	return self.p4_dumper.P4Table, self.p4_dumper.P4ActionFunction
'''
if __name__ =='__main__':
    instance = action_dependency_identify()
    instance.dependency_identify('lookup_flowlet_map')      	
'''
