#===============================================================================
# 35297: Verify that the Destination (email), Body (containing URL) and Subject
# are properly prepopulated when calling (Audio/Video) a non-Loop user
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
        to_address = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "Recipient Address")

        self.UTILS.test.test(to_address.text == self.test_contact['email']['value'], "Recipient address: {} Expected: {}".\
                             format(to_address.text, self.test_contact['email']['value']))
        subject = self.UTILS.element.getElement(DOM.Email.compose_subject, "Email subject")
        
        self.UTILS.test.test(subject.get_attribute("value") == "Firefox Hello", "Email subject: {} Expected:"\
                             " Firefox Hello".format(subject.get_attribute("value")))
        compose_msg = self.UTILS.element.getElement(DOM.Email.compose_msg, "Message body")
        
        expected_body = _("""Join me for a video chat in my Firefox Hello room {}""".format(self.room_subject))
        self.UTILS.reporting.logResult('info', 'Body: {}'.format(compose_msg.text))
        self.UTILS.test.test(expected_body in compose_msg.text, "Message body: {} Expected: {}".\
                             format(compose_msg.text, expected_body))
