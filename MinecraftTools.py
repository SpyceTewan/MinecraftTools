import sublime, sublime_plugin, getpass, os

class new_data_pack(sublime_plugin.TextCommand):

	# The function that starts the whole thing
	def run(self, edit):
		self.enter_name()

	# Opens an input to enter the pack name
	def enter_name(self):
		sublime.active_window().show_input_panel("Datapack Name: ", "", self.create_file, None, None)
	
	# Initiate the data pack creation
	def create_file(self, text):
		self.view.run_command("new_data_pack_create_file", {"args":{"name": text}})

class new_data_pack_create_file(sublime_plugin.TextCommand):
	def run(self, edit, args):

		# Put the name from the arguments into a variable
		self.packname = args["name"]

		# Those symbols can't be in the pack name
		illegal_symbols = ['\\', '/', r':', '*', '?', '"', '<', '>', '|']

		# Check if the name is valid (Not empty and no illegal symbols)
		if self.packname is not "":
			illegal = 0

			# See if the name contains any of the illegal symbols
			for i in range(0, len(illegal_symbols)):
				if illegal_symbols[i] in self.packname:

					# Illegal symbol found! Stop the loop and flag it as illegal
					illegal = 1
					illegalindex = i
					break

			if not illegal: # Check if the name is valid
				self.valid_name()
				
			else: # If illegal symbols in text, you get this error message
				sublime.error_message("[MinecraftTools] Error: Name contains illegal symbol " + illegal_symbols[illegalindex]);
		else: # If the name is empty you get this error message
			sublime.error_message(" [MinecraftTools] Error: Name cannot be empty!")

	# Create the actual pack
	def valid_name(self):

		# Setting the directory for the package 
		dir = "C:/Users/" + getpass.getuser() + "/Documents/Datapacks/" + self.packname
		
		# Creating the package folder
		self.create_folder(dir)

		# Creating the pack.mcmeta file
		file = open(dir + "/pack.mcmeta", "w")
		file.write('{ "pack": { "description": "' + self.packname + '", "pack_format": 1 }}')
		file.close()
		sublime.message_dialog("[MinecraftTools] Success! Datapack created in " + dir)
		print(dir)
		os.system("@echo off")
		os.system("start explorer " + dir)

		# Creating folder structure
		self.create_folder(dir + "/data")


	# Copied from somewhere to create directories
	def create_folder(self, directory):
	    try:
	        if not os.path.exists(directory):
	            os.makedirs(directory)
	    except OSError:
	    	print("Could not create directory")