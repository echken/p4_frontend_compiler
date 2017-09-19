from action_dependency_identify import*
from dag_split_merge import*
from json_decoder import*
import re
import os

class p4_transformer:
    def __init__(self, p4_text, p4_filename):
	##self.p4_dumper = p4_dumper()
	##self.p4_dumper.MAT_to_json()
	self.identifier = action_dependency_identify(p4_text)
	self.p4_text = p4_text
	self.p4_filename = p4_filename
	self.primitive_action_definition = './primitives.json'
	self.json_decoder = json_decoder()

    def primitive_action_access(self):
        primitive_file = open(self.primitive_action_definition, 'r')
        primitive_obj = json.load(primitive_file)
        #primitives_dict = self.json_decoder.decode_dict(primitive_obj)
        primitive_file.close()
        return self.json_decoder.decode_dict(primitive_obj)

    def p4_transform(self):
	## transfrom original p4 program to new version in which dependency of compound action is decomposed
	p4_table = self.identifier.p4_table
	p4_action_function = self.identifier.p4_action_function
	p4_code_list = self.p4_text;
	primitive_action_param_access_attr = self.primitive_action_access()
	dependency_matrix = {}	
	for table_name in p4_table.keys():## for every table in p4 program
	    dependency_matrix[table_name] = {}
	    ##dag_split_result = {}
	    primitive_action_of_region = {}
	    for action_function_name in p4_table[table_name]: ##action_function in p4 table named table_name
		dependency_matrix[table_name][action_function_name] = [[0 for x in \
                range(len(p4_action_function[action_function_name]))]for y in \
                range(len(p4_action_function[action_function_name]))]
 
		dependency_matrix[table_name][action_function_name] = self.\
                identifier.dependency_identify(action_function_name, primitive_action_param_access_attr)
	        primitive_action_dict = p4_action_function[action_function_name]
		primitive_action_of_region[action_function_name] = dag_splitter().dag_split\
		(dependency_matrix[table_name][action_function_name], primitive_action_dict)
		
		##dag_split_result[action_function_name] = self.splitter.region
		##primitive_action_of_region[action_function_name] = self.splitter.primitive_action_of_region
		# identify primitive_action_dependency of action function name
		p4_code_list = self.action_definition_transform(p4_code_list, \
                primitive_action_of_region, action_function_name)
		pass
	    p4_code_list = self.table_definition_transform(p4_code_list, primitive_action_of_region, table_name)
	    print table_name
	self.p4_codelist_to_file(p4_code_list, self.p4_filename)
	return p4_code_list
    def p4_codelist_to_file(self, line_code_list, original_p4_filename):
	'''
	annotation_line_list = []
	for i in range(len(line_code_list)):
	    print '%d\n'%i
            note_match = re.match('^\\s*#.+', line_code_list[i]) ## note
            if note_match != None:
		annotation_line_list.append(i)
	for i in range(len(annotation_line_list)):
            del line_code_list[annotation_line_list[i]]
            ##line_code_list[i] = '//' + line_code_list[i]  ## p4 annotation format: // XXXXX
	'''

	file_string = '\n'.join(line_code_list)
	filename = os.path.split(original_p4_filename)[1].split('.')[0] + '_dependency_split.p4'
	fp = open(filename, 'w')
	fp.write(file_string)
	fp.close()

    def table_definition_transform(self, p4_code_list, primitive_action_of_region, table_name):
	##transfrom one p4 table to several equality p4 table according to action transform result
	match_flag = 0
	action_flag = 0
	other_attr_flag = 0
	start_index_of_actions = 0
	end_index_of_actions = 0
	start_index_of_table = 0
	end_index_of_table = 0
	i = 0	
	## get start and end index of table/actions
	while i < len(p4_code_list):
	    ##if re.match('^\\s*',p4_code_list[i]) != None:
	    if p4_code_list[i].strip() == '':
		i = i+1
		continue
	    elif re.findall('^\\s*(.+?)\\s.+{', p4_code_list[i]) == ['table'] and \
                re.findall('^\\s*table\\s*(.+?)\\s*{', p4_code_list[i]) == [table_name]:
		start_index_of_table = i
		match_flag = 1
		i = i+1
		continue
	    elif match_flag == 1 and re.findall('^\\s*(.+?)\\s*{', p4_code_list[i]) == ['actions']:
		start_index_of_actions = i
		action_flag = 1
		i = i+1
		continue
	    elif action_flag == 1 and other_attr_flag == 0 and \
	        re.findall('^\\s*(.+?)\\s*', p4_code_list[i]) == ['}']:
		end_index_of_actions = i
		other_attr_flag = 1
		i = i+1
		continue
	    elif other_attr_flag == 1 and re.findall('^\\s*(.+?)\\s*', p4_code_list[i]) == ['}']:
		end_index_of_table = i
		break
	    else:
		i = i+1
		continue
	
	## add new action function name with format like action_function_name+'_'+ str(region_num)
	actions = []
	partition_flag = 0
	for i in range(start_index_of_actions + 1, end_index_of_actions):
	    action_function_name = p4_code_list[i].split()[0].rstrip(';')
	    region_num = len(primitive_action_of_region[action_function_name])
	    if region_num == 0 or region_num == 1:
		actions.append('\t' + action_function_name + ';')
		pass
	    else:
		partition_flag = 1  ## at least, there have one action_function that has internal dependency
	        for j in range(region_num):
		    action = '\t' + action_function_name + '_' + str(j) + ';'
		    actions.append(action)
	
        ## partition all action function from one table to several partition	
	if partition_flag == 0:
	    return p4_code_list
	else:
	    action_partition = []
	    partitions = []
	    i = 0
	    if len(actions) == 0:  ##
	        print 'acitons is none: %s'%table_name
	    elif len(actions) == 1:
	        return p4_code_list
	    else:
	        while i < len(actions)-1:
	            if actions[i].split('_')[0] == actions[i+1].split('_')[0]:
		        partitions.append(actions[i])
		        action_partition.append(partitions)
		        partitions = []
		        i = i+1
	            else:
		        partitions.append(actions[i])
		        i = i+1
	        pass
	        partitions.append(actions[len(actions)-1])
	        action_partition.append(partitions)
            pass

	##construct new table
	tables = []
	if len(action_partition) == 1:
	    return p4_code_list
	else:
	    for i in range(len(action_partition)):
	        tables.append('table' + ' ' + table_name + '_' + str(i) + ' {')
	        if i==0:
	       	    tables = tables + p4_code_list[start_index_of_table+1:start_index_of_actions+1] + \
                    action_partition[i] + p4_code_list[end_index_of_actions:end_index_of_table+1]
	        else:
		    tables = tables + [p4_code_list[start_index_of_actions]] + action_partition[i] + p4_code_list[end_index_of_actions:end_index_of_table+1]
	    ##merge other part of p4_text with newly generated table 
	    p4_code_list = p4_code_list[0:start_index_of_table] + tables +p4_code_list[end_index_of_table+1:] 
            print tables
	p4_code_list = self.control_flow_transform(p4_code_list, table_name, action_partition)
	return p4_code_list

    def action_definition_transform(self, p4_code_list, primitive_action_of_region, action_function_name):
	## transform one p4 compound action to serveral action according to primitive action dependency in it
	#----------------------------------------------------------------------------------------------	    
        #convert p4 code text string to p4 code list. for compound action in every p4_dumper.P4Table, if it 
        #has primitive action dependency between primitive action in this compound action, using self. 
        #identifier to identify primitive aciton dependency in it. and then, using splitter() to decompose
	#primitive action dependency. finally, original p4 program is converted to new version that decompose
	#primitive action dependency.
	region_num = len(primitive_action_of_region[action_function_name])
	if region_num > 1:
	    i = 0
	    action_flag = 0
	    start_index_of_action_function = 0
	    end_index_of_action_function = 0
	    decomposed_action = []
	    while i<len(p4_code_list):
		if re.findall('^\\s*action\\s*(.+?)\(\)\\s*{',p4_code_list[i]) == [action_function_name]: 
		    action_flag = 1
		    start_index_of_action_function = i
		    action_function_param = re.findall('^\\s*action\\s+.+\((.*?)\)\\s*{', p4_code_list[i])
		    for j in range(region_num):
			decomposed_action.append('action '+action_function_name+'_'+str(j)+'('+action_function_param[0] + ') {') 
			for primitive_action in primitive_action_of_region[action_function_name][j]:
			    single_primitive_action = ''
			    for k in range(len(primitive_action)):
				if k==0:
				    single_primitive_action = '\t'+primitive_action[k]+'('
				elif k==len(primitive_action)-1:
				    single_primitive_action = single_primitive_action + primitive_action[k] + ');'
				else:
				    single_primitive_action = single_primitive_action + primitive_action[k]+', '
			    decomposed_action.append(single_primitive_action)
			decomposed_action.append('}')  #  single region end
		    i = i+1
		    continue
		##record the end index of original action definition that contains dependency
		elif action_flag == 1 and re.match('^\\s*}', p4_code_list[i]) != None:
		    end_index_of_action_function = i
		    break
		else:
		    i = i+1
		    continue
	    ##new_table = decomposed_action.split('\n')
	    p4_code_list = p4_code_list[0:start_index_of_action_function] + decomposed_action + p4_code_list[end_index_of_action_function+1:] 
	else:
	    print 'action function %s have not internal dependency!'%action_function_name
	return p4_code_list

    def control_flow_transform(self, p4_code_list, table_name, action_partition):
	##transform apply(table) scentence in the control flow according to table transform result
	##----------------------------------------------------------------------------------------
	##control flow transform
	i = 0
	index_of_table_in_controlflow = []
	while i < len(p4_code_list):
	    ##if p4_code_list[i].split('(')[1].split(')')[0] == table_name:
	    if re.findall('^\\s*apply\((.+)\);\\s*', p4_code_list[i]) == [table_name]:
		index_of_table_in_controlflow.append(i)
		i = i+1
	    else:
		i = i+1
	pass
	new_table = []   ## extend table that contain some action function that have internal dependency
        for k in range(len(action_partition)):
            table = '\tapply(' + table_name + '_' + str(k) + ');'
            new_table.append(table)
 
	for i in range(len(index_of_table_in_controlflow)):##in control flow, there have not only one table 
	    p4_code_list = p4_code_list[:index_of_table_in_controlflow[i]] + new_table + p4_code_list[index_of_table_in_controlflow[i]+1:]
	    if i+1 <= len(index_of_table_in_controlflow) - 1:
		index_of_table_in_controlflow[i+1] = index_of_table_in_controlflow[i+1] + len(action_partition)-1
	return p4_code_list 
'''
if __name__ == '__main__':
    f = open('./p4_text','r')
    s = f.readlines()
    f.close()
    transformer = p4_transformer(s)
    transformer.p4_transform()
'''
