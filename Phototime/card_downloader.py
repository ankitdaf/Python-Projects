import dbus,os,subprocess,time,gobject
from sys import exit as exit

class CanonListener:
	"""
	An implementation of a DBus Signal Listener
	Listens to Device Added signals sent by HAL over DBus
	Copies my files if its one of my predefined MMC cards
	A lot of help was taken from http://stackoverflow.com/questions/469243/how-can-i-listen-for-usb-device-inserted-events-in-linux-in-python
	"""
	
	def __init__(self):
		"""
		Get the system bus and the HAL manager Proxy object
		"""
		self.system_bus = dbus.SystemBus()
		self.hal_manager_obj = self.system_bus.get_object("org.freedesktop.Hal","/org/freedesktop/Hal/Manager")	# Needs HAL libraries installed
		self.hal_manager = dbus.Interface(self.hal_manager_obj,"org.freedesktop.Hal.Manager")
		self.hal_manager.connect_to_signal("DeviceAdded", self.is_card)
		self.uuid="0101-0014"	# Enter your card UUID here
		self.user_password="your_password"	# BE EXTREMELY CAREFUL here, its your sudoers password in plaintext
		self.path="/media/C/Ankit/Photolog/Temp/"		# The path you want the photos to be copied to

	def is_card(self,udi):
		"""
		Check if the device plugged in is a memory card / pen drive
		"""
		device_obj = self.system_bus.get_object ("org.freedesktop.Hal", udi)
		device = dbus.Interface(device_obj, "org.freedesktop.Hal.Device")
		if device.QueryCapability("volume"):
			return self.copy_files(device)

	def get_uuid(self,volume):
		"""
		Get the uuid of the card/drive
		Useful if you dont want to copy everything off every card or pen drive
		This function will get the uuid, just copy it into the uuid variable for this class
		"""
		uuid = volume.GetProperty("volume.uuid")
		return str(uuid)
		
	def copy_files(self,volume):
		"""
		Get the details of the card, check if it is mine,and copy files
		More properties of the volume for adding filters and features can be utilised
		Check out the full HAL volume specifications here :
		http://www.marcuscom.com/hal-spec/hal-spec.html
		"""
		copy_from=[]
		device_file = volume.GetProperty("block.device")
		label = volume.GetProperty("volume.label")
		if not("CANON" in label):		# Just to copy files only from CANON camera MMC cards
			exit(2)
		mounted = volume.GetProperty("volume.is_mounted")
		self.uuid = self.get_uuid(volume)
		if not mounted:
			mountpath="/media/"+self.uuid	# Ensures our mount point is always unique
			try:
				result = subprocess.Popen("echo " + self.user_password + " | sudo -S mkdir -p " + mountpath , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n')
				result = subprocess.Popen("sudo mount " + device_file + " " + mountpath , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n')
				for a,b,c in os.walk(mountpath):
					copy=False
					for j in c:
						if (("JPG" in j) or ("MOV" in j)):
							copy=True
							break
					if copy:
						copy_from.append(a)
				for i in copy_from:
					result = subprocess.Popen("cp -r " + i + " " + self.path , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n')
					result = subprocess.Popen("echo " + self.user_password + " | sudo -S rm -rf " + i , shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n')
				time.sleep(2)	# Necessary for the I/O operations to complete
				result = subprocess.Popen("echo " + self.user_password + " | sudo -S umount " + device_file, shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n')
				result = subprocess.Popen("echo " + self.user_password + " | sudo -S rmdir " + mountpath, shell=True,stdout=subprocess.PIPE, cwd=None).stdout.read().strip('\n')
			except Exception as e:
				print e

if __name__ == '__main__':
	from dbus.mainloop.glib import DBusGMainLoop
	DBusGMainLoop(set_as_default=True)
	loop = gobject.MainLoop()
	CanonListener()
	loop.run()