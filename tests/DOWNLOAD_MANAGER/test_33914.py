# 33914: Try to open a .mp3 file from download list
# ** Procedure
#       1. Open browser app
#       2. Open a webpage whitch  you can download files.
#       3. Download a .mp3 file.
#       4. Open Settings/Downloads list
#       5. Tap on the file downloaded
# ** Expected Results
#       The file is opened successfully
#
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.music import Music
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.music = Music(self)
        self.test_url = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.file_name = "GOSPEL.mp3"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.connect_to_network()
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.browser.launch()
        self.browser.open_url(self.test_url)
        self.download_manager.download_file(self.file_name)
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=60)
        time.sleep(5)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()
        self.download_manager.open_download(self.data_url)
        self.download_manager.tap_on_open_option()

        self.UTILS.iframe.switchToFrame(*DOM.Music.frame_locator)
        time.sleep(5)

        title = self.UTILS.element.getElement(DOM.Music.title_song, "Getting song title in music player")
        self.UTILS.test.TEST(title.text in self.file_name, "Mp3 file title")

        self.UTILS.test.TEST(self.music.is_player_playing(), "Mp3 file is being played")

