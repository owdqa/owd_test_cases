#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

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
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
#         self.messages.deleteAllThreads()

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
