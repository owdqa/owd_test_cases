from OWDTestToolkit.firec_testcase import FireCTestCase
from marionette.marionette import Actions
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.gallery import Gallery
import time


class test_main(FireCTestCase):

    _img_list = ('img1.jpg', 'img2.jpg')

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)

        for i in self._img_list:
            self.UTILS.general.add_file_to_device('./tests/_resources/' + i, destination='DCIM/100MZLLA')

        # launch the test apps (lifted directly from gaiatest).
        self.gallery_app = {
            'name': "Gallery",
            'app': self.apps.launch("Gallery"),
            'card': (DOM.Home.app_card[0], DOM.Home.app_card[1].format("gallery")),
        }
        self.radio_app = {
            'name': "FM Radio",
            'app': self.apps.launch("FM Radio"),
            'card': (DOM.Home.app_card[0], DOM.Home.app_card[1].format("fm")),
        }

        self.UTILS.home.touchHomeButton()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.home.holdHomeButton()
        self.UTILS.element.waitForElements(DOM.Home.cards_view, "App 'cards' list")

        radio_card = self.UTILS.element.getElement(self.radio_app["card"], "Card for: {}".format(self.radio_app["name"]))

        size = radio_card.size
                
        start_x = end_x = size['width'] / 2
        start_y = size['height'] / 2
        end_y = -100
        self.UTILS.reporting.logResult('info', 'Movements: {} {} {} {}'.format(start_x, start_y, end_x, end_y))

        Actions(self.marionette).flick(radio_card, start_x, start_y, end_x, end_y, 1500).perform()

        # Open the gallery.
        gallery_card = self.UTILS.element.getElement(self.gallery_app["card"], "Card for '" + self.gallery_app["name"] + "'")
        gallery_card.tap()

        self.apps.switch_to_displayed_app()
        current_thumbs = self.gallery.get_number_of_thumbnails()
        self.UTILS.test.test(current_thumbs == len(self._img_list), "Number of Gallery images match")