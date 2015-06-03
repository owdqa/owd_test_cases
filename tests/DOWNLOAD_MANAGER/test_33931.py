# 33931: Verify the downloads list, when it's empty
# ** Procedure
#       1. Open settings app
#       2. Open Downloads
#
# ** Expected Results
#       Downloads list is displayed successfully. A message similar to "No downloads" is displayed
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        _ = setup_translations(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

        # Verify no downloads are present
        no_downloads = self.UTILS.element.getElement(
            DOM.DownloadManager.download_empty_list_content, "Getting empty list content")
        self.UTILS.test.test(no_downloads.text == _("No downloads"),
                             "Verifying '{}' message is displayed".format(_("No downloads")))
