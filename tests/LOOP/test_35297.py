#===============================================================================
# 35297: Verify that the Destination (email), Body (containing URL) and Subject
# are properly prepopulated when calling (Audio/Video) a non-Loop user
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

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.email = Email(self)
        self.loop = Loop(self)

        self.email_add = self.UTILS.general.get_config_variable("gmail_2_email", "common")
        self.email_pass = self.UTILS.general.get_config_variable("gmail_2_pass", "common")
        self.email_user = self.UTILS.general.get_config_variable("gmail_2_user", "common")
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
        self.email.setup_account(self.email_user, self.email_add, self.email_pass)
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
        self.UTILS.test.test(not_a_user_explanation.text == self.expected_message, "Message found: {} (Expected: {}".\
                             format(not_a_user_explanation.text, self.expected_message))

        share_options = self.UTILS.element.getElements(DOM.Loop.share_link_options, "Sharing options")
        self.UTILS.test.test(len(share_options) == 3, "There are {} sharing options (Expected: 3)".\
                             format(len(share_options)))
        share_by_email = self.UTILS.element.getElement(DOM.Loop.share_panel_email_share, "Share by email")
        share_by_email.tap()
        self.UTILS.iframe.switch_to_frame(*DOM.Email.frame_locator)
        to_address = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "Recipient Address")
        self.UTILS.test.test(to_address.text == self.contact['email']['value'], "Recipient address: {} Expected: {}".\
                             format(to_address.text, self.contact['email']['value']))
        subject = self.UTILS.element.getElement(DOM.Email.compose_subject, "Email subject")
        self.UTILS.test.test(subject.get_attribute("value") == "Firefox Hello", "Email subject: {} Expected:"\
                             " Firefox Hello".format(subject.get_attribute("value")))
        compose_msg = self.UTILS.element.getElement(DOM.Email.compose_msg, "Message body")
        expected_body = _("Click on the link and answer the call! https://hello.firefox.com/#call")
        self.UTILS.test.test(expected_body in compose_msg.text, "Message body: {} Expected: {}".\
                             format(compose_msg.text, expected_body))
