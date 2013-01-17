from bluetooth import * # I wasn't looking for this, but now you're in my way

logfile = file("gps_log.txt","w") # Hey I just met you
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  #  and this is crazy
gt_750_bt = ("11:22:33:44:6D:3D",1) # But here's my number
sock.connect((bt,port)) # So call me maybe

while 1:  # Chorus
    of.write(sock.recv(38400))  # It's hard to look right, at you baby
    of.write('\n')  # And all the other boys, try to chase me

logfile.close()
