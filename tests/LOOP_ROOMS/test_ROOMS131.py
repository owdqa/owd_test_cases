#===============================================================================
# 131: Check the correct behaviour of the Save button
#
# Prerequisites:
# Mobile user "A" is logged in Loop and owns a room
#
# Procedure:
# 1. On Rooms list tap on one room created by "A" (ER1)
# 2. Tap on 'Edit' button (ER2)
# 3. Change the room's name by adding or deleting any character (ER3)
# 4. Tap on Save (ER4)
#
# Expected results:
# ER1. The Room details screen is open
# ER2. The Edit name room screen is open, at this point the Save button
# is greyed out (inactive)
# ER3. The Save button should be active
# ER4. Saving screen is shown and then user is taken back to Room Detail
# screen.
#===============================================================================

import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit import DOM


class test_main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)

        self.data_layer.connect_to_wifi()
        self.loop.initial_test_checks()

        self.apps.kill_all()
        time.sleep(2)
        self.test_room = "Room{}".format(time.time())
        self.new_name = self.test_room + "--New"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

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

        self.wait_for_element_displayed(*DOM.Loop.room_back_btn, timeout=10)
        self.marionette.find_element(*DOM.Loop.room_back_btn).tap()
        time.sleep(1)
        self.loop.open_room_details(self.test_room)
        time.sleep(2)
        self.loop.edit_room(self.new_name)

        # Check the new room name in the details view
        time.sleep(3)
        self.wait_for_element_displayed(*DOM.Loop.room_name)
        name = self.marionette.find_element(*DOM.Loop.room_name)
        self.UTILS.test.test(name.text == self.new_name, "New name for room is [{}]   Expected: [{}]".
                             format(name.text, self.new_name))
