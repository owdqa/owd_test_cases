#===============================================================================
# 35118:Verify that, if the device has no connection (wifi, data), and the video
# button call is pressed from contact details, Loop app is launched, but the
# user is notified about it.
#===============================================================================

import sys
sys.path.insert(1, "./")
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.loop import Loop
from tests.i18nsetup import setup_translations


class test_main(PixiTestCase):

    def setUp(self):
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.loop = Loop(self)

        # Insert test contact
        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)
        _ = setup_translations(self)

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
        self.loop.tap_on_firefox_login_button()

        self.wait_for_element_displayed(DOM.Loop.error_msg[0], DOM.Loop.error_msg[1], timeout=15)
        error_msg = self.marionette.find_element(*DOM.Loop.error_msg)
        self.UTILS.test.test(error_msg.text == _("Please check your Internet connection"), "No connection messaged shown")
        
        error_ok = self.marionette.find_element(*DOM.Loop.error_screen_ok)
        error_ok.tap()

        self.loop.tap_on_phone_login_button()
        self.wait_for_element_displayed(DOM.Loop.error_msg[0], DOM.Loop.error_msg[1], timeout=15)
        error_msg = self.marionette.find_element(*DOM.Loop.error_msg)
        self.UTILS.test.test(error_msg.text == _("Please check your Internet connection"), "No connection messaged shown")