import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        contacts_option = self.UTILS.element.getElement(DOM.Dialer.option_bar_contacts, "Contacts option")
        contacts_option.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.contacts_sub_iframe, via_root_frame=False)
        self.UTILS.element.waitForElements(DOM.Dialer.contact_list_header, "Contact list header")