#===============================================================================
# 130: Verify that user can exit editing mode without doing changes
#
# Prerequisites:
# Mobile user "A" is logged in Loop and owns a room
#
# Procedure:
# 1. On Rooms list tap on one room created by "A" (ER1)
# 2. Tap on 'Edit' button (ER2)
# 3. Change the room's name by adding or deleting any character, then
# tap on close button 'X' (ER3)
#
# Expected results:
# ER1. The Room details screen is open
# ER2. The Edit name room screen is open, at this point the Save button
# is greyed out (inactive)
# ER3. User is taken back to Room Detail screen, the name of the room should
# be the same since the changes done did not apply
#===============================================================================

import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit import DOM


class test_main(PixiTestCase):

    def setUp(self):
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)

        self.connect_to_network()
        self.loop.initial_test_checks()

        self.apps.kill_all()
        time.sleep(2)
        self.test_room = "Room{}".format(time.time())

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

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
        time.sleep(3)
        self.marionette.find_element(*DOM.Loop.room_back_btn).tap()
        time.sleep(1)
        self.loop.open_room_details(self.test_room)
        time.sleep(2)

        self.loop.edit_room("New fake room name", save=False)

        # Check the new room name in the details view
        time.sleep(3)
        self.wait_for_element_displayed(*DOM.Loop.room_name)
        name = self.marionette.find_element(*DOM.Loop.room_name)
        self.UTILS.test.test(name.text == self.test_room, "New name for room is [{}]   Expected: [{}]".
                             format(name.text, self.test_room))
