"""String"""
import string
import random
import pprint
import uuid

def nicely_print(dictionary,print=True):
	"""Prints the nicely formatted dictionary - shaonutil.strings.nicely_print(object)"""
	if print: pprint.pprint(dictionary)

	# Sets 'pretty_dict_str' to 
	return pprint.pformat(dictionary)

def change_dic_key(dic,old_key,new_key):
	"""Change dictionary key with new key"""
	dic[new_key] = dic.pop(old_key)
	return dic

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    for c in range(10):
        letters = letters + str(c)

    return ''.join(random.choice(letters) for i in range(stringLength))

def generateSecureRandomString(stringLength=10):
    """Generate a secure random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits #+ string.punctuation
    return ''.join(secrets.choice(password_characters) for i in range(stringLength))

def generateCryptographicallySecureRandomString(stringLength=10,filters=[]):
	"""Generate a random string in a UUID fromat which is crytographically secure and random"""
	randomString = uuid.uuid4().hex
	if 'number' in filters:
		randomString = str(int(randomString,16))
	else:
		randomString = randomString.upper()
	
	randomString  = randomString[0:stringLength]

	return randomString

if __name__ == '__main__':
	pass