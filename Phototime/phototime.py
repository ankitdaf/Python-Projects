import sys,os, time,subprocess

path = sys.argv[1]
ftype = sys.argv[2]
filelist = subprocess.Popen("find " + path + " -name \"*."+ftype+"\"" , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n').split('\n')
j=1
for i in filelist:
	statinfo = os.stat(i)
	newname= i.rsplit('/',1)[0] +'/'+ time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(statinfo.st_mtime))
	tempnewname =  newname +  ".%s"%(sys.argv[2])
	print tempnewname
	if(not os.path.exists(tempnewname)):
		os.renames(i,tempnewname)
		j=1
	else:
		tempnewname = newname + str(j) + ".%s"%(sys.argv[2])
		os.renames(i,tempnewname)
		j+=1
