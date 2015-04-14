#===============================================================================
# 35119:  Verify that, when video call button pressed, if user has not logged-in
# in Loop, he is prompted to do that.
#===============================================================================

import sys
sys.path.insert(1, "./")
import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit import DOM
from tests.i18nsetup import setup_translations


class main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.contacts = Contacts(self)

        self.data_layer.connect_to_wifi()

        self.loop.initial_test_checks()

        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)

        self.apps.kill_all()
        time.sleep(2)
        _ = setup_translations(self)

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

        phone_btn = self.marionette.find_element(*DOM.Loop.wizard_login_phone_number)
        self.UTILS.test.test(phone_btn.is_displayed(), "Login using phone number button present")
        
        ffox_btn = self.marionette.find_element(*DOM.Loop.wizard_login_ffox_account)
        self.UTILS.test.test(ffox_btn.is_displayed(), "Login using phone number button present")
