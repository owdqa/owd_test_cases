#===============================================================================
# 26779: Verify that if no connection available when selecting a category
# in everything.me the user will be notified about the need to have a
# network connection to use this functionality
#
# Pre-requisites:
# The user shouldn't have a valid internet connection available.
#
# Procedure:
# Navigate to everything.me main page
#
# Expected results:
# The user will be notified about the need to have a network connection
# to use this functionality.
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(FireCTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.EME = EverythingMe(self)
        self.settings = Settings(self)
        self.cat_id = "207"

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        #
        # Select a category (group).
        #
        self.EME.pick_group(self.cat_id)

        #
        # Verify that the message is displayed.
        #
        self.UTILS.element.waitForElements(DOM.EME.offline_message,
                                   "Connection message (without using with a network first)", timeout=30)
