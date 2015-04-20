from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.settings.launch()
        self.settings.wifi()
        self.settings.wifi_switchOn()

        available_nets = self.UTILS.element.getElements(DOM.Settings.wifi_available_networks, "Available networks",
                                                        False)

        self.UTILS.reporting.logResult("info", "Found {} networks".format(len(available_nets)))

        for net in available_nets:
            _secure1 = False
            _secure2 = False

            try:
                _secure1 = 'secured' in net.get_attribute('class')
            except:
                pass

            try:
                net.find_element("xpath", "../small[contains(text(), 'Secured')]")
                _secure2 = True
            except:
                pass

            try:
                _name = net.find_element("xpath", "../a").text
            except:
                _name = False

            if _name:
                self.UTILS.test.test(_secure1 == _secure2,
                                     "Network '{}' has matching 'network is secured' details ({} "\
                                     "for icon and {} for description).".format(_name, _secure1, _secure2))
