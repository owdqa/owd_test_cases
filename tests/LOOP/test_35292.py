#===============================================================================
# 35292: When I try to call a non-Loop user, and I select the option to use for
# share the URL in the confirmation message window, the different sharing
# options are shown
#===============================================================================

import sys
sys.path.insert(1, "./")
import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.loop import Loop
from tests.i18nsetup import setup_translations


class test_main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.loop = Loop(self)

        self.test_contact = MockContact()
        curr_time = repr(time.time()).replace('.', '')
        self.test_contact['email'] = [self.test_contact['email']]
        self.test_contact['tel'] = [self.test_contact['tel']]
        self.test_contact['email'].append({
            'type': 'Job',
            'value': '{}@testmail.net'.format(curr_time)})
        self.test_contact['tel'].append({
            'type': 'Landline',
            'value': '91{}'.format(curr_time)})
        self.UTILS.general.insertContact(self.test_contact)
        self.data_layer.connect_to_wifi()

        self.loop.initial_test_checks()

        result = self.loop.wizard_or_login()
        if result:
            self.loop.phone_login_auto()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
        self.apps.kill_all()
        time.sleep(2)

        _ = setup_translations(self)
        self.expected_reason = "{} {}".format(self.test_contact['name'], self.loop.not_a_loop_user)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact['name'])
        video_btn = self.marionette.find_element(DOM.Contacts.view_contact_hello_option[0],
                                                 DOM.Contacts.view_contact_hello_option[1].format("video"))
        video_btn.tap()

        self.apps.switch_to_displayed_app()
        time.sleep(2)

        self.wait_for_element_displayed(DOM.Loop.new_call_header[0], DOM.Loop.new_call_header[1], timeout=15)
        self.loop.create_new_call(subject="Dummy subject", back_camera=False)
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
        fallback_options_text = [option.text for option in fallback_options]

        for index, number in enumerate(self.test_contact['tel']):
            self.UTILS.test.test(
                number['value'] in fallback_options_text, "Number #{} is in the fallback".format(index))

        for index, email in enumerate(self.test_contact['email']):
            self.UTILS.test.test(
                email['value'] in fallback_options_text, "Number #{} is in the fallback".format(index))
