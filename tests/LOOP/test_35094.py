# OWD-35094: Verify that if none of the IDs of the selected contact is a
# LoopID, the user is notified and fall-back mechanism is shown.

import time
import sys
sys.path.insert(1, "./")
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from tests.i18nsetup import setup_translations


class main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)

        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)

        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")
        _ = setup_translations(self)
        self.expected_message = _("No problem! Just share the following link and they can call you back from"
                          " any browser.")


        self.connect_to_network()
        self.loop.initial_test_checks()
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

            self.loop.open_address_book()
            elem = (DOM.Contacts.view_all_contact_specific_contact[
                    0], DOM.Contacts.view_all_contact_specific_contact[1].format(self.test_contact["givenName"]))
            entry = self.UTILS.element.getElement(elem, "Contact in address book")
            entry.tap()

            self.UTILS.iframe.switch_to_active_frame()
            elem = (DOM.Loop.call_screen_contact_details[
                    0], DOM.Loop.call_screen_contact_details[1].format(self.test_contact["name"]))
            self.UTILS.element.waitForElements(elem, "Call to contact: {}".format(self.test_contact["name"]))

            time.sleep(5)
            self.apps.switch_to_displayed_app()
            self.UTILS.element.waitForElements(DOM.Loop.share_panel, "Share panel")

            not_a_user_explanation = self.marionette.find_element(*DOM.Loop.not_a_user_explanation)
            self.UTILS.test.test(not_a_user_explanation.text == self.expected_message, "Message found: {} (Expected: {}".\
                                 format(not_a_user_explanation.text, self.expected_message))
