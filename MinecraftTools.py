import sublime
import sublime_plugin
import getpass
import os
import subprocess

class tools():
	def create_folder(directory): # Copied from somewhere to create directories
	    try:
	        if not os.path.exists(directory):
	            os.makedirs(directory)
	        else:
	        	print("[Tools] Directory already exists!")
	    except OSError:
	    	print("[Tools] Could not create directory")

	def create_file(directory, content):
		file = open(directory, "w")
		file.write(content)
		file.close()

class about_menu(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.message_dialog("Credits \n----------\nPlugin coding etc: Tewan\nTwitter: @spyce_tewan\nYouTube: youtube.com/tewan\n\nDatapack structure & libraries: Halbzwilling\nTwitter: @Halbzwilling\nYouTube: youtube.com/halbzwilling")

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

				self.pack_dir = "C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/datapacks/" + self.pack_name

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
			sublime.error_message("[MinecraftTools] Error: Name cannot be empty!")

	# Create the actual pack
	def create_data_pack(self):

		# Creating the package folder
		tools.create_folder(self.pack_dir)

		# Creating the pack.mcmeta file
		tools.create_file(self.pack_dir + "/pack.mcmeta", '{ "pack": { "description": "' + self.pack_name + '", "pack_format": 1 }}')

		# Creating datapack structure
		data_dir = self.pack_dir + "/data/"
		data_namespace = data_dir + self.pack_name

		# Creating tags in minecraft namespace
		tools.create_folder(data_dir + "minecraft/tags/functions")
		tools.create_file(data_dir + "minecraft/tags/functions/load.json", '{ "values": ["' + self.pack_name + ':init"] }')
		tools.create_file(data_dir + "minecraft/tags/functions/tick.json", '{ "values": ["' + self.pack_name + ':update"] }')

		# Creating update and init under package namespace
		tools.create_folder(data_dir + self.pack_name + "/functions")
		tools.create_file(data_namespace + "/functions/init.mcfunction", '#This gets executed only one time when the datapack has loaded!')
		tools.create_file(data_namespace + "/functions/update.mcfunction", '#This gets executed every tick after initializing!')

		# Creating shapeless and shaped templates
		tools.create_folder(data_namespace + "/recipes")
		tools.create_file(data_namespace + "/recipes/shaped.json", '{\n  "type": "crafting_shaped",\n"pattern": [\n    "# #",\n    " # ",\n    "# #"\n  ],\n  "key": {\n    "": {\n      "item": "minecraft:"\n    }\n  },\n  "result": {\n    "item": "minecraft:",\n    "count": 1\n  }\n}')
		tools.create_file(data_namespace + "/recipes/shapeless.json", '{\n  "type": "crafting_shapeless",\n  "ingredients": [{\n    "item": "minecraft:"\n  }],\n  "result": {\n    "item": "minecraft:",\n    "count": 1\n  }\n}')

		## ========	 SUCCESS!! =========	
		sublime.message_dialog("[MinecraftTools] Success! Datapack " + self.pack_name + " has been created")
		
		if sublime.platform() == "windows":
			subprocess.Popen(["C:\Program Files\Sublime Text 3\sublime_text.exe", self.pack_dir], shell=True)