import sublime
import sublime_plugin
import getpass
import os

class tools():
	def create_folder(directory): # Copied from somewhere to create directories
	    try:
	        if not os.path.exists(directory):
	            os.makedirs(directory)
	        else:
	        	print("[Tools] Directory already exists!")
	    except OSError:
	    	print("[Tools] Could not create directory")

class new_data_pack(sublime_plugin.TextCommand):

	def run(self, edit):
		self.enter_name(edit)

	def enter_name(self, edit):
		sublime.active_window().show_input_panel("Datapack Name: ", "", self.check_name, None, None)

	def check_name(self, pname):
		self.pack_name = pname # Put the name from the arguments into a variable	
		illegal_symbols = ['\\', '/', r':', '*', '?', '"', '<', '>', '|'] # Those symbols can't be in the pack name
		illegal = 0

		# Check if the name is valid (Not empty and no illegal symbols)
		if self.pack_name is not "":	
			# See if the name contains any of the illegal symbols
			for i in range(0, len(illegal_symbols)):
				if illegal_symbols[i] in self.pack_name:

					# Illegal symbol found! Stop the loop and flag it as illegal
					illegal = 1
					illegalindex = i
					break

			if not illegal: # Check if the name is valid

				self.pack_dir = "C:/Users/" + getpass.getuser() + "/Documents/Datapacks/" + self.pack_name

				if not self.pack_dir[len(self.pack_dir) - 1] is " ":
					if not os.path.exists(self.pack_dir):
						self.create_data_pack()

					else: # Pack already exists
						sublime.error_message("[MinecraftTools] Error: Datapack " + self.pack_name + " gibt es bereits!");

				else: # Name has an empty character at the end
					sublime.error_message("[MinecraftTools] Error: Last character cannot be empty!!")
				
			else: # Name has illegal characters
				sublime.error_message("[MinecraftTools] Error: Name contains illegal symbol " + illegal_symbols[illegalindex]);
		
		else: # Name is empty
			sublime.error_message(" [MinecraftTools] Error: Name cannot be empty!")

	# Create the actual pack
	def create_data_pack(self):

		# Creating the package folder
		tools.create_folder(self.pack_dir)

		# Creating the pack.mcmeta file
		file = open(self.pack_dir + "/pack.mcmeta", "w")
		file.write('{ "pack": { "description": "' + self.pack_name + '", "pack_format": 1 }}')
		file.close()
		sublime.message_dialog("[MinecraftTools] Success! Datapack created in " + self.pack_dir)

		# Opening explorer in the right directory
		os.system("@echo off")
		os.system("start explorer " + self.pack_dir)

		# Creating datapack structure
		tools.create_folder(self.pack_dir + "/data")
