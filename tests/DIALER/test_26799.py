from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact(tel={'type': 'Mobile', 'value': '665666666'})
        self.UTILS.general.insertContact(self.Contact_1)

        self._name = self.Contact_1["name"]
        self.phone_number = self.Contact_1["tel"]["value"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch dialer app.
        #
        self.dialer.launch()

        self.dialer.enterNumber(self.phone_number)
        self.dialer.call_this_number()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(self._name)),
                                    "Outgoing call found with name matching '{}'".format(self._name))

        time.sleep(2)
        self.dialer.hangUp()
