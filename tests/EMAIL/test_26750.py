#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")

from gaiatest import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
            
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Email      = Email(self)
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.UTILS.getNetworkConnection()

        self.USER1  = self.UTILS.get_os_variable("GMAIL_2_USER")
        self.EMAIL1 = self.UTILS.get_os_variable("GMAIL_2_EMAIL")
        self.PASS1  = self.UTILS.get_os_variable("GMAIL_2_PASS")
        
        self.UTILS.logComment("Using username '" + self.USER1 + "'")
        self.UTILS.logComment("Using password '" + self.PASS1 + "'")
        self.UTILS.logComment("Using email    '" + self.EMAIL1 + "'")

        #
        # Launch Email app.
        #
        self.Email.launch()
                
        #
        # Login.
        #
        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)
        
        #
        # Delete the first email we come across.
        #
        _subject = self.marionette.find_elements(*DOM.Email.folder_subject_list)[0].text
        self.UTILS.logComment("Deleting email with subject '" + _subject + "'.")

        self.Email.deleteEmail(_subject)
