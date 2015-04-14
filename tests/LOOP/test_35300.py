#===============================================================================
# 35300: Verify that is possible to cancel the fall back mechanism from the
# sharing options screen, when trying to call (Audio/Video) a non-Loop user
#===============================================================================
import sys
sys.path.insert(1, "./")
import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit.apps.loop import Loop
from tests.i18nsetup import setup_translations


class test_main(FireCTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.email = Email(self)
        self.loop = Loop(self)
        self.room_subject = "Dummy subject"
       
        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)
        self.data_layer.connect_to_cell_data()

        result = self.loop.initial_test_checks()

        if result:
            self.loop.phone_login_auto()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

        self.apps.kill_all()
        time.sleep(2)

        _ = setup_translations(self)
        self.expected_reason = "{} {}".format(self.test_contact['name'], self.loop.not_a_loop_user)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact['name'])
        video_btn = self.marionette.find_element(DOM.Contacts.view_contact_hello_option[0],
                                                 DOM.Contacts.view_contact_hello_option[1].format("video"))
        video_btn.tap()

        self.apps.switch_to_displayed_app()
        time.sleep(2)

        self.wait_for_element_displayed(DOM.Loop.new_call_header[0], DOM.Loop.new_call_header[1], timeout=15)
        self.loop.create_new_call(subject=self.room_subject, back_camera=False)
        self.loop.share_micro_and_camera()

        self.wait_for_element_displayed(*DOM.Loop.new_call_fallback_message)
        notif_reason = self.marionette.find_element(*DOM.Loop.new_call_fallback_message)
        self.UTILS.test.test(notif_reason.text == self.expected_reason, "'Not a Firefox Hello user' message found")

        # In 1.1.1, the fallback mechanism implies the creation of a brand new Room
        self.wait_for_element_displayed(*DOM.Loop.new_call_fallback_cancel)
        cancel_fallback = self.marionette.find_element(*DOM.Loop.new_call_fallback_cancel)
        cancel_fallback.tap()
        self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")