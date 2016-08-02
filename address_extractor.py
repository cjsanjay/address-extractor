import json
import sys
import re
from sets import Set
import time 




"""
Keywords: contains list of all the addresses type that we want to use for processing.
"""

keywords=["avenue","blvd","boulevard","pkwy","parkway","street","st","rd","road","drive","lane","alley","ave"]		

#phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})')

cleaningLevel=4

def verifyAddress(text_string):
	flag=True
	for each_word in text_string.split(" "):
		if len(each_word)>0 and each_word not in keywords:
			return True
	return False

def cleanAddress(text_string,level):
	if level>0:
		#Slicing from 'location' word in found adddress	
		pos=text_string.find('location')
		if pos >-1:
			text_string=text_string[pos+len('location'):]

	if level>1:
		#Slicing from phone number reference word in found adddress to end
		m=phonePattern.search(text_string)
		if m!=None:			
			pos=m.span()[1]
			text_string=text_string[pos:]

	if level>2:
		#Cleaning if maps URL present
		if text_string.find('maps.google.com') >-1 or text_string.find('=')>-1:
			pos=text_string.rfind('=')
			if pos >-1:
				text_string=text_string[pos+1:].replace('+',' ')

	if level>3:
		#Cleaning if special symbols are present in found address		
		text_string=re.sub('[^a-zA-Z0-9.\- \n\.]', '', text_string)				

	return text_string.strip()

def getNum(text,start,dist):
	end=start+1
	flag=0
	while start >0 and end-start <=dist and text[start]!='\r' and text[start]!='\n':
		if text[start].isdigit() and (start-1==0 or text[start-1]==" " or text[start-1]=="\n" or text[start-1]==">" or text[start-1]==")"):
			flag=1
			break;
		start=start-1	
	return flag,start

def getNumNext(text,end,dist):
	start=end
	flag=0
	count=0
	while end <len(text)-2 and end-start <=dist and text[start]!='\r' and text[start]!='\n':		
		if text[end].isdigit():
			count+=1		
		if count==5 and text[end+1].isdigit() and (end+1==len(text)-2 or text[end+1]==" " or text[end+1]=="\n" or text[end+1]=="<"):
			flag=1
			break;
		end=end+1	
	return flag,end+1	

def getSpace(text,start):
	while start >0:
		if text[start-1]==" ":			
			break;
		start=start-1
	return start

def extractAddress(text,p,type1,addresses):	
	end=-1	
	m=p.search(text.lower())
	if m!=None:
		end=m.span()[0]+len(type1)+1
	if end !=-1:
		flag=1
		flag,bkStart=getNum(text,end-(len(type1)+1),50)		
		if flag==0:
			start=getSpace(text,end-(len(type1)+2))
		elif flag==1:
			flag,start=getNum(text,bkStart-1,10)
			#print (flag, text[start:end])
			if flag==0:
				start=bkStart
		flag,newEnd=getNumNext(text,end,25)
		if flag:
			end=newEnd
		temp=cleanAddress(text[start:end].lower(),cleaningLevel)	
		if verifyAddress(temp):
			addresses.add(temp)
		m=p.search(text.lower(),end)
		if m!=None:
			addresses=extractAddress(text[end:],p,type1,addresses)
		return addresses
	return addresses	
#extractAddress("<BR />=?=?=  Table Shower available  =?=?=<br><br>?=Let us make you stress free one day at a time=?<br><br>=?= PUENTE Spa=?= <br><br>TEL:  626-338-8809  <br><br>  1832 Puente Ave. Baldwin Park, CA. 91706  <br><br>Clean Shower Included With Session<br><br>we always hiring beautiful ladies<br><br> Open- 9:00 AM to 9:30 PM<br>	</div>")		


def processFile(input_file_name,keywords,finalAddressData):
	input_data=""
	with open(input_file_name) as data_file:
		input_data=json.load(data_file)	
	extracted_address=[]
	for each_type in input_data:
		for each_a in input_data[each_type]:
			temp={}
			temp["input"]=each_a
			addresses=Set()
			for each_keyword in keywords:
				p = re.compile(r'\b%s\b' % each_keyword.lower(), re.I)
				m=p.search(each_a.lower())
				if m!=None:
					addresses=extractAddress(each_a,p,each_keyword,addresses)			
			temp["address"]=list(addresses)		
			finalAddressData.append(temp)

"""
Input: Text String
Output: Json object containing input text string with list of associated present addresses

Uses default keywords embedded in script file
"""
def getAddressFromString(text_string):
	temp={}
	temp["input"]=text_string
	addresses=Set()
	for each_keyword in keywords:		
		p = re.compile(r'\b%s\b' % each_keyword.lower(), re.I)
		m=p.search(text_string.lower())	
		if m!=None:
			extractAddress(text_string,p,each_keyword,addresses)
	temp["address"]=list(addresses)		
	return temp

"""
Input: Text String and keyword python list ex: ["ave","street"] etc.
Output: Json object containing input text string with list of associated present addresses

Uses keywords list passed as an parameter
"""
def getAddressFromStringType(text_string,keywords):
	temp={}
	temp["input"]=text_string
	addresses=Set()
	for each_keyword in keywords:	
		p = re.compile(r'\b%s\b' % each_keyword.lower(), re.I)
		m=p.search(text_string.lower())
		if m!=None:			
			extractAddress(text_string,p,each_keyword,addresses)
	temp["address"]=list(addresses)		
	return temp	

"""
Input: File name and keyword python list ex: ["ave","street"] etc.
Output: Json object containing list of all input text strings with list of associated present addresses
"""
def getAddressFromFile(file_name,keywords):
	finalAddressData=[]	
	processFile(file_name,keywords,finalAddressData)
	return finalAddressData

if __name__ == '__main__':
	startTime = time.time()
	finalAddressData=[]
	processFile(sys.argv[1],keywords,finalAddressData)
	outputFile=open(sys.argv[1].split(".")[0]+"_out.txt","w")
	json.dump(finalAddressData,outputFile,sort_keys=False,indent=2)	
	outputFile.close()
	print ("Output File: ",sys.argv[1].split(".")[0]+"_out.txt")
	print ('Took {0} second !'.format(time.time() - startTime))
	#print getAddressFromStringType("Very passable black 25 year young TS girl with the best of the best! 9193959158 hosting off Western Boulevard NCstate area I'm waiting! 20-40 $pecial$",["boulevard"])