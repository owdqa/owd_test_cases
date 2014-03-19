#
# Runs through composing and sending an email as one user, then
# receiving it as another user.
#
# As I can't see ANY different between read and unread emails in the html,
# I need to rely on a totally unique subject line to identify the precise
# message sent between the two test accounts.
#

#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit.apps.settings import Settings

#
# Imports particular to this test case.
#
import os
import time


class Emailing(GaiaTestCase):

    def setUpEmail(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.user1 = self.UTILS.general.get_os_variable(self.testType.upper() + "_1_USER")
        self.email1 = self.UTILS.general.get_os_variable(self.testType.upper() + "_1_EMAIL")
        self.passwd1 = self.UTILS.general.get_os_variable(self.testType.upper() + "_1_PASS")
        self.user2 = self.UTILS.general.get_os_variable(self.testType.upper() + "_2_USER")
        self.email2 = self.UTILS.general.get_os_variable(self.testType.upper() + "_2_EMAIL")
        self.passwd2 = self.UTILS.general.get_os_variable(self.testType.upper() + "_2_PASS")

        self.UTILS.reporting.logComment("Using username 1 '" + self.user1 + "'")
        self.UTILS.reporting.logComment("Using password 1 '" + self.passwd1 + "'")
        self.UTILS.reporting.logComment("Using email    1 '" + self.email1 + "'")
        self.UTILS.reporting.logComment("Using username 2 '" + self.user2 + "'")
        self.UTILS.reporting.logComment("Using password 2 '" + self.passwd2 + "'")
        self.UTILS.reporting.logComment("Using email    2 '" + self.email2 + "'")

        self.Email = Email(self)
        self.settings = Settings(self)

        #
        # Set up specific folder names.
        #
        if "gmail" in self.testType.lower():
            self.UTILS.reporting.logComment("Gmail account being used.")
            self.sentFolderName = "Sent Mail"
        else:
            self.UTILS.reporting.logComment("Non-gmail account being used.")
            self.sentFolderName = "Sent"

        self.marionette.set_search_timeout(50)

        #
        # Make sure we have some data connectivity.
        #
        self.UTILS.network.getNetworkConnection()

    def send_email(self):

        self.setUpEmail()

        #
        # We're sending, so create (and record) a unique 'subject'.
        #
        self.subject = "TEST " + str(time.time())
        self.body = "This is the test email body."

        self.UTILS.reporting.logComment("Using subject \"" + self.subject + "\".")

        #
        # Keep the subject in a file so the next test (receive email)
        # can see what subject to search for.
        #
        SUBJECT_FILE = open(os.environ['RESULT_DIR'] + "/.email_subject", "w")
        SUBJECT_FILE.write(self.subject)
        SUBJECT_FILE.close()

        #
        # Launch Email app.
        #
        self.Email.launch()

        #
        # Login.
        #
        self.Email.setupAccount(self.user1, self.email1, self.passwd1)

        #
        # Return to the Inbox.
        #
        self.Email.openMailFolder("Inbox")

        #
        # At the inbox, compose and send a new email (or fail).
        #
        self.Email.send_new_email(self.email2, self.subject, self.body)

        #
        # Check our email is in the sent folder.
        #
        self.Email.openMailFolder(self.sentFolderName)
        time.sleep(10)
        self.UTILS.test.TEST(self.Email.emailIsInFolder(self.subject),
            "Email '" + self.subject + "' found in the Sent folder.", False)

    def receive_email(self):
        self.setUpEmail()

        #
        # Get the unique 'subject'.
        #
        try:
            SUBJECT_FILE = open(os.environ['RESULT_DIR'] + "/.email_subject", "r")
            self.subject = SUBJECT_FILE.read()
            SUBJECT_FILE.close()
        except:
            self.UTILS.reporting.logResult(False, "Email subject file was not found - this test should only"\
                                 " be run in conjunction with a 'send email' test.")
            self.UTILS.test.quitTest()

        self.UTILS.reporting.logComment("Using subject \"" + self.subject + "\".")

        #
        # Launch Email app.
        #
        self.Email.launch()

        #
        # Login.
        #
        self.Email.setupAccount(self.user2, self.email2, self.passwd2)

        self.UTILS.reporting.logResult("info", "Finished setting up the account to log in with.")

        #
        # Open the email (we'll already be in the Inbox).
        #
        self.UTILS.test.TEST(self.Email.openMsg(self.subject),
            "Email was opened successfully.", True)

        #
        # Verify the contents - the email address is shortened to just the name (sometimes!).
        #
        email1_name = self.email1.split("@")[0]
        email2_name = self.email2.split("@")[0]

        x = self.UTILS.element.getElement(DOM.Email.open_email_from, "'From' field")

        self.UTILS.test.TEST((x.text == self.email1 or x.text == email1_name or x.text == self.user1),
            "'From' field shows the sender (it was '" + x.text + "').")

        x = self.UTILS.element.getElement(DOM.Email.open_email_to, "'To' field")
        self.UTILS.test.TEST((x.text == self.email2 or x.text == email2_name),
            "'To' field = '" + self.email2 + "', (it was '" + x.text + "').")

        x = self.UTILS.element.getElement(DOM.Email.open_email_subject, "'Subject' field")
        self.UTILS.test.TEST(x.text == self.subject,
            "'From' field = '" + self.subject + "', (it was '" + x.text + "').")
