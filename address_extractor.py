import json
import sys
from sets import Set

addresses=Set()

def getNum(text,start,dist):
	end=start+1
	flag=0
	while start >0 and end-start <=dist:
		if text[start].isdigit() and (start-1==0 or text[start-1]==" " or text[start-1]=="\n" or text[start-1]==">" or text[start-1]==")"):
			flag=1
			break;
		start=start-1	
	return flag,start

def getNumNext(text,end,dist):
	start=end
	flag=0
	count=0
	while end <len(text)-2 and end-start <=dist:		
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

def extractAddress(text):	
	end=-1	
	if text.lower().find(" ave") !=-1:
		end=text.lower().find(" ave") +4
	if end !=-1:
		flag=1
		flag,bkStart=getNum(text,end-5,50)		
		if flag==0:
			start=getSpace(text,end-5)
		elif flag==1:
			flag,start=getNum(text,bkStart-1,10)
			#print (flag, text[start:end])
			if flag==0:
				start=bkStart
		flag,newEnd=getNumNext(text,end,25)
		if flag:
			end=newEnd		
		#print "Input: ", text
		#print "Extracted: ",text[start:end].replace("\n","")
		addresses.add(text[start:end].lower().replace("\n",""))
		if text[end:].lower().find(" ave")!=-1:
			extractAddress(text[end:])
#extractAddress("<BR />=?=?=  Table Shower available  =?=?=<br><br>?=Let us make you stress free one day at a time=?<br><br>=?= PUENTE Spa=?= <br><br>TEL:  626-338-8809  <br><br>  1832 Puente Ave. Baldwin Park, CA. 91706  <br><br>Clean Shower Included With Session<br><br>we always hiring beautiful ladies<br><br> Open- 9:00 AM to 9:30 PM<br>	</div>")		


def processFile(input_file_name,type1):
	input_data=""
	with open(input_file_name) as data_file:
		input_data=json.load(data_file)	
	extracted_address=[]
	if type1 in input_data:
		for each_a in input_data[type1]:
			extractAddress(each_a)		

if __name__ == '__main__':
	processFile(sys.argv[1],sys.argv[2])
	outputFile=open(sys.argv[1].split(".")[0]+"_out.txt","w")
	json.dump(list(addresses),outputFile,sort_keys=False,indent=2)
	outputFile.close()