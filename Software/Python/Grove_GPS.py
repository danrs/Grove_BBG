import Adafruit_BBIO.UART as UART
import serial
import time
import sys
import struct
import math

UART.setup("UART2")

ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
ser.flush()

class GPS:
    # The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
    # Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
    inp=[] #input string
    GGA=[] #parsed data

    #Read data from the GPS
    def read(self):
        while True:
            GPS.inp=ser.readline()
            print GPS.inp
            if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
                break
            time.sleep(0.1)
        try:
            ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))    #Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
            GPS.inp=GPS.inp[ind:]
        except ValueError:
            print ""
        GPS.GGA=GPS.inp.split(",")    #Split the stream into individual parts
        return [GPS.GGA]

    #Split the data into individual elements
    def vals(self):
        time=GPS.GGA[1] #UTC time
        lat=GPS.GGA[2]
        lat_ns=GPS.GGA[3]
        lon=GPS.GGA[4]
        lon_ew=GPS.GGA[5]
        fix=GPS.GGA[6]
        sats=GPS.GGA[7]
        alt=GPS.GGA[9]
        return [time,fix,sats,alt,lat,lat_ns,lon,lon_ew]

g=GPS()
f=open("gps_data.csv",'w')    #Open file to log the data
f.write("name,latitude,longitude\n")    #Write the header to the top of the file
ind=0
while True:
    try:
        x=g.read()    #Read from GPS
        [t,fix,sats,alt,lat,lat_ns,lon,lon_ew]=g.vals()    #Get the individial values
        print "Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",lon,lon_ew
        if lat is not "" and lon is not "":
            s=str(t)+","+str(float(lat)/100)+","+str(float(lon)/100)+"\n"
            f.write(s)    #Save to file
        time.sleep(2)
    except IndexError:
        print "Unable to read"
    except KeyboardInterrupt:
        f.close()
        print "Exiting"
        sys.exit(0)


