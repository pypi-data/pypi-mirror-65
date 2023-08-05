import toml
import warnings

def parse_appinfo(path: str):
	temp = toml.load(path) # We store the data to parse it and check for errors
	
	# [App]
	if temp.get("app") == None : raise RuntimeError("AppInfo provided does not present required app field")
	if temp.get("app").get("name") == None : raise RuntimeError("AppInfo provided does not present required name key under app field")
	
	# [Functions]
	if temp.get("functions") == None :
		warnings.warn("AppInfo provided does not present a functions field, assuming dummy functions")
		temp["functions"] = {"init" :"dummy_init", "loop" :"dummy_loop"}
	else:
		if temp.get("functions").get("init") == None:
			warnings.warn("AppInfo provided does not present a init function, assuming dummy init")
			temp["functions"]["init"] = "dummy_init"
		if temp.get("functions").get("loop") == None:
			warnings.warn("AppInfo provided does not present a loop function, assuming dummy loop")
			temp["functions"]["loop"] = "dummy_loop"

	return temp