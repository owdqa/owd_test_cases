#
# Runs through composing and sending an email as one user, then
# receiving it as another user.
#
# As I can't see ANY different between read and unread emails in the html,
# I need to rely on a totally unique subject line to identify the precise
# message sent between the two test accounts.
#

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser
from tests.i18nsetup import setup_translations


class Emailing(GaiaTestCase):

    def setUpEmail(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.email = Email(self)
        self.settings = Settings(self)
        self.browser = Browser(self)

        _ = setup_translations(self)

        # Create (and record) a unique 'subject'.
        self.subject = "test " + str(time.time())
        self.body = "This is the test email body."

        # Set up specific folder names.
        if "gmail" in self.test_type:
            self.UTILS.reporting.logComment("Gmail account being used.")
            self.sent_folder_name = _("Sent Mail")
        elif "exchange" in self.test_type:
            self.UTILS.reporting.logComment("Exchange account being used.")
            self.sent_folder_name = _("Sent Items")
        else:
            self.UTILS.reporting.logComment("Non-gmail account being used.")
            self.sent_folder_name = _("Sent")

        self.marionette.set_search_timeout(50)

    def set_subject(self):
        self.subject = "test " + str(time.time())

    def send_email(self, account_to_load, to):
        self.UTILS.reporting.logComment("[SEND]Using subject \"" + self.subject + "\".")

        self.email.launch()
        self.email.setup_account(account_to_load["username"], account_to_load["email"], account_to_load["pass"])
        self.email.open_folder(_("Inbox"))

        # At the inbox, compose and send a new email (or fail).
        if type(to) is list:
            to_addresses = [account["email"] for account in to]
            self.email.send_new_email(to_addresses, self.subject, self.body)
        else:
            self.email.send_new_email(to["email"], self.subject, self.body)

        # Check our email is in the sent folder.
        self.email.open_folder(self.sent_folder_name)
        self.UTILS.test.test(self.email.email_is_in_folder(self.subject),
                             "Email with subject [{}] found in the Sent folder.".format(self.subject))

    def receive_email(self, account_to_load, sender, prefix="", many_recipients=False, files_attached=False):

        self.UTILS.reporting.logComment("[RECEIVE]Using subject \"" + self.subject + "\".")

        self.email.launch()
        self.email.setup_account(account_to_load["username"], account_to_load["email"], account_to_load["pass"])

        # Make sure we're in the inbox
        header_text = self.UTILS.element.getElement(DOM.GLOBAL.app_head, "Application header").text
        self.UTILS.reporting.logResult("info", "Header name in <b>receive_email</b> method: {}".format(header_text))

        if header_text != _("Inbox"):
            self.email.open_folder(_("Inbox"))

        self.UTILS.test.test(self.email.open_msg(prefix + self.subject),
                             "Email was opened successfully.", True)

        to_name = account_to_load["email"].split("@")[0]
        from_name = sender["email"].split("@")[0]

        x = self.UTILS.element.getElement(DOM.Email.open_email_from, "'From' field")

        self.UTILS.test.test((x.text == sender["email"] or x.text == from_name),
                             "'To' field = '" + sender["email"] + "', (it was '" + x.text + "').")

        if many_recipients:
            # self.UTILS.reporting.logResult("info", "Many recipients!!!!!")
            to_fields = self.UTILS.element.getElements(DOM.Email.open_email_to, "'To' field")
            to_fields_text = [elem.text for elem in to_fields]
            isThere = account_to_load["email"] in to_fields_text or to_name in to_fields_text \
                or account_to_load["username"] in to_fields_text

            self.UTILS.test.test(isThere,
                                 "'From' field shows the sender (it was '{}').".format(" ".join(to_fields_text)))
        else:
            x = self.UTILS.element.getElement(DOM.Email.open_email_to, "'To' field")
            self.UTILS.test.test((x.text == account_to_load["email"] or x.text == to_name
                                  or x.text == account_to_load["username"]),
                                 "'From' field shows the sender (it was '" + x.text + "').")

        x = self.UTILS.element.getElement(DOM.Email.open_email_subject, "'Subject' field")
        self.UTILS.test.test(x.text == prefix + self.subject,
                             "'Subject' field = '" + prefix + self.subject + "', (it was '" + x.text + "').")

        if files_attached:
            self.UTILS.element.waitForElements(DOM.Email.open_email_attached_file,
                                               "There are files attached to this mail")
