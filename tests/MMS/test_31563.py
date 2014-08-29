#===============================================================================
# 31563: Remove the subject using the option given in options menu
#
# Procedure:
# 1. Open Messaging app
# 2. Create a new message
# 3. Selecting options menu in top right hand corner to show the options menu (ER1)
# 4. Select Add subject (ER2)
# 5. Type something in the subject field (ER3)
# 6. Tap on the options menu (ER4)
# 7. Tap on Remove Subject option (ER5)
#
# Expected results:
# ER1. The options menu appears giving the possibility to Add Subject
# ER2. The subject field appears above of the text field.
# ER3. There is a temporary banner displayed indicating that message is entering
# MMS mode. It is possible to write something into the Subject field. Just when
# introducing a character, the MMS label appears.
# ER4. Options menu is open with options to Remove Subject and Cancel
# ER5. User is taken back to message composer view. Temporary banner displayed
# indicating that message is entering SMS mode 'Converting to Text message', the
# subject is removed and message is returned to SMS format.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    test_msg = "Hello World"
    test_subject = "My Subject"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.target_mms_number = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Add subject
        #
        self.messages.addSubject(self.test_subject)

        #
        # Check convert notice appears
        #
        convert_notice = self.marionette.find_element(*DOM.Messages.message_convert_notice)
        self.UTILS.test.TEST(convert_notice.text, "Converting to multimedia message.", True)

        #
        # Delete subject
        #
        self.messages.deleteSubject(self.test_subject)

        #
        # Check convert notice appears
        #
        convert_notice = self.marionette.find_element(*DOM.Messages.message_convert_notice)
        self.UTILS.test.TEST(convert_notice.text, "Converting to text message.", True)
