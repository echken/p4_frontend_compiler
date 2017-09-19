import string
import os,sys,re

class p4_dumper():
    def __init__(self):
	self.P4Table = {}
	self.P4ActionFunction = {}
	pass
    '''
    def dump_to_dict(self):
	f = open('./p4_text', 'r+')
	line_list = f.readlines()
	i = 0 
	while i < len(line_list):
            table_match = re.match('^\\s*table\\s+.*{\n', line_list[i])
            action_match = re.match('^\\s*action(.*)\\s*{\n', line_list[i])
	    if table_match!=None
    '''
    def MAT_to_json(self, p4_text):
        ##processing line of code as read line
	##f = open('./p4_text', 'r+')
	line_list = p4_text
	i = 0
	## first read p4_text,
	while i<len(line_list): 
	    table_match = re.match('^\\s*table\\s+.+\\s*{', line_list[i]) ##table definition
	    action_match = re.match('^\\s*action\\s+.+\(.*\)\\s*{', line_list[i]) ## action definition
            if table_match!=None and action_match==None:
		P4Table_name = self.get_table_name(line_list[i])
		i = i+1
		pass
		while re.match('^\\s*actions\\s*{', line_list[i])==None:  ##actions of logical table
		    ## if this line is not the start point of actions definition
		    i = i+1  ## match fields 
		    pass
		pass
		i = i+1
		action_function_list = []
		while re.match('^\\s*}', line_list[i])==None: ## or re.match('.*;\\s*}\n', line_list[i])
                    ## if this line is still actions definition
                    action_function = line_list[i].lstrip().split(';')[0]  ##action name
		    action_function_list.append(action_function) ## function list of this table
	            i = i+1
		    pass
		pass
		self.P4Table[P4Table_name] = action_function_list		
		i = i+1
		while re.match('^\\s*}', line_list[i])==None:
		    i= i+1
		    pass
		pass
		i = i+1
		continue
	    
	    ##table_match = re.match('^\\s*table\\s+.*{\n', line_list[i])
	    ##action_match = re.match('^\\s*action(.*)\\s*{\n', line_list[i])
            elif table_match==None and action_match!=None:  ## action match
	        action_function_name = line_list[i].split()[1][0:line_list[i].split()[1].index('(')]
		i = i+1
		primitive_action_dict = {}
		primitive_action_num = 0
		print '%s'%action_function_name
		pass
	        while re.match('^\\s*}', line_list[i])==None:  ## for each line in actions definition
		    if line_list[i] == '':
			i = i+1
			continue
		    else:
		        primitive_action_param_list = []
			print line_list[i] 
		        param_start_index = line_list[i].lstrip().split(';')[0].index('(') + 1
                        param_end_index = line_list[i].lstrip().split(';')[0].index(')');
		        primitive_action_name = line_list[i].lstrip().split(';')[0][0:param_start_index -1]
			if param_start_index == param_end_index:
			    primitive_aciton_param_list = []
			else:
		            primitive_action_param_list = [line_list[i].lstrip().split(';')[0][param_start_index:param_end_index].split(',')[x].strip() for x in range(len(line_list[i].lstrip().split(';')[0][param_start_index:param_end_index].split(',')))]
		        primitive_action_param_list.insert(0,primitive_action_name) 
		        primitive_action_dict[primitive_action_num] = primitive_action_param_list
		        primitive_action_num += 1
		        i = i+1
		    pass
		self.P4ActionFunction[action_function_name] = primitive_action_dict
		i = i+1
		continue
		pass
	    ##table_match = re.match('^\\s*table\\s+.*{\n', line_list[i])
	    ##action_match = re.match('^\\s*action(.*)\\s*{\n', line_list[i])
	    else:                   ## table_match == none and action_match == none: 
		i = i+1
		continue
		pass
	    pass
	##f.close()

	##-----------------------------------------------------------------
	## read all lines p4 code to buffer, and then, processing that
	'''
	f = open('./p4_text', 'r+')
	line_list = f.readlines()
	i = 0
	## first read p4_text,
	while i<len(line_list): 
	    table_match = re.match('^\\s*table\\s+.*{\n', line_list[i])
	    action_match = re.match('^\\s*action(.*)\\s*{\n', line_list[i])
            if table_match!=None and action_match==None:
		P4Table_name = self.get_table_name(line_list[i])
		i = i+1
		pass
		while re.match('^\\s*actions\\s*{\n', line_list[i])==None:
		    ## if this line is not the start point of actions definition
		    i = i+1  ## match fields 
		    pass
		pass
		i = i+1
		action_function_list = []
		while re.match('^\\s*}\n', line_list[i])==None: ## or re.match('.*;\\s*}\n', line_list[i])
                    ## if this line is still actions definition
                    action_function = line_list[i].lstrip().split(';')[0]  ##action name
		    action_function_list.append(action_function) ## function list of this table
	            i = i+1
		    pass
		pass
		self.P4Table[P4Table_name] = action_function_list		
		i = i+1
		while re.match('^\\s*}\n', line_list[i])==None:
		    i= i+1
		    pass
		pass
		i = i+1
		continue
	    
	    ##table_match = re.match('^\\s*table\\s+.*{\n', line_list[i])
	    ##action_match = re.match('^\\s*action(.*)\\s*{\n', line_list[i])
            elif table_match==None and action_match!=None:  ## action match
	        action_function_name = line_list[i].split()[1][0:line_list[i].split()[1].index('(')]
		i = i+1
		primitive_action_dict = {}
		primitive_action_num = 0
		pass
	        while re.match('^\\s*}\n', line_list[i])==None:  ## for each line in actions definition
		    primitive_action_param_list = [] 
		    param_start_index = line_list[i].lstrip().split(';')[0].index('(') + 1
                    param_end_index = line_list[i].lstrip().split(';')[0].index(')');
		    primitive_action_name = line_list[i].lstrip().split(';')[0][0:param_start_index -1]
		    primitive_action_param_list = [line_list[i].lstrip().split(';')[0][param_start_index:param_end_index].split(',')[x].strip() for x in range(len(line_list[i].lstrip().split(';')[0][param_start_index:param_end_index].split(',')))]
		    primitive_action_param_list.insert(0,primitive_action_name) 
		    primitive_action_dict[primitive_action_num] = primitive_action_param_list
		    primitive_action_num += 1
		    i = i+1
		pass
		self.P4ActionFunction[action_function_name] = primitive_action_dict
		i = i+1
		continue
		pass
	    ##table_match = re.match('^\\s*table\\s+.*{\n', line_list[i])
	    ##action_match = re.match('^\\s*action(.*)\\s*{\n', line_list[i])
	    else:                   ## table_match == none and action_match == none: 
		i = i+1
		continue
		pass
	    pass
	f.close()
	'''
    def get_table_name(self, line_code):
	table_name = line_code.split()[1].rstrip('{') ## if a space is located between table_name and { ,
	return table_name
'''
if __name__ == '__main__':
    p4_dumper_instance = p4_dumper()
    p4_dumper_instance.MAT_to_json(p4_text)
'''
