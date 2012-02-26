import sys,os, time,subprocess

path = sys.argv[1]
ftype = sys.argv[2]
filelist = subprocess.Popen("find " + path + " -name \"*."+ftype+"\"" , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n').split('\n')
for i in filelist:
	statinfo = os.stat(i)
	newname= time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(statinfo.st_mtime)) + ".%s"%(sys.argv[2])
	tempnewname = i.rsplit('/',1)[0] +'/'+ newname
	if(not os.path.exists(tempnewname)):
		os.renames(i,tempnewname)
