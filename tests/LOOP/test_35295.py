#===============================================================================
# 35295: Verify that if the non-Loop user's email has been selected when
# calling (Audio/Video) a non-Loop user, the email composer will be opened
# via the e-mail activity
#===============================================================================

import sys
sys.path.insert(1, "./")
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit.apps.loop import Loop
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.email = Email(self)
        self.loop = Loop(self)

        self.email_add = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")
        self.email_pass = self.UTILS.general.get_os_variable("GMAIL_2_PASS")
        self.email_user = self.UTILS.general.get_os_variable("GMAIL_2_USER")
        #
        # Get details of our test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)
        self.data_layer.connect_to_wifi()

        result = self.loop.initial_test_checks()

        if result:
            self.loop.phone_login()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

        self.email.launch()
        self.email.setupAccount(self.email_user, self.email_add, self.email_pass)
        self.apps.kill_all()
        time.sleep(2)

        _ = setup_translations(self)
        self.expected_message = _("No problem! Just share the following link and they can call you back from"\
                                  " any browser.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        self.contacts.view_contact(self.contact['name'])
        video_btn = self.marionette.find_element(DOM.Contacts.view_contact_hello_option[0],
                                                 DOM.Contacts.view_contact_hello_option[1].format("video"))
        video_btn.tap()
        self.loop.share_micro_and_camera()
        self.wait_for_element_displayed(*DOM.Loop.not_a_user_explanation, timeout=10)
        not_a_user_explanation = self.marionette.find_element(*DOM.Loop.not_a_user_explanation)
        self.UTILS.test.TEST(not_a_user_explanation.text == self.expected_message, "Message found: {} (Expected: {}".\
                             format(not_a_user_explanation.text, self.expected_message))

        share_options = self.UTILS.element.getElements(DOM.Loop.share_link_options, "Sharing options")
        self.UTILS.test.TEST(len(share_options) == 3, "There are {} sharing options (Expected: 3)".\
                             format(len(share_options)))
        share_by_email = self.UTILS.element.getElement(DOM.Loop.share_panel_email_share, "Share by email")
        share_by_email.tap()
        self.UTILS.iframe.switch_to_frame(*DOM.Email.frame_locator)
        self.UTILS.element.getElement(DOM.Email.compose_header, "Composer header")
