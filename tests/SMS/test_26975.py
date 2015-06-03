from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser
from marionette_driver.marionette import Actions

class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)
        self.actions = Actions(self.marionette)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.target_email = self.UTILS.general.get_config_variable("gmail_1_email", "common")

        self.msg = "Testing email link with " + self.target_email

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.connect_to_network()

        # Launch messages app.
        self.messages.launch()

        # Create and send a new test message.
        self.messages.create_and_send_sms([self.phone_number], self.msg)
        """
        Wait for the last message in this thread to be a 'received' one
        and click the link.
        """

        x = self.messages.wait_for_message()
        self.UTILS.test.test(x, "Received a message.", True)

        # Long-press the link.
        email_link = x.find_element("tag name", "a")
        email_link.tap()

        x = self.UTILS.element.getElement(DOM.Messages.header_add_to_contact_btn,
                                    "'Add to an existing contact' button")
        x.tap()

        # Check for warning message.
        self.UTILS.iframe.switchToFrame("src", "contacts")

        self.UTILS.element.waitForElements(("xpath", 
                "//p[contains(text(),'contact list is empty')]"), "Warning message")

        fnam = self.UTILS.debug.screenShot("26975")
        self.UTILS.reporting.logResult("info", "Screenshot of final position", fnam)
