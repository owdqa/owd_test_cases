#===============================================================================
# 129: Verify that the new name for the room is shown in Rooms list
#
# Procedure:
# 1. On Rooms list tap on one room created by "A" (ER1)
# 2. Tap on 'Edit' button (ER2)
# 3. Change the room's name by adding or deleting any character, then tap on
# Save (ER3)
# 4. Go back to Rooms list by tapping on back button (<) (ER4).
# 5. Check whether the room name change is already visible for B user (ER5)
#
# Expected results:
# ER1. The Room details screen is open
# ER2. The Edit name room screen is open allowing user to change the name of the
# room
# ER3. The saving screen is shown and user is taken back to Room Detail screen
# where the name is updated with the changes
# ER4. The new name for the room is updated in the Rooms list
# ER5. The new name for the room will be available for B user once he joins the
# room again
#===============================================================================


import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit import DOM


class test_main(PixiTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)
        self.browser = Browser(self)

        self.connect_to_network()

        self.loop.initial_test_checks()

        self.apps.kill_all()
        time.sleep(2)
        self.test_room = "Room{}".format(time.time())
        self.new_name = self.test_room + "--New"
        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.test_contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.test_contact)

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
        # Share the room with the user we have just created
        self.loop.share_room(self.test_contact, by_sms=True)

        self.apps.kill_all()
        time.sleep(2)
        self.loop.launch()
        time.sleep(3)
        self.loop.open_room_details(self.test_room)
        time.sleep(2)
        self.loop.edit_room(self.new_name)

        # Check the new room name in the details view
        time.sleep(3)
        self.wait_for_element_displayed(*DOM.Loop.room_name)
        name = self.marionette.find_element(*DOM.Loop.room_name)
        self.UTILS.test.test(name.text == self.new_name, "New name for room is [{}]   Expected: [{}]".
                             format(name.text, self.new_name))

        # Now logout and log in with another user
        self.marionette.find_element(*DOM.Loop.room_back_btn).tap()
        self.loop.open_settings()
        self.loop.logout()
        time.sleep(3)
        self.loop.firefox_login(self.fxa_user, self.fxa_pass)
        self.UTILS.iframe.switchToFrame(*DOM.Loop.frame_locator)
        self.loop.tap_on_firefox_login_button()

        # Open the messaging application and click the room link
        self.messages.launch()
        self.messages.openThread(self.test_contact['name'])
        send_time = self.messages.last_sent_message_timestamp()
        msg = self.messages.wait_for_message(send_time)
        link = self.marionette.find_element(*DOM.Messages.link_in_msg, id=msg.id)
        self.UTILS.reporting.debug("Link in message: {}".format(link.text))
        self.UTILS.element.simulateClick(link)

        # Go to the browser iframe to look for the Join button
        time.sleep(2)
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
        self.browser.switch_to_frame_by_url("hello.firefox.com")
        self.wait_for_element_displayed(*DOM.Loop.room_btn_browser_join)
        join_btn = self.marionette.find_element(*DOM.Loop.room_btn_browser_join)
        join_btn.tap()

        # Switch again to Hello frame and select Front camera
        time.sleep(2)
        self.UTILS.iframe.switchToFrame(*DOM.Loop.frame_locator)
        self.loop.select_camera_and_join_room(back=False)
        self.loop.share_micro_and_camera()
        time.sleep(2)

        self.wait_for_element_displayed(*DOM.Loop.room_call_name, timeout=20)
        name = self.marionette.find_element(*DOM.Loop.room_call_name).text
        self.UTILS.test.test(name == self.new_name, "Room name for user B: {}  Expected: {}".
                             format(name, self.new_name))
        time.sleep(3)
