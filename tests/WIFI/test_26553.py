#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_main(GaiaTestCase):
    
    _RESTART_DEVICE = True
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.Browser    = Browser(self)
        self.messages   = Messages(self)
        
        self.wifi_name  = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user  = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass  = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")

        self.num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Open the Settings application.
        #
        self.Settings.launch()
           
        #
        # Tap Wi-Fi.
        #
        self.Settings.wifi()
   
        #
        # Make sure wifi is set to 'on'.
        #
        self.Settings.turn_wifi_on()
           
        #
        # Connect to the wifi.
        #
        self.Settings.tap_wifi_network_name(self.wifi_name, self.wifi_user, self.wifi_pass)
           
        #
        # Tap specific wifi network (if it's not already connected).
        #
        self.UTILS.TEST(
                self.Settings.checkWifiLisetedAsConnected(self.wifi_name),
                "Wifi '" + self.wifi_name + "' is listed as 'connected' in wifi settings.", True)
             
        #
        # Open the browser app.
        #
        self.Browser.launch()
         
        #
        # Open our URL.
        #
        self.Browser.open_url("www.google.com")

        #
        # Open the SMS app, send a message then jump back to the browser asap.
        #
        msgApp = self.messages.launch()
        self.messages.startNewSMS()
        self.messages.addNumbersInToField([self.num])
        self.messages.enterSMSMsg("Test")
        sendBtn = self.UTILS.getElement(DOM.Messages.send_message_button, "Send sms button")
        sendBtn.tap()

        self.apps.kill(msgApp)

        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        self.messages.waitForSMSNotifier(self.num, 60)
        
        self.Browser.open_url("www.wikipedia.com")
        

