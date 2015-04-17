from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)


    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):

        self.contacts.launch()
        self.messages.launch()
        self.UTILS.home.touchHomeButton()
        time.sleep(1)

        self.UTILS.home.holdHomeButton()

        self.UTILS.element.waitForElements(DOM.Home.cards_view, "App 'cards' list (task switcher)")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot:", x)