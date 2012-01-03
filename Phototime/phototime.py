import sys
import os, time
import subprocess

path = sys.argv[1]
ftype = "/*." + sys.argv[2]	# I can't believe I was too lazy to add this line before ;)
dirlist = []
dirlist.append('.')		# This is to ensure that the main cause is not lost in the melee

# A loop to get all the directories in the current directory
# Works only for 1 level right now. No whitespaces in directory name please
# Should have been recursive, but I am too sleepy right now
# Will do it later

for i in os.listdir(path):
	if not(os.path.isfile(path+i)):
		dirlist.append("./" + i)
print dirlist
# Unleash the hounds on those wretched filepaths, I say

for i in dirlist:
	# os.listdir(path) Add this for nested directories later + 
	filelist = subprocess.Popen("ls " + i + ftype , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n').split('\n')
	for j in filelist:
		try:
			statinfo = os.stat(j)
		except OSError:
			continue
		newname= time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(statinfo.st_mtime)) + ".%s"%(sys.argv[2])  #FIXED THIS LINE.
		os.renames(j,i+"/"+newname)

# And someone once said "What's in a name" .. Hah, in your face !!
