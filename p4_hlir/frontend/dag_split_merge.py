import string
from action_dependency_identify import *

class dag_splitter():
    def __init__(self):
	##self.region = [1,2,2,3,4,4]
	##self.dependency_of_primitive_action = [[0,1,0,1,0,1],[0,0,0,0,0,0],[0,0,0,0,1,0],[0,0,0,0,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0]]
	##self.primitive_action_dict = ['a','b','c','d','e','f']
	self.primitive_action_of_region = []	
        ##num_of_primitive_action = len(self.action)	
	pass

    def dag_split(self, dependency_of_primitive_action, primitive_action_dict):
	# using Breadth-First Traverse to determine the subregion of original compound action 
        #dependency_matrix = dependency_of_primitive_action;
	while len(dependency_of_primitive_action) != 0:
	    dependency = self.region_split(dependency_of_primitive_action, primitive_action_dict)
	    dependency_of_primitive_action, primitive_action_dict = self.dependency_matrix_update(dependency, dependency_of_primitive_action, primitive_action_dict)
	    pass
        pass
	return self.primitive_action_of_region

    def region_split(self, dependency_of_primitive_action, primitive_action_dict):
	#split dag that constitued of codelet which is primitive action
	num_remained_primitive_action = len(dependency_of_primitive_action)
	# dependency between primitive action i and any other primitive action. ex. i with 0-n
        dependency = [0 for i in range(num_remained_primitive_action)]
        for i in range(num_remained_primitive_action):
	    for j in range(num_remained_primitive_action):
		dependency[j] = dependency[j] + dependency_of_primitive_action[i][j]
		pass
	    pass
	pass
        action_list = []
        for i in range(num_remained_primitive_action):
	    if dependency[i] == 0:
		# update action list of specific region if there have not any dependency between this 
		action_list.append(primitive_action_dict[i]) 
		pass
	    pass
        self.primitive_action_of_region.append(action_list)
        return dependency

    def dependency_matrix_update(self, dependency, dependency_of_primitive_action, primitive_action_dict):
	update_flag = []
	for i in range(len(dependency)):
	    if dependency[i] == 0:
		update_flag.append(i)
		pass
	    pass

# update each row of dependency matrix,(delete colomun that have not any dependency between other primitive)
	for i in range(len(dependency)):
	    dependency_temp = []
	    for j in range(len(update_flag)):
		if j == 0:
		    if update_flag[j] == 0:
			continue
		    else:
		        dependency_temp = dependency_of_primitive_action[i][:update_flag[j]]
			pass 
		elif j == len(update_flag) - 1:
		    if update_flag[j] == len(dependency) - 1: # last primitive 
			dependency_temp = dependency_temp + dependency_of_primitive_action[i][update_flag\
                        [j-1]+1:update_flag[j]]
			pass
		    else:
			dependency_temp = dependency_temp + dependency_of_primitive_action[i][update_flag[j-1]+1:update_flag[j]] + dependency_of_primitive_action[i][update_flag[j] + 1:]
		else:
		    dependency_temp = dependency_temp + dependency_of_primitive_action[i][update_flag[j-1]+1:update_flag[j]]


	    dependency_of_primitive_action[i] = dependency_temp
	    pass
	# delete row that corresponding to other primitive,(edge of codelet dag)
	dependency_matrix_row_temp = []
	primitive_action_temp = []
	for i in range(len(update_flag)):
	    if i == 0:
		if update_flag[i] == 0:
		    continue
		else:
		    dependency_matrix_row_temp = dependency_of_primitive_action[:update_flag[i]]
		    primitive_action_temp = primitive_action_dict[:update_flag[i]]
		    pass	
	    elif i == len(update_flag) - 1:
		if update_flag[i] == len(dependency) - 1:
		    dependency_matrix_row_temp = dependency_matrix_row_temp + dependency_of_primitive_action[update_flag[i-1]+1 : update_flag[i]]
		    primitive_action_temp = primitive_action_temp + primitive_action_dict[update_flag[i-1]+1 : update_flag[i]]
		else:
		    dependency_matrix_row_temp = dependency_matrix_row_temp + dependency_of_primitive_action[update_flag[i-1]+1 : update_flag[i]] + dependency_of_primitive_action[update_flag[i]+1:]
		    primitive_action_temp = primitive_action_temp + primitive_action_dict[update_flag[i-1]+1 : update_flag[i]] + primitive_action_dict[update_flag[i]+1:]
	    else:
		dependency_matrix_row_temp = dependency_matrix_row_temp + dependency_of_primitive_action[update_flag[i-1]+1 : update_flag[i]]
		primitive_action_temp = primitive_action_temp + primitive_action_dict[update_flag[i-1]+1: update_flag[i]]
	    pass
	dependency_of_primitive_action = dependency_matrix_row_temp
	primitive_action_dict = primitive_action_temp
	pass
        return dependency_of_primitive_action, primitive_action_dict
'''
if __name__ == "__main__":
    print"main module"
    splitter = dag_splitter()
    ##primitive_action_dict = ['a','b','c','d','e','f']
    ##dependency_of_primitive_action = [[0,1,0,1,0,1],[0,0,0,0,0,0],[0,0,0,0,1,0],[0,0,0,0,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    
    primitive_action_dict = ['a','b','c','d','e','f','g','h']
    dependency_of_primitive_action = [[0,1,0,0,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,1],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0]]
    splitter.dag_split(dependency_of_primitive_action, primitive_action_dict)
    print"%s" %(splitter.primitive_action_of_region)
'''
