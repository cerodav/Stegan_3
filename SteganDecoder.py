import cImage as image
import os
import math
import argparse
import sys
from random import randint

class SteganDecoder(object):


	def __init__(self, imagesource = None, key= None):

		
		if imagesource == None :
			sys.exit("\n## Error : Image source location not specified \n")

		if not self.valid(imagesource, 0) :
			sys.exit("\n## Error : Invalid image source\n")

		self.imagesource = imagesource
		self.key = key


	def valid(self, sourcelocation, type) :

		if (not os.path.exists(sourcelocation)) :
			return False
		
		if type == 1 :
			if os.stat(sourcelocation).st_size == 0 :
				return False
			
		return True


	def desteganize(self):

		img = image.Image(self.imagesource)
		imgHeight = img.getHeight()
		imgWidth = img.getWidth() 

		headerHeight = math.floor(imgHeight/10)

		if self.key :
			adder_list = []
			for digit in str(self.key) :
				adder_list.append(int(digit))

		retrRunLen = []
		for row in range(1,2) :

			for col in range(1,5) :

				pixel = img.getPixel(col,row)
				pixR = pixel.getRed()
				pixG = pixel.getGreen()
				pixB = pixel.getBlue()

				binaryStrR = format(pixR,'#10b')[2:]
				binaryStrG = format(pixG,'#10b')[2:]
				binaryStrB = format(pixB,'#10b')[2:]
				
				listStrR = list(binaryStrR)
				listStrG = list(binaryStrG)
				listStrB = list(binaryStrB)

				retrRunLen.append(listStrR[6])
				retrRunLen.append(listStrR[7])
				retrRunLen.append(listStrG[6])
				retrRunLen.append(listStrG[7])
				retrRunLen.append(listStrB[6])
				retrRunLen.append(listStrB[7])		

		binaryStr = ''.join(retrRunLen)
		
		retrRunLen = int(binaryStr,2)
		runLen = retrRunLen

		#print(runLen)

		if self.key :
			count = 0
			adder_list_size = len(adder_list)
		else :
			count = 0
			adder_list_size = 1
			adder_list = []
			adder_list.append(0)

		runData=[]
		
		sys.stdout.write('## Status : Extracting ...\n')
		
		for row in range(int(headerHeight+1),int(imgHeight-1)) :

			for col in range(1,imgWidth-1) :

				if runLen > 0 :

					pixel = img.getPixel(col,row)
					pixR = pixel.getRed()
					pixG = pixel.getGreen()
					pixB = pixel.getBlue()

					binaryStrR = format(pixR,'#10b')[2:]
					binaryStrG = format(pixG,'#10b')[2:]
					binaryStrB = format(pixB,'#10b')[2:]


					
					listStrR = list(binaryStrR)
					listStrG = list(binaryStrG)
					listStrB = list(binaryStrB)

					node={}
					node['runlength'] = (int(listStrR[6]) * 8) + (int(listStrR[7]) * 4) + (int(listStrG[6]) * 2) + (int(listStrG[7]) * 1) - adder_list[count]
					node['value'] = listStrB[7]

					#print(node['runlength'])
					#print(node['value'])
					#print("\n")

					runData.append(node)
					runLen = runLen - 1
					if count + 1 < adder_list_size :
						count = count + 1


		runDataSimplified=[]

		sys.stdout.write('## Status : Decoding ...\n')

		#print(*runData, sep='\n') 

		for idx in range(0,len(runData)) :
			for i in range(0,runData[idx]['runlength']) :
				runDataSimplified.append(runData[idx]['value'])

		#print(len(runDataSimplified))

		idx = 0
		#print("Length of string : %d runData: %d" % (len(runDataSimplified),len(runData)))
		sys.stdout.write('## Status[Complete] Encrypted message : ')
		while idx < len(runDataSimplified) :
			x = []
			#x.append('0')
			#x.append('b')
			try :
				for i in range(0,7) :
					x.append(runDataSimplified[idx + i])
			except IndexError :
				sys.exit("\n!! Error : Invalid data or corrupted data \n")					

			b_string = ''.join(x)
			sys.stdout.write('%c' % int(b_string,2))
			idx = idx + 7


	def run(self):

		self.desteganize()


def main() : 
	try:
		parser = argparse.ArgumentParser(description = "Encodes textual data into images")
		parser.add_argument('Image_Source',help = 'The location containing the image file')
		parser.add_argument('Key',nargs = '?', default = None,help = 'Key for decoding purpose')
		
		args = parser.parse_args()

		stegan_obj = SteganDecoder(args.Image_Source, args.Key)
		stegan_obj.run()

	except KeyboardInterrupt:
		sys.exit("\nProgram was closed by user\n")

if __name__=='__main__':
	main()





