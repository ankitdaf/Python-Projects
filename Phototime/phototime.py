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
	print "--pre=string Specify a string which will be prefixed to each filename (optional) "
	print "--post=string Specify a string which will be postfixed to each filename (optional) "
	print "Invoke this script thus :"
	print "python phototime.py --ftype=filetype --path=filepath --pre=optional_string --post=optional_string\n\n"

def rename_using(path,ftype,pre="",post=""):
	"""
	Rename files according to creation date in meta-data.
	For SLRs which can click multiple pictures per second,
	an extra index is suffixed to prevent overwriting
	Takes path of the folder, the specific filetype to be renamed
	and optional prefix and postfixes
	"""
	filelist = subprocess.Popen("find " + path + " -name \"*."+ftype+"\"" , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n').split('\n')
	j=1
	for i in filelist:
		try:
			statinfo = os.stat(i)
		except OSError,msg:
			print msg
			show_help()
			sys.exit(2)
		# Added prefix here, tricky
		newname= i.rsplit('/',1)[0] +'/'+ pre + time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(statinfo.st_mtime))
		# Added postfix here
		tempnewname = newname + post +  ".%s"%(ftype)
		print tempnewname
		if(not os.path.exists(tempnewname)):
			os.renames(i,tempnewname)
			j=1
		else:
			if (pre in tempnewname) and (post in tempnewname):
				# The files have already been renamed, there's nothing to do here
				continue
			tempnewname = newname + str(j) + post + ".%s"%(ftype)
			os.renames(i,tempnewname)
			j+=1


def main(argv=None):
	"""
	Main execution flow, get command line options
	"""
	if argv is None:
		argv = sys.argv
	#Get command line arguments
	try:
		opts, args = getopt.getopt(sys.argv[1:], "", ["help","ftype=","path=","pre=","post="])
	except getopt.error, msg:
		print msg
		show_help()
		sys.exit(2)
	# Convert the arguments into a dictionary to make life easier
	opts = dict(opts)
	# Show help 
	if opts.has_key("--help"):
		show_help()
		sys.exit(2)
	# Check for valid path
	try:
		path = get_path(opts['--path'])
	except:
		print "Error in Path"
		show_help()
		sys.exit(2)
	# Check for valid filetype
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
	# Append prefix string here
	try:
		if(opts['--pre']==""):
			pre=""
		else:
			pre=opts['--pre']
	except KeyError:
		pre=""
	# Append postfix string here
	try:
		if(opts['--post']==""):
			post=""
		else:
			post=opts['--post']
	except KeyError:
		post=""
	# Actual file renaming happens here
	rename_using(path,ftype,pre,post)

if __name__ == "__main__":
	sys.exit(main())