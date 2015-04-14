#===============================================================================
# 126: Verify that the user can rename a room
#
# Procedure:
# --Owner
# 1. On Rooms list tap on one room created by "A" (ER1)
# 2. Tap on 'Edit' button (ER2)
# 3. Change the room's name by adding or deleting any character, then tap on
# Save (ER3)
# 4. Go back to Rooms list by tapping on back button (<) (ER4).
# --Invited user
# 1. Check that there is no way to change the name of the room (ER5)
#
# Expected results:
# --Owner
# ER1. The Room details screen is open
# ER2. The Edit name room screen is open allowing user to change the name of
# the room
# ER3. The saving screen is shown and user is taken back to Room Detail screen
# where the name is updated with the changes
# ER4. The new name for the room is updated in the Rooms list
# --Invited user
# ER5. There should not be any way to change the name of the room
#===============================================================================

import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit import DOM


class test_main(FireCTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.contacts = Contacts(self)
        self.email = Email(self)
        self.browser = Browser(self)

        self.data_layer.connect_to_wifi()

        self.user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.emailadd = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.passwd = self.UTILS.general.get_config_variable("gmail_1_pass", "common")
        self.hot_user = self.UTILS.general.get_config_variable("hotmail_1_user", "common")
        self.hot_emailadd = self.UTILS.general.get_config_variable("hotmail_1_email", "common")
        self.hot_passwd = self.UTILS.general.get_config_variable("hotmail_1_pass", "common")
        self.email.launch()
        self.email.setupAccount(self.user, self.emailadd, self.passwd)
        self.apps.kill_all()
        time.sleep(2)

        self.loop.initial_test_checks()

        self.apps.kill_all()
        time.sleep(2)
        self.test_room = "Room{}".format(time.time())
        self.new_name = self.test_room + "--New"
        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")
        self.test_contact = MockContact(email={'type': 'Personal', 'value': self.fxa_user})
        self.UTILS.general.insertContact(self.test_contact)

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
        self.loop.edit_room(self.new_name)

        # Check the new room name in the details view
        time.sleep(5)
        self.wait_for_element_displayed(*DOM.Loop.room_name)
        name = self.marionette.find_element(*DOM.Loop.room_name)
        self.UTILS.test.test(name.text == self.new_name, "New name for room is [{}]   Expected: [{}]".
                             format(name.text, self.new_name))

        # Share the room with the user we have just created
        self.loop.share_room(self.test_contact, by_sms=False)

        # Now logout and log in with another user
        self.marionette.find_element(*DOM.Loop.room_back_btn).tap()
        self.loop.open_settings()
        self.loop.logout()
        time.sleep(3)
        self.loop.firefox_login(self.fxa_user, self.fxa_pass)
        self.UTILS.iframe.switchToFrame(*DOM.Loop.frame_locator)
        self.loop.tap_on_firefox_login_button()

        self.email.launch()
        self.email.setupAccount(self.hot_user, self.hot_emailadd, self.hot_passwd)
        invitation = self.email.get_email("Firefox Hello")
        self.UTILS.reporting.debug("Room invitation received: {}".format(invitation))
        invitation.tap()
        self.email.wait_for_email_loaded("Firefox Hello")
        link = self.marionette.find_element(*DOM.Loop.room_link_in_email)
        self.UTILS.reporting.debug("Link found in email: {}".format(link.text))
        self.UTILS.element.simulateClick(link)

        # Tap to open the link and join the room
        self.marionette.find_element(*DOM.Loop.room_open_link_ok).tap()

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

        # Hang up the call and go back to the call log
        self.loop.hangup_room()

        # Open the room details and check there is no Edit button
        self.UTILS.reporting.debug("Room closed")
        room_dom = (DOM.Loop.room_entry[0], DOM.Loop.room_entry[1].format(self.new_name))
        self.UTILS.reporting.debug("Searching room with DOM: {}".format(room_dom))
        room_entry = self.marionette.find_element(*room_dom)
        name = room_entry.get_attribute("data-room-name")
        self.UTILS.test.test(name == self.new_name, "Room name: {}  Expected: {}".format(name, self.new_name))
        self.marionette.find_element(*DOM.Loop.room_edit).tap()
        self.wait_for_element_displayed(*DOM.Loop.room_detail_header)
        self.wait_for_element_not_displayed(*DOM.Loop.room_detail_edit_btn, timeout=10)
        self.UTILS.reporting.debug("No Edit button found, as expected")
