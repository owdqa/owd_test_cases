from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings

class test_main(GaiaTestCase):

    _newGroup = "Sports"

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)

        self.UTILS      = UTILS(self)
        self.settings   = Settings(self)
        self.EME        = EverythingMe(self)

        self.UTILS.app.setPermission('Homescreen', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Make sure 'things' are as we expect them to be first.
        self.connect_to_network()

        # Launch the 'everything.me' app.
        self.UTILS.reporting.logResult("info", "Launching EME ...")
        self.EME.launch()

        # Make sure our group isn't already present.
        #self.EME.remove_groups([self._newGroup], p_validate=False)
        #self.EME.remove_groups([self._newGroup], p_validate=False)
        self.EME.remove_groups([self._newGroup])

        # Add the group.
        self.EME.add_group(self._newGroup)

        # Remove the group.
        self.EME.remove_groups([self._newGroup])


