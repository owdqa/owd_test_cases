import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.facebook import Facebook
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.facebook = Facebook(self)
        self.settings = Settings(self)

        self.fb_user = self.UTILS.general.get_config_variable("T19392_FB_USERNAME")
        self.fb_pass = self.UTILS.general.get_config_variable("T19392_FB_PASSWORD")
    
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)
        self.connect_to_network()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.tapSettingsButton()
        self.contacts.enable_FB_import()

        self.facebook.login(self.fb_user, self.fb_pass)

        # Import facebook contacts.
        self.contacts.switch_to_facebook()
        friend_count = self.facebook.importAll()

        # Go back to "All contacts" screen
        backBTN = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Details 'done' button")
        backBTN.tap()

        fb_contacts = self.UTILS.element.getElements(DOM.Contacts.social_network_contacts,
                                                     "Social network contact list", True, 20, False)

        self.UTILS.test.test(
            len(fb_contacts) == friend_count, "Checking all contacts ({}) have been imported".format(friend_count))

        time.sleep(2)
        self.contacts.tapSettingsButton()

        total_fb = self.UTILS.element.getElement(DOM.Facebook.totals, "Facebook totals")
        shown_msg = str(friend_count) + "/" + str(friend_count) + " friends imported"
        self.UTILS.test.test(
            total_fb.text == shown_msg, "Check that the message actually matches the number of contacts imported")
