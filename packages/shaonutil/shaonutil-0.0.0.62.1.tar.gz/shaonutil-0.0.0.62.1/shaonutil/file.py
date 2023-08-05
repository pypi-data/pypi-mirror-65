"""File"""
from pip._internal import main as pipmain
from os.path import dirname, basename, isfile, join
import json,codecs,configparser,subprocess,platform,os,glob,shaonutil,pickle,importlib,pip

def get_module_path(module):
	return module.__file__
	
def get_all_dirs():
    return [basename(file_) for file_ in glob.glob(join(os.getcwd(), "*")) if  os.path.isdir(file_) and not '..' in file_]
def get_all_files_dirs():
    return [basename(file_) for file_ in glob.glob(join(os.getcwd(), "*")) if not '..' in file_]

def package_exists(package_name):
	"""check if a python pcakage exists."""
	
	spam_spec = importlib.util.find_spec(package_name)
	found = spam_spec is not None
	return found


def pip_install(package_name):
	failed = pipmain(['-m','install', package_name])
	return failed

def get_all_functions(object):
	"""shaonutil.file.get_all_functions(object/file/class)"""
	return [func for func in dir(object) if callable(getattr(object, func))]

def ConfigSectionMap(Config, section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

class CaseConfigParser(configparser.SafeConfigParser):
    def optionxform(self, optionstr):
        return optionstr

def read_configuration_ini(filename):
	config = configparser.ConfigParser()
	config.readfp(codecs.open(filename, "r", "utf8"))
	return config

def read_safecase_configuration_ini(filename):
	config = CaseConfigParser()
	config.readfp(codecs.open(filename, "r", "utf8"))
	return config

def write_configuration_ini(configs_par,filename, f_mode='w'):
	with open(filename, f_mode) as configfile:    # save
		configs_par.write(configfile)

def read_json(filename):
	"""Read JSON file and return dictionary"""
	with codecs.open(filename, "r", encoding="utf-8") as fp:
		data = json.load(fp)
	#Print Formatted Dictionary
	#print(json.dumps(data, indent=4))
	return data

def write_json(obj,filename):
	"""Write JSON file"""
	with codecs.open(filename, "w", encoding='utf-8') as fp:
	    json.dump(obj, fp, indent=1)

def read_file(filename):
	"""Read File and return lines as list"""
	if os.path.exists(filename):
		with codecs.open(filename, "r", encoding="utf-8") as file_reader:
			lines = file_reader.readlines()

		ill_chars = ['\r','\n']
		_ = []
		for line in lines:
			for ic in ill_chars:
				line = line.replace(ic,'')
			_.append(line)
		filtered_lines = _
		return filtered_lines
	else:
		return False

def write_file(filename, strs,mode="w"):
	"""Write File from string"""
	with codecs.open(filename, mode, encoding='utf-8') as file_appender:
		file_appender.writelines(strs)

def read_pickle(filename):
	# Unpickling
	with open(filename, "rb") as fp:
		unpickler = pickle.Unpickler(fp)
		b = unpickler.load(fp)
	return b

def write_pickle(filename, obj_):
	with open(filename, "wb") as fp:   #Pickling
		pickle.dump(obj_, fp)


def open_file_with_default_app(filepath):
	if platform.system() == 'Darwin':       # macOS
	    subprocess.call(('open', filepath))
	elif platform.system() == 'Windows':    # Windows
	    os.startfile(filepath)
	elif platform.system() == 'Windows':    # Windows
		subprocess.call(('xdg-open', filepath))
	else:                                   # linux variants
	    subprocess.call(('xdg-open', filepath))

def get_last_file_of_dir(filename):
	list_of_files = glob.glob(filename)
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file

def remove_duplicateLines_from_file(filename):
	lines = shaonutil.file.read_file(filename)
	lines_seen = set() # holds lines already seen

	for line in lines:
		if line not in lines_seen: # not a duplicate
			lines_seen.add(line)

	strs = '\n'.join(lines_seen)
	shaonutil.file.write_file(filename, strs)

if __name__ == '__main__':
	pass