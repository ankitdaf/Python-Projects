"""

This snippet aims to clean the messy and huge csv files that the Android phones generate
when exporting to a VCF on an SDCard

It provides a set of utilities, each of which is described below

Note : The phone number formatting logic is specific to India, and you may want to change it to suit your needs


 Copyright 2011 Ankit Daftery
 All Rights Reserved

"""


import re

def remove_photos(infile):
	"""
	Remove photos that are stored in plaintext.
	The photos are the major reason for the huge size of the contacts file
	"""
	foo = open(infile,"r")
	lines=foo.readlines()
	foo.close()
	start= re.compile("PHOTO")
	temp = []
	flag = False
	for i in lines:
		if (flag == False):
			if(start.search(i) != None):
				flag = True
				pass
			else:
				temp.append(i)
		elif (flag == True):
			if (i == '\r\n'):
				flag = False
			pass
	foo = open(infile,"w")
	for i in temp:
		foo.write(i)
	foo.close()
	del temp,lines



def remove_addresses(infile):
	"""
	This function removes the addresses that might have been saved or 	
	synced automatically with Social networks. It also removes invalid email
	addresses and web urls which are link to Google profiles
	"""
	p1= re.compile("ADR;")
	p2= re.compile("found]")
	p3 = re.compile("profiles")
	foo = open(infile,"r")
	lines = foo.readlines()
	foo.close()
	temp = []
	for i in lines:
		if (p1.search(i) or p2.search(i) or p3.search(i)):
			pass
		else:
			temp.append(i)
	foo = open(infile,"w")
	for i in temp:
		foo.write(i)
	foo.close()
	del temp,lines
	

def remove_non_fields(infile):
	"""
	This function removes trash fields which might sometimes arise, very subjective
	"""
	foo = open(infile,"r")
	lines = foo.readlines()
	foo.close()
	temp = []
	for i in range(0,len(lines)):
		lines[i]= lines[i].replace('+91','0')
		if (':' in lines[i]):
			temp.append(lines[i])
		else:
			pass	
	foo = open(infile,"w")
	for i in temp:
		foo.write(i)
	foo.close()
	del temp,lines

def remove_non_numbers(infile):
	"""
	Remove all entries which do not have phone numbers
	Very useful if you plan to export Android contacts to 'dumbphones'
	"""
	foo = open(infile,"r")
	lines =  foo.readlines()
	foo.close()
	start= re.compile("BEGIN:")
	stop=re.compile("END:")
	tel=re.compile("TEL;")
	foobar = open(infile,"w")
	temp=[]
	within_contact = False
	has_tel = False
	for i in lines:
		if(within_contact):
			temp.append(i)
			if (stop.search(i)):
				if(has_tel):
					for i in temp:
						foobar.write(i)
				temp = []
				within_contact=False
				has_tel = False
			elif (tel.search(i)):
				has_tel = True
		else:
			if (start.search(i)):
				within_contact = True
				temp.append(i)
	foobar.close()
	del temp,lines	

def cleanup_phones(infile):
	"""
	Cleanup varying formats of all numbers and converge them to a uniform format
	"""
	p=re.compile("[0-9]+-[0-9]+-[0-9]+");
	foo = open(infile,"r")
	lines =  foo.readlines()
	foo.close()
	foobar = open(infile,"w")
	temp=[]
	for i in range(0,len(lines)):
		if(p.search(lines[i])):
			lines[i]=lines[i].replace("-","")
		if(len(lines[i].split(':')[-1]) == 14 and lines[i].split(':')[-1].startswith("91")):
			lines[i] = lines[i].replace(":91",":0")
		foobar.write(lines[i])
	foobar.close()

"""
Sample usage
"""

remove_photos("00003.vcf")
remove_addresses("00003.vcf")
remove_non_fields("00003.vcf")
remove_non_numbers("00003.vcf")
cleanup_phones("00003.vcf")
