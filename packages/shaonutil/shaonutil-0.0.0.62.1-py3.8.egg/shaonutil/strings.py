"""String"""
import pprint


def nicely_print(dictionary,print=True):
	"""Prints the nicely formatted dictionary - shaonutil.strings.nicely_print(object)"""
	if print: pprint.pprint(dictionary)

	# Sets 'pretty_dict_str' to 
	return pprint.pformat(dictionary)

def change_dic_key(dic,old_key,new_key):
	"""Change dictionary key with new key"""
	dic[new_key] = dic.pop(old_key)
	return dic