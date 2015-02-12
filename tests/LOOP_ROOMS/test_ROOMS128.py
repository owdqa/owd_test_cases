#===============================================================================
# 128: Verify that the room name field is pre-filled with the previous name
#
# Procedure:
# 1. On Rooms list tap on one room created by "A" (ER1)
# 2. Tap on 'Edit' button (ER2)
#
# Expected results:
# ER1. The Room details screen is open
# ER2. The Edit name room screen is open showing the current name of the room
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)

        self.connect_to_network()

        self.loop.initial_test_checks()

        self.apps.kill_all()
        time.sleep(2)

        self.test_room = "Room{}".format(time.time())

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.phone_login_auto()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

        self.UTILS.iframe.switchToFrame(*DOM.Loop.frame_locator)
        self.UTILS.reporting.debug("Creating room with name: {}".format(self.test_room))
        self.loop.create_room(self.test_room)
        time.sleep(5)
        self.apps.kill_all()
        time.sleep(2)

        self.loop.launch()
        time.sleep(3)
        self.loop.open_room_details(self.test_room)
        time.sleep(2)

        # Check the room name appears in the details view
        time.sleep(5)
        self.wait_for_element_displayed(*DOM.Loop.room_name)
        name = self.marionette.find_element(*DOM.Loop.room_name)
        self.UTILS.test.test(name.text == self.test_room, "Name shown for room is [{}]   Expected: [{}]".
                             format(name.text, self.test_room))
