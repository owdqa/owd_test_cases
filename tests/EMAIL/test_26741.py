#===============================================================================
# 26741: Email containing a URL
#
# Pre-requisites:
# Make sure that the user has included an URL in sent message.
#
# Procedure:
# 1. Compose an email containing an URL link
# 2. Send the email to the DuT email address.
# 3. Retrieve the email with the DuT s email client.
# 4. Verify that the email is correctly received.
# 5. A link in the text body should be highlighted and underlined.
# 6. Verify the functionality of the link.
#
# Expected results:
# The user shall be notified on email receival. Email should be
# received and shall contain a link in the text body. The link should
# be highlighted and underlined and it shall work when accessing the link.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Restart the app.
        #
        self.messages.launch()

        #
        # Check things are as we'd expect.
        #
        self.UTILS.element.waitForNotElements(DOM.Messages.threads, "Message threads")
        self.UTILS.element.waitForElements(DOM.Messages.create_new_message_btn,
                                    "Create new message button")
        self.UTILS.element.waitForElements(DOM.Messages.edit_threads_button,
                                    "Edit threads button")
        self.UTILS.element.waitForElements(DOM.Messages.no_threads_message,
                                    "No message threads notification")
