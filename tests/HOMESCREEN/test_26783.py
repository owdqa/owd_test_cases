#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_main(GaiaTestCase):
    
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)
        self.actions    = Actions(self.marionette)

        self.UTILS.setPermission('Homescreen', 'geolocation', 'deny')
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):    
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()

        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.logResult("info", "Launching EME ...")
        self.EME.launch()
        
        x = self.UTILS.getElement(DOM.EME.add_group_button, "'More' icon")
        x.tap()
        self.UTILS.waitForNotElements(DOM.EME.loading_groups_message, "'Loading' message", True, 120)
        
        self.marionette.switch_to_frame()

        _listEls = ("xpath", "//section[@id='value-selector-container']//li")
        _list = self.UTILS.getElements(_listEls, "Groups list", False)
    
    
        
        _list = self.marionette.find_elements(*_listEls)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "1", x)

        _list_names = []
        for i in range(0, len(_list)): #len(_list)):
            _list_names.append(_list[i].find_element("tag name", "span").text)
            if i > 0:
                self.actions.press(_list[i]).move(_list[i-1]).release().perform()
                _list = self.marionette.find_elements(*_listEls)
                
            _list[i].tap()
            
            #
            # Sometimes the first tap does nothing for some reason.
            #
            if not  _list[i].get_attribute("aria-checked"):
                _list[i].tap()
                
        x = self.UTILS.getElement(DOM.GLOBAL.modal_valueSel_ok, "OK button", True, 30)
        x.click()

        self.UTILS.switchToFrame(*DOM.Home.frame_locator)
        time.sleep(5)
        for _list_name in _list_names:
            _boolOK = False
            
            # Reload the groups (silently or we'll have loads of these messages!).
            try:
                x = self.marionette.find_elements(*DOM.EME.groups)
            except:
                break
            
            for i in x:
                _group_name = i.get_attribute("data-query")
                if _group_name == _list_name:
                    _boolOK = True
                    break
                
            self.UTILS.TEST(_boolOK, "'%s' is now among the groups." % _list_name)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "x", x)


