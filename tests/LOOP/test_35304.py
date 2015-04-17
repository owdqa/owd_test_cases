#===============================================================================
# 35304: Verify that the user can edit the subject and body from the Email
# composer, when trying to call a non-Loop user
#===============================================================================

import sys
sys.path.insert(1, "./")
import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit.apps.loop import Loop
from tests.i18nsetup import setup_translations


class test_main(PixiTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.email = Email(self)
        self.loop = Loop(self)

        self.email_add = self.UTILS.general.get_config_variable("gmail_2_email", "common")
        self.email_pass = self.UTILS.general.get_config_variable("gmail_2_pass", "common")
        self.email_user = self.UTILS.general.get_config_variable("gmail_2_user", "common")
        self.room_subject = "Dummy subject"
       
        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)
        self.data_layer.connect_to_cell_data()

        result = self.loop.initial_test_checks()

        if result:
            self.loop.phone_login_auto()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

        self.email.launch()
        self.email.setupAccount(self.email_user, self.email_add, self.email_pass)
        self.apps.kill_all()
        time.sleep(2)

        _ = setup_translations(self)
        self.expected_reason = "{} {}".format(self.test_contact['name'], self.loop.not_a_loop_user)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact['name'])
        video_btn = self.marionette.find_element(DOM.Contacts.view_contact_hello_option[0],
                                                 DOM.Contacts.view_contact_hello_option[1].format("video"))
        video_btn.tap()

        self.apps.switch_to_displayed_app()
        time.sleep(2)

        self.wait_for_element_displayed(DOM.Loop.new_call_header[0], DOM.Loop.new_call_header[1], timeout=15)
        self.loop.create_new_call(subject=self.room_subject, back_camera=False)
        self.loop.share_micro_and_camera()

        self.wait_for_element_displayed(*DOM.Loop.new_call_fallback_message)
        notif_reason = self.marionette.find_element(*DOM.Loop.new_call_fallback_message)
        self.UTILS.test.test(notif_reason.text == self.expected_reason, "'Not a Firefox Hello user' message found")

        # In 1.1.1, the fallback mechanism implies the creation of a brand new Room
        self.wait_for_element_displayed(*DOM.Loop.new_call_fallback_new_room)
        new_room = self.marionette.find_element(*DOM.Loop.new_call_fallback_new_room)
        new_room.tap()

        # After tapping on new room, the different options to reach our contact are shown
        self.wait_for_element_displayed(DOM.Loop.fallback_options[0], DOM.Loop.fallback_options[1], timeout=15)
        fallback_options = self.marionette.find_elements(*DOM.Loop.fallback_options)

        email_option = [option for option in fallback_options if option.text == self.test_contact["email"]["value"]][0]
        email_option.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        time.sleep(2)

        # Modify the message subject
        subject = self.UTILS.element.getElement(DOM.Email.compose_subject, "Subject input").get_attribute("value")
        self.UTILS.reporting.debug("*** Email Subject before editing: {}".format(subject))
        new_subject = "[NEW SUBJECT] "
        expected = new_subject + subject

        compose_subject = self.marionette.find_element(*DOM.Email.compose_subject)
        compose_subject.send_keys(new_subject)
        subject_after = self.UTILS.element.getElement(DOM.Email.compose_subject, "Subject input").\
                                                        get_attribute("value")
        self.UTILS.test.test(expected == subject_after, "Expected subject: {} Actual subject: {}".\
                            format(expected, subject_after))

        # Modify the message body
        msg_body = self.UTILS.element.getElement(DOM.Email.compose_msg, "Input message area").text
        self.UTILS.reporting.debug("*** Email Body before editing: {}".format(msg_body))
        new_text = "[NEW TEXT] "
        expected = new_text + msg_body 

        compose_msg = self.marionette.find_element(*DOM.Email.compose_msg)
        compose_msg.send_keys(new_text)
        msg_body_after = self.UTILS.element.getElement(DOM.Email.compose_msg, "Input message area").text
        self.UTILS.test.test(expected == msg_body_after, "Expected text: {} Actual text: {}".\
                            format(expected, msg_body_after))
