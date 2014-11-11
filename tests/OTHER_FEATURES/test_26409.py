from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.utils import UTILS

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.UTILS.statusbar.openSettingFromStatusbar()

        fnam = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of final position:", fnam)  
   
