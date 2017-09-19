import json
import sys
import getopt

class json_decoder():
    def __init__(self):
	pass
    '''
    def decoder(self, argv):
	try:
	    opts,args = getopt.getopt(argv[1:], 'hf:', ['help','filename='])
	except getopt.GetoptError, err:
	    print str(err)
	    usage()
	    sys.exit(2)
	for o,a in opts:
	    if o in ('-h','--help'):
		usage()
		sys.exit(1)
	    elif o in ('-f','--filename'):
		filename = a
	    else:
		print'unhandled option'
		sys.exit(3)
	#action_primitives = "./primitives.json"
	primitive_file = open(filename, 'r')
	primitive_dict = json.load(primitive_file)
	primitives = self.decode_dict(primitive_dict)
        ##print"%s" %primitives['properties']
	pass	
    '''
    def decode_dict(self, data):
	rv = {}
	for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self.decode_list(value)
            elif isinstance(value, dict):
                value = self.decode_dict(value)
            rv[key] = value
        return rv

    def decode_list(self, data):
	rv = []
	for item in data:
	    if isinstance(item, unicode):
		item = item.encode('utf-8')
	    elif isinstance(item, list):
		item = self.decode_list(item)
	    elif isinstance(item, dict):
		item = self.decode_dict(item)
	    rv.append(item)
	return rv;
    def usage():
	print"json_test usage:"
	print"-f: action_primitives json file"
	print"-h,--help: print help message."
'''
if __name__ == "__main__":
    print("main module")
    json_decoder = json_decoder() 
    json_decoder.decoder(sys.argv)
'''



    
