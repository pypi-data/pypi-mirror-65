"""Security"""
from uuid import UUID
import os
import string
import random
from file import get_all_files_dirs
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
	# uuid.uuid4() returns UUID(bytes=os.urandom(16), version=4)
	#randomString = uuid.uuid4().hex
	randomString = UUID(bytes=os.urandom(16), version=4).hex
	if 'number' in filters:
		randomString = str(int(randomString,16))
	else:
		randomString = randomString.upper()
	
	randomString  = randomString[0:stringLength]

	return randomString