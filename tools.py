<<<<<<< HEAD
class tools():
	# Copied from somewhere to create directories
	def create_folder(self, directory):
	    try:
	        if not os.path.exists(directory):
	            os.makedirs(directory)
	    except OSError:
=======
class tools():
	# Copied from somewhere to create directories
	def create_folder(self, directory):
	    try:
	        if not os.path.exists(directory):
	            os.makedirs(directory)
	    except OSError:
>>>>>>> 1706c9fc5015676a36b3093c7a1632847bac2504
	    	print("Could not create directory")