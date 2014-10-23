#===============================================================================
# 35118:Verify that, if the device has no connection (wifi, data), and the video
# button call is pressed from contact details, Loop app is launched, but the
# user is notified about it.
#===============================================================================

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.loop import Loop
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.loop = Loop(self)

        # Insert test contact
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)
        _ = setup_translations(self)

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
        self.marionette.switch_to_frame()
        msg_dom = (DOM.Loop.connection_error_msg[0], DOM.Loop.connection_error_msg[1].format(_("connection failure")))
        self.wait_for_element_displayed(*msg_dom,
                                        timeout=15)
        error_msg = self.marionette.find_element(*msg_dom)
        self.UTILS.test.TEST(error_msg, "Error message due to connection failure was found")
