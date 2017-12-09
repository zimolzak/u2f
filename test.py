#!/usr/bin/env python2

import sys
sys.path.append('/Library/Python/2.7/site-packages/')
from u2flib_host import u2f, exc
from time import sleep

L = u2f.list_devices()
f = "https://raspador.local:8080"

req = {
    "version": "U2F_V2",
    "challenge": "K0aDxsacDNqrzlaGyLZoFYbXvCJcdIhq0SSaMz-lsV4",
    "appId": f # must use https despite what you hear
    }

print "number of devices found:", len(L)

for d in L:
    with d as dev:
        print d        
        print "OK versions:"
        print ' ', d.get_supported_versions()
        d.wink()
        print "winked, pausing..."
        sleep(2.5)
        print "Trying to register..."
        try:
            registrationResponse = u2f.register(d, req, f)
            print registrationResponse
        except exc.APDUError as e:
            print "APDU Error:"
            if str(e) == '0x6985':
                print ' ', e, 'Conditions of use not satisfied'
                print '  whatever that means'
            else:
                print type(e)
                print ' ', e, "I don't know what that error means"

print "Done."

# methods for a device
#  |  call(self, cmd, data='')
#  |  close(self)
#  |  init(self)
#  |  lock(self, lock_time=10)
#  |  open(self)
#  |  ping(self, msg='Hello U2F')
#  |  set_mode(self, mode)
#  |  wink(self)
#  |  get_supported_versions(self)
#  |      Gets a list of supported U2F versions from the device.
#  |  send_apdu(self, ins, p1=0, p2=0, data='')
#  |      Sends an APDU to the device, and waits for a response.

# HOW TO REGISTER
# registrationResponse = u2f.register(device, registrationRequest, facet)

# HOW TO FORM A REQUEST DICT
## registrationrequest = 
## data = {
##        "version": "U2F_V2",
##        "challenge": string, //b64 encoded challenge
##        "appId": string, //app_id
##    }
