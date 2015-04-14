from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(FireCTestCase):

    def setUp(self):
        # Set up child objects...
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.settings.launch()
        self.settings.wifi()
        self.settings.wifi_switchOn()

        x = self.UTILS.element.getElements(DOM.Settings.wifi_available_networks, "Available networks", False)

        self.UTILS.reporting.logResult("info", "Found %s networks" % len(x))

        for i in x:
            _secure1 = False
            _secure2 = False

            try:
                i.find_element("xpath", ".//aside[contains(@class,'secured')]")
                _secure1 = True
            except:
                pass

            try:
                i.find_element("xpath", ".//small[contains(text(), 'Secured')]")
                _secure2 = True
            except:
                pass

            try:
                _name = i.find_element("xpath", ".//a").text
            except:
                _name = False

            if _name:
                self.UTILS.test.test(_secure1 == _secure2,
                                     "Network '{}' has matching 'network is secured' details ({} "\
                                     "for icon and {} for description).".format(_name, _secure1, _secure2))
