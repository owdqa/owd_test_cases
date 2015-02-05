#===============================================================================
# 35122: Verify that, when video call button pressed, if multiple IDs (e-mail or
# phone numbers), but none of them is a Loop ID, the user is notified about
# that, and a fall-back mechanism is shown.
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
        GaiaTestCase.setUp(self)
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

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact['name'])
        video_btn = self.marionette.find_element(DOM.Contacts.view_contact_hello_option[0],
                                                 DOM.Contacts.view_contact_hello_option[1].format("video"))
        video_btn.tap()
        self.loop.share_micro_and_camera()
        
        not_user_str = _("Not a Firefox Hello user yet")
        not_user_dom = (DOM.Loop.not_a_hello_user_msg[0], DOM.Loop.not_a_hello_user_msg[1].format(not_user_str))
        self.wait_for_element_displayed(*not_user_dom, timeout=10)
        not_a_user_msg = self.marionette.find_element(*not_user_dom)
        self.UTILS.test.test(not_a_user_msg.text == not_user_str, "Message found: {} (Expected: {}".\
                             format(not_a_user_msg.text, not_user_str))
