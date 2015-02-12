#===============================================================================
# 127: Verify that it is possible to rename the room after sharing it
#
# Prerequisites:
# Mobile user "A" is the owner and has created a room previously,
# it has been already share to some invitees.
#
# Procedure:
# 1. On Rooms list tap on one room created by "A" and already shared with invitees
# (ER1)
# 2. Tap on 'Edit' button (ER2)
# 3. Change the room's name by adding or deleting any character, then tap on Save
# (ER3)
# 4. Go back to Rooms list by tapping on back button (<) (ER4).
#
# Expected results:
# ER1. The Room details screen is open
# ER2. The Edit name room screen is open allowing user to change the name of the
# room
# ER3. The saving screen is shown and user is taken back to Room Detail screen
# where the name is updated with the changes
# ER4. The new name for the room is updated in the Rooms list
#===============================================================================


import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.contacts = Contacts(self)
        self.email = Email(self)
        self.browser = Browser(self)

        self.connect_to_network()

        self.user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.emailadd = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.passwd = self.UTILS.general.get_config_variable("gmail_1_pass", "common")
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
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.test_contact1 = MockContact(email={'type': 'Personal', 'value': self.fxa_user})
        time.sleep(0.5)
        self.test_contact2 = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.test_contact1)
        self.UTILS.general.insertContact(self.test_contact2)

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

        # Share the room with the two test contacts
        self.loop.share_room(self.test_contact1, by_sms=False)
        self.loop.share_room(self.test_contact2, by_sms=True)

        self.apps.kill_all()
        time.sleep(2)
        self.loop.launch()
        time.sleep(3)
        self.loop.open_room_details(self.test_room)
        time.sleep(2)
        self.loop.edit_room(self.new_name)

        # Check the new room name in the details view
        time.sleep(5)
        self.wait_for_element_displayed(*DOM.Loop.room_name)
        name = self.marionette.find_element(*DOM.Loop.room_name)
        self.UTILS.test.test(name.text == self.new_name, "New name for room is [{}]   Expected: [{}]".
                             format(name.text, self.new_name))
