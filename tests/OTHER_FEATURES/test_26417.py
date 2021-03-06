# OWD-26417: Verify the behaviour of Home key
# ** Procedure
#       1. Open some apps (i.e. SMS, Contacts)
#       2. Press home key
#       3. Verify whether user is taken to homescreen
#
# ** Expected Results
#       When user press on home key he is taken to homescreen no matter
#       in which app he is or how many apps are open

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        time.sleep(2)
        self.messages.launch()

        self.UTILS.home.touchHomeButton()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        frame_contacts = (DOM.GLOBAL.frame_containing[0], DOM.GLOBAL.frame_containing[1].format(
            DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1]))
        frame_messages = (DOM.GLOBAL.frame_containing[0], DOM.GLOBAL.frame_containing[1].format(
            DOM.Messages.frame_locator[0], DOM.Messages.frame_locator[1]))

        self.UTILS.element.waitForNotElements(frame_contacts, "Contacts iframe", True, 1)
        self.UTILS.element.waitForNotElements(frame_messages, "Messages iframe", True, 1)

        self.UTILS.element.waitForElements(DOM.Home.grid, "Homescreen icons grid")
