'''
  Repurpose AVERMedia C985 button as push-to-talk key
  (good for Streaming while playing games with a Joystick)

  Vendor information for button (via device manger):
  HID\VID_07CA&PID_9850&REV_0101

  Requirements:
  pywinusb, pywin32
'''

import time
import pywinusb.hid as hid
from win32api import keybd_event
import winsound

class App:
    hid_vendor_id = 0x07CA
    hid_product_id = 0x9850
    hid_device_list = None
    sound_enabled = True

    #https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731%28v=vs.85%29.aspx
    ptt_key = 0xC0

    def start( self ):
        self.hid_device_list = hid.HidDeviceFilter( vendor_id = self.hid_vendor_id, product_id = self.hid_product_id )
        self.hid_device_list = self.hid_device_list.get_devices( )

        print "Looking for Device... \nPress Control+C to Quit"

        if self.hid_device_list:
            for device in self.hid_device_list:
                    print "Found One!\n"
                    device.open( )
                    device.set_raw_data_handler( self.raw_input_callback )
        else:
            print "Oh No, no devices were found! \n"

        while True:
            time.sleep( 1000 ) #HID input/keysend on separate thread.

    def raw_input_callback( self, data ):
        # So we know from pushing out the output (data)
        # that we get an array of 9 values, 0-1.
        # index 2 in this array denotes the state of the button
        # 1 is down, 0 is up - so let's send the keypress event to whatever
        # the active window is. Let's just assume people are using global PTT
        #keys so it doesn't really matter what window we actually send the event to.

        if data[2] == 1:
            if self.sound_enabled:
                winsound.PlaySound( "mic-open.wav", winsound.SND_ALIAS )

            print "Microphone open"
            keybd_event( self.ptt_key, 0, 0x0000, 0 )
        elif data[2] == 0:
            if self.sound_enabled:
                winsound.PlaySound( "mic-closed.wav", winsound.SND_ALIAS )

            print "Microphone closed"
            keybd_event( self.ptt_key, 0, 0x0002, 0 )

if __name__ == '__main__':
    app = App( )
    app.start( )
