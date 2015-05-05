#===============================================================================
# 27036: Go back (Cancel ('x')) on Account web log-in page
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Gmail
# 4. Verify the log in screen is shown
# 5. Go back to Settings
#
# Expected results:
# It should be possible to go back to Settings from the authentication login
# screen
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        settings_btn = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        settings_btn.tap()

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        time.sleep(1)
        import_btn.tap()

        gmail_btn = self.UTILS.element.getElement(DOM.Contacts.gmail_button, "Gmail button")
        time.sleep(1)
        gmail_btn.tap()

        self.UTILS.reporting.logResult("info", "Check that the gmail login frame is present ...")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.Contacts.gmail_frame, "Gmail login iframe")
        time.sleep(1)
        
        cancel = self.UTILS.element.getElement(('xpath', '//h1[contains(text(), "Google")]/..'), "Cancel icon")
        # TODO: Change this when ShadowDOM marionette bug fixed (Bug 1061698)
        cancel.tap(25, 25)

        self.UTILS.reporting.logResult("info", "Check that the gmail login frame is no longer present ...")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(DOM.Contacts.gmail_frame, "Gmail login iframe")

        self.UTILS.reporting.logResult("info", "Check that the contacts app is now visible again ...")
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        self.UTILS.element.waitForElements(DOM.Contacts.import_contacts_header, "Import contacts header")
