#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.email import Email


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):

        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.Email = Email(self)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.UTILS.getNetworkConnection()

        self.user1 = self.UTILS.get_os_variable("GMAIL_2_USER")
        self.email1 = self.UTILS.get_os_variable("GMAIL_2_EMAIL")
        self.passwd1 = self.UTILS.get_os_variable("GMAIL_2_PASS")

        self.UTILS.logComment("Using username '" + self.user1 + "'")
        self.UTILS.logComment("Using password '" + self.passwd1 + "'")
        self.UTILS.logComment("Using email    '" + self.email1 + "'")

        #
        # Launch Email app.
        #
        self.Email.launch()

        #
        # Login.
        #
        self.Email.setupAccount(self.user1, self.email1, self.passwd1)

        #
        # Delete the first email we come across.
        #
        _subject = self.marionette.find_elements(*DOM.Email.folder_subject_list)[0].text
        self.UTILS.logComment("Deleting email with subject '" + _subject + "'.")

        self.Email.deleteEmail(_subject)
