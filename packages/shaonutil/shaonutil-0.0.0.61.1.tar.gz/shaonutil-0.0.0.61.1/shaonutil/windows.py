"""Windows"""
from psutil import AccessDenied as AccessDeniedError
import ctypes, sys
import os

import inspect, os
	

def is_winapp_admin():
	"""If the windows app is running with Administrator permission"""
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

def get_UAC_permission():
	"""Get Windows User Account Control Permission for the executing file. If already executing file has admin access, do not ask for permission."""
	# previous param: func
	
	if is_winapp_admin():
		# Code of your program here
		#func() # previously
		print("The executing file already has admin access.")
		pass
	else:
		# Re-run the program with admin rights
		

		# the file which imports and execute others or parent running file
		executing_script = sys.argv[0] # previously __file__ which caused error """Don't work without locally defining in the working file"""
		pathname = os.path.dirname(executing_script)
		executing_script_full_path = os.path.join( os.path.abspath(pathname) ,executing_script)
		rest_params = sys.argv[1:]
		final_arg_list_unfiltered = [executing_script_full_path] + rest_params
		# print(#os.getcwd())
		# print(executing_script)
		# print(sys.argv)
		# print('running from %s' % os.path.abspath(pathname))
		# print(pathname)
		#print('file is %s' % executing_script)
		

		"""
		#To test if the current module is imported
		try:
			module = sys.modules['shaonutil.windows']
			# print("imported")
			
		except KeyError:
			print("not import")
			__file__
		"""
		"""
		sys.argv[0] = [executing_script_full_path]
		executing_script_full_path = " ".join(sys.argv)
		"""
		
		
		# adding quot before and after of param containting spaces
		final_arg_list = ['"' + path_elem + '"' if " " in path_elem else path_elem for path_elem in final_arg_list_unfiltered]
		final_arg_str = " ".join(final_arg_list)
		#print(final_arg_list)
		#quit()
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, final_arg_str , None, 1)