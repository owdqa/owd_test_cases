from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    _gmail_pseudo_locator = ("data-url", "google")

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.gmail_passwd = self.UTILS.general.get_config_variable("gmail_1_pass", "common")

        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)
        self.connect_to_network()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd, False)

        # Cancel the login
        self.marionette.switch_to_frame()
        cancel = self.UTILS.element.getElement(('xpath', '//h1[contains(text(), "Google")]/..'), "Cancel icon")
        # TODO: Change this when ShadowDOM marionette bug fixed (Bug 1061698)
        cancel.tap(25, 25)

        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                    format(self._gmail_pseudo_locator[0], self._gmail_pseudo_locator[1])),
                                   "Gmail login iframe")

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(DOM.Contacts.import_contacts_header, "Import contacts header")
