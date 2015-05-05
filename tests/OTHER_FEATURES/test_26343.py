from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time


class test_main(SpreadtrumTestCase):

    _test_apps = ["Gallery", "FM Radio"]
    _img_list = ('img1.jpg', 'img2.jpg')

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Load a couple of images into the gallery.
        for i in self._img_list:
            self.UTILS.general.add_file_to_device('./tests/_resources/' + i)

        self.UTILS.home.goHome()

        # launch the test apps (lifted directly from gaiatest).
        gallery_app = {
            'name': "Gallery",
            'app': self.apps.launch("Gallery"),
            'card': (DOM.Home.app_card[0], DOM.Home.app_card[1].format("gallery")),
            'close_button': (DOM.Home.app_close[0], DOM.Home.app_close[1].format("gallery"))
        }
        radio_app = {
            'name': "FM Radio",
            'app': self.apps.launch("FM Radio"),
            'card': (DOM.Home.app_card[0], DOM.Home.app_card[1].format("fm")),
            'close_button': (DOM.Home.app_close[0], DOM.Home.app_close[1].format("fm"))
        }

        self.UTILS.home.touchHomeButton()
        time.sleep(1)

        self.UTILS.home.holdHomeButton()

        self.UTILS.element.waitForElements(DOM.Home.cards_view, "App 'cards' list")

        # For now just click the close_button
        self.UTILS.reporting.logComment("(Didn't drag the app 'up' to close it, I just clicked the 'close' button.)")

        # Kill the radio.
        x = self.UTILS.element.getElement(radio_app["close_button"],
                                          "Close button on '" + radio_app["name"] + "' card")
        x.tap()
        self.UTILS.element.waitForNotElements(radio_app["card"],
                                              "Card for '" + radio_app["name"] + "'", True, 5, False)

        # Open the gallery.
        x = self.UTILS.element.getElement(gallery_app["card"], "Card for '" + gallery_app["name"] + "'")
        x.tap()

        time.sleep(3)
        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)
