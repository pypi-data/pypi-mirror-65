"""Network"""
from io import StringIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import  shaonutil
import urllib.parse
import re
import requests
import wget
import socket
import sys


def check_port(address='localhost', port=80, log = False):
	# localhost / 127.0.0.1
	# http port 80

    # Create a TCP socket
    s = socket.socket()
    if log: print("Attempting to connect to %s on port %s" % (address, port))
    try:
        s.connect((address, port))
        if log: print("Connected to %s on port %s" % (address, port))
        return True
    except socket.error as  e:
        if log: print("Connection to %s on port %s failed: %s" % (address, port, e))
        return False
    finally:
        s.close()

def urlExist(url):
	"""Check if the file exist in online"""
	res = requests.head(url)
	if res.ok:
		return True
	else:
		return False

def downloadFile(url,filename):
	"""Donwload a file if error occurs returns false"""
	if urlExist(url):
		wget.download(url,filename)
		return True
	else:
		return False

def url_encoding_to_utf_8(url):
	"""url_encoding_to_utf_8(url)"""
	url = urllib.parse.unquote(url)
	return url


def check_valid_url(url):
	regex = re.compile(
	        r'^(?:http|ftp)s?://' # http:// or https://
	        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
	        r'localhost|' #localhost...
	        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
	        r'(?::\d+)?' # optional port
	        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	return re.match(regex, url) is not None


class Email:
	def __init__(self):
		self._authentication = ''

	@property
	def authentication(self):
		## changing the argument values by accesing property via setter methods
		return self._authentication

	@authentication.setter
	def authentication(self, new_value):
		self._authentication = new_value

	def send_email(self,receiver_address,subject,mail_content,attachment_file_link,log=False):
		#The mail addresses and password
		smtp_server = self._authentication['smtp_server']
		smtp_port = self._authentication['smtp_port']
		sender_address = self._authentication['smtp_username']
		sender_pass = self._authentication['smtp_password']

		receiver_address = receiver_address

		#Setup the MIME
		message = MIMEMultipart()
		message['From'] = sender_address
		message['To'] = receiver_address
		message['Subject'] = subject
		#The body and the attachments for the mail
		message.attach(MIMEText(mail_content, 'plain'))
		#Create SMTP session for sending the mail
		session = smtplib.SMTP(smtp_server, smtp_port) #use gmail with port
		session.starttls() #enable security

		try:
			session.login(sender_address, sender_pass) #login with mail_id and password
		except smtplib.SMTPAuthenticationError as e:
			#: (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials j24sm19239050pfi.55 - gsmtp')
			if(log): print('if using gmail smtp, check server host,port\n  if user/pass is not accepeted , turn on less secure app setting and recognize the activity warning mail sent in your gmail, then it will send email in next run.')
			stat_message = str(e)
			return stat_message


		text = message.as_string()
		session.sendmail(sender_address, receiver_address, text)
		session.quit()
		stat_message = 'Mail Sent'
		return stat_message


if __name__ == '__main__':
	pass