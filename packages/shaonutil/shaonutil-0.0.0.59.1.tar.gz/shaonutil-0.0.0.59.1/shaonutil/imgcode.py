"""BarCode"""
#https://note.nkmk.me/en/python-pillow-qrcode/
#https://www.barcodefaq.com/best-to-use/
#https://www.barcodefaq.com/wp-content/uploads/2018/10/Barcoding4Beginners.pdf
#from barcode import EAN8,Code128,Code39
# encode,decode,display,actual_data,make_barcode_matrix
try:
    reduce
except NameError:
    from functools import reduce
#from io import BytesIO
from barcode.writer import ImageWriter
from imutils.video import VideoStream
from barcode import __BARCODE_MAP
from imutils.video import FPS
from pyzbar import pyzbar
from PIL import Image
import numpy as np
import shaonutil
import barcode
import imutils
import qrcode
import time
import sys
import cv2
import PIL
import os



def calculate_checksum(data):
    """Calculates the checksum for EAN13-Code / EAN8-Code return type: Integer"""
    def sum_(x, y):
        return int(x) + int(y)

    evensum = reduce(sum_, data[-2::-2])
    oddsum = reduce(sum_, data[-1::-2])
    return (10 - ((evensum + oddsum * 3) % 10)) % 10

def verify_data(data):
	"""Verify the EAN encoded data"""
	verification_digit = int(data[-1])
	check_digit = data[:-1]
	return verification_digit == calculate_checksum(check_digit)

def actual_data(decodedObjects):
	"""Returns data without checksum digit for EAN type"""
	if len(decodedObjects) > 0:
		obj = decodedObjects[0]
		data = obj.data.decode('ascii')
	else:
		return False

	if 'ean' in obj.type.lower():
		if verify_data(data):
			return data[:-1]
		else:
			return False
	else:
		return data


def encode(type_,file_,data,rt='FILE'):
	"""Encode the data as barcode or qrcode"""
	# rt = 'OBJ'
	__BARCODE_MAP['qrcode'] = ''
	if not type_.lower() in __BARCODE_MAP:
		raise ValueError("BarCode Type invalid")
	"""
	if type_ == 'EAN8':
		
		# print to a file-like object:
		#rv = BytesIO()
		#EAN8(str(1708929), writer=ImageWriter()).write(rv)
		
		# or sure, to an actual file:
		with open(file_, 'wb') as f:
		    EAN8(data, writer=ImageWriter()).write(f)
	elif type_ == 'Code128':
		with open(file_, 'wb') as f:
		    Code128(data, writer=ImageWriter()).write(f)
	elif type_ == 'Code39':
		with open(file_, 'wb') as f:
		    Code39(data, writer=ImageWriter()).write(f)
	elif type_ == 'qrcode':

		qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=10,
		    border=4,
		)
		qr.add_data(data)
		qr.make(fit=True)

		img = qr.make_image(fill_color="black", back_color="white")
		img.save(file_)
	"""

	if type_ == 'qrcode':

		qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=10,
		    border=4,
		)
		qr.add_data(data)
		qr.make(fit=True)

		img = qr.make_image(fill_color="black", back_color="white")
		if  rt == 'OBJ':
			return img
		else:
			img.save(file_)
			return file_
	else:
		#ean = barcode.get('ean13', '123456789102', writer = barcode.writer.ImageWriter())
		#print(type(ean))
		
		bar_class = barcode.get_barcode_class(type_)
		#bar_class.default_writer_options['write_text'] = False
		bar_class.default_writer_options['text_distance'] = .5
		bar_class.default_writer_options['quiet_zone'] = 1.8
		bar_class.default_writer_options['module_height'] = int(15/1.1)
		
		writer=ImageWriter()
		bar = bar_class(data, writer)
		#print(type(bar))
		to_be_resized = bar.render()
		#bar.save('temp')
		#to_be_resized = Image.open('temp.png')
		del bar

		width,height = to_be_resized.size
		width = int(width/1.2)
		newSize = (width, height)
		resized = to_be_resized.resize(newSize, resample=PIL.Image.NEAREST)
		
		
		if  rt == 'OBJ':
			if os.path.exists(file_): os.remove(file_)
			return resized
		else:
			resized.save(file_)
			return file_

		



	
def decode(infile,log=False):
	"""Decode barcode or qrcode"""
	if type(infile) == str:
		im = cv2.imread(infile)
	elif type(infile) == np.ndarray:
		im = infile

	data = False
	# Find barcodes and QR codes
	decodedObjects = pyzbar.decode(im)

	# Print results
	for obj in decodedObjects:
		if log: print('Type : ', obj.type)
		if log: print('Data : ', obj.data,'\n')
    
	return decodedObjects


def markBarcode(im, decodedObjects):
	"""Mark and show the detected barcode"""
    # Loop over all decoded objects
	for decodedObject in decodedObjects: 
		points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
		if len(points) > 4 : 
			hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
			hull = list(map(tuple, np.squeeze(hull)))
		else : 
			hull = points;

        # Number of points in the convex hull
		n = len(hull)

        # Draw the convext hull
		for j in range(0,n):
			cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

	return im

def make_barcode_matrix(type_,unique_ids,row_number,column_number,filename):
	"""Make barcode matrix image"""
	print("Making "+str(row_number)+"x"+str(column_number)+" BarCode Matrix ...")

	if not len(unique_ids) == row_number * column_number:
		raise ValueError("number of ids not equal to row x column size")
    
	
	TwoDArray = np.array(unique_ids).reshape(row_number,column_number)
	column_img = []
	for row_ids in TwoDArray:
		row_img  = [encode(type_,'',row_ids[i],rt='OBJ') for i in range(column_number)] 
		row_concatenated_img = shaonutil.image.merge_horizontally(row_img)
		column_img.append(row_concatenated_img)

	shaonutil.image.merge_vertically(column_img,filename)

	print("Exported "+str(row_number)+"x"+str(column_number)+" BarCode Matrix as "+filename)

def read_live_barcode(detection_threshold = 50):
	"""Live read the barcode and returns data"""
	##detection_threshold = 50 # 1 sec
	##detection_threshold = 100 # 2 sec

	detection_time = 'no detection'

	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	# vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# start the FPS counter
	fps = FPS().start()

	counter_i = 0
	# loop over frames from the video file stream
	previous_data = None
	while True:
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		
		# convert the input frame from (1) BGR to grayscale (for face
		# detection) and (2) from BGR to RGB (for face recognition)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		im = gray
		
		decodedObjects = decode(im,log=True)
		frame = markBarcode(frame, decodedObjects)
		data = actual_data(decodedObjects)

		# draw the predicted face name on the image
		#cv2.rectangle(frame, (left, top), (right, bottom),	(0, 255, 0), 2)
		#y = top - 15 if top - 15 > 15 else top + 15
		#cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

		# display the image to our screen
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == 27:
			break

		# update the FPS counter
		fps.update()

		#barcode detection program
		if data:
			if previous_data == data:
				if counter_i == 1: start_time = time.time()
				counter_i += 1
			else:
				counter_i = 0
		previous_data = data

		if counter_i > detection_threshold:
			detection_time = time.time() - start_time
			break
		

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	
	message = data
	return message, detection_time

	