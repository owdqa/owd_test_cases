# OWD-26750
# Deleting of a e-mail in Inbox
#
#   PROCEDURE
#       1. Open Mail app
#       2. Choose a mail from inbox
#       3. Delete an e-mail from Inbox.
#       4. Check inbox
#       5. The mail does not appears on inbox
#   EXPECTED RESULT
#       E-mail is correctly deleted from device Inbox.
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.email import Email


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.email = Email(self)

        self.user1 = self.UTILS.general.get_os_variable("GMAIL_2_USER")
        self.email1 = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")
        self.passwd1 = self.UTILS.general.get_os_variable("GMAIL_2_PASS")

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.email.launch()
        self.email.setupAccount(self.user1, self.email1, self.passwd1)

        _subject = self.marionette.find_elements(*DOM.Email.folder_subject_list)[0].text
        self.UTILS.reporting.logComment("Deleting email with subject '" + _subject + "'.")

        self.email.deleteEmail(_subject)
