import sys,os, time,subprocess,getopt

def get_path(filename):
	"""
	Get specified path
	If not specified, take current directory as path
	"""
	if filename != "":
		return filename
	else:
		filename = "."


def show_help():
	"""
	Show the help string
	"""
	print "This is the Phototime script to manage pictures taken by date"
	print "The list of valid parameters are :"
	print "--ftype=ftype Enter the filetype"
	print "--path=filepath Specify the path to the director containing the pictures"
	print "Invoke this script thus :"
	print "python phototime.py --ftype=filetype --path=filepath\n\n"

def main(argv=None):
	"""
	Main execution flow, get command line options
	"""
	if argv is None:
		argv = sys.argv
	try:
		opts, args = getopt.getopt(sys.argv[1:], "", ["help","ftype=","path="])
	except getopt.error, msg:
		print msg
		show_help()
		sys.exit(2)
	opts = dict(opts)
	if opts.has_key("--help"):
		show_help()
		sys.exit(2)
	try:
		path = get_path(opts['--path'])
	except:
		print "Error in Path"
		show_help()
		sys.exit(2)
	try:
		if(opts['--ftype']==""):
			print "No filetype specified"
			show_help()
			sys.exit(2)
		else:
			ftype = opts['--ftype']
	except KeyError:
		print "No filetype specified"
		show_help()
		sys.exit(2)
	filelist = subprocess.Popen("find " + path + " -name \"*."+ftype+"\"" , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n').split('\n')
	j=1
	for i in filelist:
		try:
			statinfo = os.stat(i)
		except OSError,msg:
			print msg
			show_help()
			sys.exit(2)
		newname= i.rsplit('/',1)[0] +'/'+ time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(statinfo.st_mtime))
		tempnewname =  newname +  ".%s"%(ftype)
		print tempnewname
		if(not os.path.exists(tempnewname)):
			os.renames(i,tempnewname)
			j=1
		else:
			tempnewname = newname + str(j) + ".%s"%(sys.argv[2])
			os.renames(i,tempnewname)
			j+=1

if __name__ == "__main__":
	sys.exit(main())
	


