#===============================================================================
# 35303: Verify that the user can edit the body in the SMS composer, when trying
# to call a non-Loop user
#===============================================================================

import sys
sys.path.insert(1, "./")
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.loop import Loop
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.loop = Loop(self)

        # Get details of our test contacts.
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)
        self.data_layer.connect_to_wifi()

        result = self.loop.initial_test_checks()

        if result:
            self.loop.phone_login()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

        self.apps.kill_all()
        time.sleep(2)

        _ = setup_translations(self)
        self.expected_message = _("No problem! Just share the following link and they can call you back from"\
                                  " any browser.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
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
        share_by_sms = self.UTILS.element.getElement(DOM.Loop.share_panel_sms_share, "Share by SMS")
        share_by_sms.tap()
        self.UTILS.iframe.switch_to_frame(*DOM.Messages.frame_locator)
        time.sleep(2)
        msg_body = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Input message area").text
        self.UTILS.reporting.debug("*** SMS Body before editing: {}".format(msg_body))
        new_text = " This is more test in the SMS"
        expected = msg_body + new_text
        self.UTILS.general.typeThis(DOM.Messages.input_message_area, "Input message area",
                                    new_text, p_clear=False, p_validate=False)
        msg_body_after = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Input message area")
        self.UTILS.test.test(expected == msg_body_after.text, "Expected text: {} Actual text: {}".\
                             format(expected, msg_body_after.text))
