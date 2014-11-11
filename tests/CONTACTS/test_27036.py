from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    _gmail_pseudo_locator = ("data-url", "google")

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        x = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        time.sleep(1)
        x.tap()

        x = self.UTILS.element.getElement(DOM.Contacts.gmail_button, "Gmail button")
        time.sleep(1)
        x.tap()

        self.UTILS.reporting.logResult("info", "Check that the gmail login frame is present ...")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                    format(self._gmail_pseudo_locator[0], self._gmail_pseudo_locator[1])),
                                   "Gmail login iframe")
        x = self.UTILS.element.getElement(DOM.Contacts.import_cancel_login, "Cancel button")
        x.tap()

        self.UTILS.reporting.logResult("info", "Check that the gmail login frame is no longer present ...")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                    format(self._gmail_pseudo_locator[0], self._gmail_pseudo_locator[1])),
                                   "Gmail login iframe")

        self.UTILS.reporting.logResult("info", "Check that the contacts app is now visible again ...")
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        self.UTILS.element.waitForElements(DOM.Contacts.import_contacts_header, "Import contacts header")