class tools():
	# Copied from somewhere to create directories
	def create_folder(self, directory):
	    try:
	        if not os.path.exists(directory):
	            os.makedirs(directory)
	    except OSError:
	    	print("Could not create directory")