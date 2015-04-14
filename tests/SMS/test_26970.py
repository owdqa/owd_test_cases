from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser
import time


class test_main(FireCTestCase):

    link = "www.google.com"
    test_msg = "Test " + link + " this."

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        #
        # Launch messages app.
        #
        self.messages.launch()
  
        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], self.test_msg)
  
        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        x = self.messages.wait_for_message()
        self.UTILS.test.test(x, "Received a message.", True)

        # Go into messages Settings..
        #
        z = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        z.tap()

        #
        # Go into message edit mode..
        #
        z = self.UTILS.element.getElement(DOM.Messages.delete_messages_btn, "Edit button")
        z.tap()
   
        y = x.find_element("tag name", "a")
        y.tap()
   
        z = self.UTILS.element.getElement(DOM.Messages.edit_msgs_header,"1 selected message")
        self.UTILS.test.test(z.text == "1 selected", 
            "Into edit mode, if you tap on link, the browser is not open and the message is selected.")


        self.marionette.switch_to_frame()
        time.sleep(5) #(give the browser time to launch)
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src,'browser')]"), "Browser iframe")
