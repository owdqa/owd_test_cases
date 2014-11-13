#===============================================================================
# 31720: Differentiation between EMS, MMS and SMS
#
# Procedure:
# Each type of message: SMS, EMS and MMS shall be identified by a particular
# icon with the object of being able to differentiate between the types of
# messages.
# 1. In client A, create a new MM
# 2. In MM header: To-field is set to Client B (DuT).
# 3. In MM content: Add any content
# 4. In client A, send MM to Client B (DuT)
# 5. In Client B (DuT), accept the message .
# 6. In client A, create a new SMS
# 7. In SMS header: To-field is set to Client B (DuT)
# 8. In SMS content: add any text.
# 9. In client A, send SMS to Client B (DuT).
# 10. In Client B (DuT), accept the message.
# 11. In client A, repeat process with a EMS
# 12. In client A, send message to Client B (DuT).
# 13. In Client B (DuT), accept the message
# 14. Verify the pass criteria below.
#
# Expected results:
# In Client B (DuT), each kind of message must be differentiated with a different
# icon.
# ADDITIONAL INFO:
# For MX:
# Include text, smiley / animations, sound in EMS
# For EC:
# Also the handset must notify when the SMS change to MMS"
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

        #
        # Create message.
        #
        sms_message = "Test"

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], sms_message)
        self.messages.wait_for_message()
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.UTILS.element.waitForNotElements(DOM.Messages.mms_icon, "MMS Icon")

        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(sms_message)

        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        self.messages.wait_for_message()

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.checkMMSIcon(self.phone_number)
