#===============================================================================
# 26770: Launch the everything.me page and click on the first category displayed
#
# Procedure:
# 1- Open everything.me
# 2- click on the first category
#
# Expected results:
# The user can click on any of those categories and a page with a list of
# applications related with that category are shown
#===============================================================================


from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.EME = EverythingMe(self)

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

        self.ids = ["289", "207", "142"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.connect_to_network()

        for i in range(3):
            self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)
            self.EME.pick_group(self.ids[i])
            self.UTILS.iframe.switchToFrame(*DOM.EME.frame_locator)
            items = self.UTILS.element.getElements(DOM.EME.apps_not_installed, "Getting available applications")
            group_name = self.UTILS.element.getElement(DOM.EME.bookmark_group_name, "Bookmark group name")
            self.UTILS.test.test(items, "There are {} applications available for group {}".\
                                        format(len(items), group_name.text))
            btn = self.UTILS.element.getElement(DOM.EME.bookmark_close, "Bookmarks Close button")
            btn.tap()
