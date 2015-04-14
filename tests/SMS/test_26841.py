#===============================================================================
# 26841: Open SMS app after all sms were deleted or there is any sms
#
# Procedure:
# Open sms and delete all sms
#
# Expected results:
# Verify that SMS app is shown successfully
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        self.messages.delete_all_threads()
        self.UTILS.element.headerCheck("Messages")
