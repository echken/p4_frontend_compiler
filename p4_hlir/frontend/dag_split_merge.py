import string
from action_dependency_identify import *

class dag_splitter():
    def __init__(self):
	##self.region = [1,2,2,3,4,4]
	##self.dependency_of_primitive_action = [[0,1,0,1,0,1],[0,0,0,0,0,0],[0,0,0,0,1,0],[0,0,0,0,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0]]
	##self.action = ['a','b','c','d','e','f']
	self.region = []
	self.primitive_action_of_region = []	
        ##num_of_primitive_action = len(self.action)	
	pass
    def dag_split(self, dependency_of_primitive_action, primitive_action_dict):
	num_of_primitive_action = len(primitive_action_dict)
	self.region_split(dependency_of_primitive_action, num_of_primitive_action, primitive_action_dict)
	self.region_merge(dependency_of_primitive_action, num_of_primitive_action)
	return self.region, self.primitive_action_of_region

    def region_split(self, dependency_of_primitive_action, num_of_primitive_action, primitive_action_dict):
	# simple split DAG that was consitituted by codelet correspoding to single primitive action
       	'''
        dependency_of_primitive_action = [[0,1,0,1,0,1],[0,0,0,0,0,0],[0,0,0,0,1,0],[0,0,0,0,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        ## primitive_action_of_region = [['a'],['b','c'],['d'],['e','f']]
        ## k = len(primitive_action_of_region)
        action = ['a','b','c','d','e','f']
	primitive_action_of_region = []
        num_of_primitive_action = len(action)
	'''
        dependency = [0 for i in range(num_of_primitive_action)]  ## initial dependency matrix
        for i in range(num_of_primitive_action):
	    for j in range(num_of_primitive_action):
		dependency[i] += dependency_of_primitive_action[i][j]
		pass
	    pass
	pass

        k = 0  ## k is region id
	action_list = [] ## primitive aciton list that belong to specific region 
	##self.region.append(k)              
        for i in range(num_of_primitive_action):
            self.region.append(k) ## set region id of primitive action
	    ##action_list.append(self.action[i])
	    action_list.append(primitive_action_dict[i]) ## [primtive_action_name,para1,para2,^^^]
            if(i == num_of_primitive_action - 1):    ## last action   
                self.primitive_action_of_region.append(action_list)
		pass
	    pass
	    if(dependency[i] != 0): ## if there have any dependency between i to any other dependency
                self.primitive_action_of_region.append(action_list) # split region, append action_list
		action_list =[]  ## clear action list to append primitive action of next region
                k = k+1   ##update region id to next region
                pass
            pass
        pass

    def get_start_index_of_region(self, total_region, num_of_primitive_action):
         ##get every region start index.
	start_index_of_region = []
        for i in range(total_region):
	    for j in range(num_of_primitive_action):
                if(self.region[j] == i):
		    start_index_of_region.append(j)
    		    break
		    pass
		pass
            pass
	pass
	return start_index_of_region

    def get_total_region(self, num_of_primitive_action):  ## get total region num
	total_region = 1
	for i in range(num_of_primitive_action-1):
	    if(self.region[i] != self.region[i+1]):
		total_region += 1
		pass
	    pass
	pass
	return total_region

    def update_primitive_action_of_region(self, op_region): ## reset primitive action belong to every region
	'''
	for i in range(len(primitive_action_of_region[op_region+1])):
	    primitive_action_of_region[op_region].append(primitive_action_of_region[op_region+1][i])
	    pass
	pass
	'''
	self.primitive_action_of_region[op_region].extend(self.primitive_action_of_region[op_region+1])
	self.primitive_action_of_region.remove(self.primitive_action_of_region[op_region+1])

    def update_region(self, n, num_of_primitive_action): ## update region id of action that the number 
        for i in range(n, num_of_primitive_action):
            self.region[i] = self.region[i] - 1
            pass
        pass

    def scan_and_merge_neighbouring_region(self, op_region, dependency_of_primitive_action, num_of_primitive_action):
	merge_flags = 1
	total_region = self.get_total_region(num_of_primitive_action)
	if(op_region == total_region-1):
	    merge_flags -= 1
	    return merge_flags
	    pass
	pass

	start_index_of_region = self.get_start_index_of_region(total_region, num_of_primitive_action)
	prior_region_start = start_index_of_region[op_region]  ## op_region <= total_region - 1
	prior_region_end = start_index_of_region[op_region] + len(self.primitive_action_of_region[op_region]) - 1
	successor_region_start = start_index_of_region[op_region+1]
	successor_region_end = start_index_of_region[op_region+1] + len(self.primitive_action_of_region[op_region+1]) - 1
	##merge_flags = 1
	for i in range(prior_region_start, prior_region_end+1):
	    for j in range(successor_region_start, successor_region_end+1):
		if(dependency_of_primitive_action[i][j] != 0):
		    merge_flags -= 1
		    break
		    pass
		pass
	    pass
	    if(merge_flags == 0):
		break
		pass
	    pass
	pass
	if(merge_flags == 1):
	    ## update region and primitive_action_of_region
	    self.update_region(successor_region_start, num_of_primitive_action) 
	    self.update_primitive_action_of_region(op_region)
	    pass
	pass
	return merge_flags ## return value
	
    def region_merge(self, dependency_of_primitive_action, num_of_primitive_action):
	action_num = 0
	while(action_num < num_of_primitive_action-1):
	    op_region = self.region[action_num]
	    merge_flags = self.scan_and_merge_neighbouring_region(op_region, dependency_of_primitive_action, num_of_primitive_action)
	    if(merge_flags == 0):
		action_num = action_num + len(self.primitive_action_of_region[op_region])
		pass
	    pass
	pass

'''	
if __name__ == "__main__":
    print"main module"
    splitter = dag_splitter()
    splitter.dag_split()
'''
    #print "%s %s" %(test_instance.region,test_instance.primitive_action_of_region)
