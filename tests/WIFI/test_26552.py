#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Settings
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps import Messages


class test_main(GaiaTestCase):
    
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
        self.Settings.wifi()
        self.Settings.wifi_switchOn()
        self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
             
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
        msgapp = self.messages.launch()
        self.messages.createAndSendSMS([self.num], "Test message.")

        self.apps.kill_all()

        self.Browser.launch()
        self.Browser.open_url("www.wikipedia.com")
        

