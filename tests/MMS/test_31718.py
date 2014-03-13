#
# MMSTC-COMPT-012b
# Message size during composition
#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery

class test_main(GaiaTestCase):
    
    test_msg = "Test."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):

        #
        # Load files into the device.
        #
        self.UTILS.addFileToDevice('./tests/_resources/imgd.jpg',
                                    destination='DCIM/100MZLLA')

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()
        
        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.target_telNum])
        
        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)

        self.marionette.execute_script("""
            var getElementByXpath = function (path) {
                return document.evaluate(path, document, null, 9, null).singleNodeValue;
            };
            getElementByXpath("/html/body/div/div[2]");
        """)