from piconlib import parse
import toml
import os
# https://stackoverflow.com/a/1994840
import shutil, errno
def copy(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

class SystemTree:
	def __init__(self, map_path):
	 self.path = map_path

	def get_apps(self):
		apps = []
		from os import walk
		f = []
		for (dirpath, dirnames, filenames) in walk(self.path+"/apps_info"):
			f.extend(filenames)
			break
		for app_path in f:
			apps.append(parse.parse_appinfo(self.path+"/apps_info/"+app_path))

	def get_enabled_apps(self):
		f = open(self.path+"/apps_active", "r+")
		apps = f.readlines()
		out = list()
		for app in apps:
			out.append(parse.parse_appinfo(self.path+"/apps_info/"+str.strip(app)+".toml"));
		f.close()
		return out

	def install_app(self, appdir_path):
		info = parse.parse_appinfo(appdir_path+"/app.toml")
		name = info["app"]["name"].lower()
		f = open(self.path+"/apps_info/"+name+".toml", "w+")
		toml.dump(info, f)
		copy(appdir_path+"/app_data", self.path+"/apps/"+name)
		f = open(self.path+"/apps_active", "r+")
		active_apps = f.readlines()
		active_apps = list(map(str.strip, active_apps))
		active_apps.append(name)
		f.seek(0)
		f.write("\n".join(active_apps))
		f.close()

	def remove_app(self, app_name):
		name = app_name.lower()
		shutil.rmtree(self.path+"/apps/"+name)
		os.remove(self.path+"/apps_info/"+name+".toml")
		f = open(self.path+"/apps_active", "r+")
		old_active_apps = f.readlines()
		active_apps = list()
		for app in old_active_apps:
			if (name != app):
				active_apps.append(app)
				print(app)
		
		active_apps = list(map(str.strip, active_apps))
		f.truncate(0)
		f.seek(0)
		f.write("\n".join(active_apps))
		print("\n".join(active_apps))
		f.close()


	#Required when removing and installing applications
	def refresh_apploader(self):
		enabled_apps = self.get_enabled_apps()
		app_count = len(enabled_apps)
		f = open(self.path+"/app_loader.h", "r+")
		f.truncate(0)
		f.seek(0)
		f.write("#ifndef APP_LOADER_H_\n#define APP_LOADER_H_\n")
		f.write("#define APPS_COUNT "+str(app_count)+"\n")
		f.write("""
#include <Arduino.h>
extern String apps_name[];
extern bool apps_hidden[];
""")
		for app in enabled_apps:
			f.write('#include "apps/'+app["app"]["name"].lower()+"/"+app["app"]["main_header"]+'"\n')
		f.write("#endif\n")
		f.close()

		f = open(self.path+"/app_loader.cpp", "r+")
		f.truncate(0)
		f.seek(0)
		f.write(
"""
#include "app_loader.h" 
#include <Arduino.h>
String apps_name[] = {
"""
		)
		for app in enabled_apps:
			f.write('"' + app["app"]["name"] + '",\n')
		f.write("};\n")
		f.write("bool apps_hidden[] = {\n")
		for app in enabled_apps:
			print(app["app"]["name"])
			f.write(str(app["flags"]["hidden"]).lower()+",\n")
		f.write("};\n")
		f.close()
		f = open(self.path+"/app_list.cpp", "r+")
		f.write(
"""
#include "app_loader.h" 
#include "app_list.h" 
#include "api.h" 
void (*apps_loop[])() = {
"""
		)
		for app in enabled_apps:
			f.write(app["functions"]["loop"]+",\n")
		f.write("};\n")
		f.write("void (*apps_init[])() = {\n")

		for app in enabled_apps:
			f.write(app["functions"]["init"]+",\n")
		f.write("};\n")

		f.close()