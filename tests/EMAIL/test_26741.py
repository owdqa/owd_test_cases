#===============================================================================
# 26741: Email containing a URL
#
# Pre-requisites:
# Make sure that the user has included an URL in sent message.
#
# Procedure:
# 1. Compose an email containing an URL link
# 2. Send the email to the DuT email address.
# 3. Retrieve the email with the DuT s email client.
# 4. Verify that the email is correctly received.
# 5. A link in the text body should be highlighted and underlined.
# 6. Verify the functionality of the link.
#
# Expected results:
# The user shall be notified on email receival. Email should be
# received and shall contain a link in the text body. The link should
# be highlighted and underlined and it shall work when accessing the link.
#===============================================================================

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from tests.EMAIL.shared_test_functions.emailing import Emailing


class test_26741(Emailing):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        self.testNum = self.__class__.__name__
        self.testType = "gmail"

        self.setUpEmail()
        self.link = "http://www.wikipedia.org"
        self.body = "This is the test msg with a link: {}".format(self.link)

        #
        # Email parameters
        #
        self.username1 = self.UTILS.general.get_os_variable(self.testType.upper() + "_1_USER")
        self.email1 = self.UTILS.general.get_os_variable(self.testType.upper() + "_1_EMAIL")
        self.passwd1 = self.UTILS.general.get_os_variable(self.testType.upper() + "_1_PASS")
        self.user1 = {"username": self.username1, "email": self.email1, "pass": self.passwd1}

        self.username2 = self.UTILS.general.get_os_variable(self.testType.upper() + "_2_USER")
        self.email2 = self.UTILS.general.get_os_variable(self.testType.upper() + "_2_EMAIL")
        self.passwd2 = self.UTILS.general.get_os_variable(self.testType.upper() + "_2_PASS")
        self.user2 = {"username": self.username2, "email": self.email2, "pass": self.passwd2}

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.send_email(self.user1, self.user2)
        time.sleep(2)
        self.apps.kill_all()
        time.sleep(2)
        self.receive_email(self.user2, self.user1)

        email_body = self.UTILS.element.getElement(DOM.Email.open_email_body, "Email body")
        self.UTILS.test.test(self.link in email_body.text, "The link is in the email body")

        # Check link behavior
        email_body.find_element(*DOM.Email.open_email_body_link).tap()
        self.marionette.find_element(*DOM.Email.confirmation_browser_ok).tap()

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
        time.sleep(2)
        self.browser.check_page_loaded(self.link)