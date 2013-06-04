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
from marionette import Actions
from marionette import MultiActions


class test_0(GaiaTestCase):
    _Description = "MOVE APP"
    
    APP_NAME = 'Clock'

    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Market     = AppMarket(self)
        self.Settings   = AppSettings(self)
        
        
        self.UTILS.logComment("Using app '" + self.APP_NAME + "'")


    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
   
        #
        # Launch the app icon in the same screen.
        #
        time.sleep(1)
        
        #
        # Find the app icon and Verify that the app is installed.
        #
        self.UTILS.TEST(self.UTILS.findAppIcon(self.APP_NAME), "App icon is present in the homescreen.")
        if not self.UTILS.isAppInstalled(self.APP_NAME):
            return False
        
        x = ('css selector', DOM.Home.app_icon_css % self.APP_NAME)
        myApp = self.UTILS.getElement(x, "App icon")
        
        # Move App to other place
        actions = Actions(self.marionette)
        actions.press(myApp).wait(2).move_by_offset(-120, 190).wait(5).release().perform()
#         self.UTILS.scrollHomescreenLeft()
        myApp = self.UTILS.getElement(x, "App icon")
        actions.press(myApp).wait(2)
        y = ('css selector', DOM.Home.app_icon_css % "Gallery")
        myApp2 = self.UTILS.getElement(y, "App icon")
        actions.move(myApp2).wait(2).release()
        actions.perform()
        self.UTILS.touchHomeButton()
        return
        
        
        #
        # Launch the app icon to the other screen.
        #
        time.sleep(1)
        
        # Find the app icon and Verify that the app is installed.
        self.UTILS.TEST(self.UTILS.findAppIcon(self.APP_NAME), "App icon is present in the homescreen.")
        if not self.UTILS.isAppInstalled(self.APP_NAME):
            return False
        
        x = ('css selector', DOM.Home.app_icon_css % self.APP_NAME)
        myApp = self.UTILS.getElement(x, "App icon") 
        
        # Move App to its initial place
        actions = Actions(self.marionette)
        actions.press(myApp).wait(5).move_by_offset(-140, -190).wait(5).release()
        actions.perform()
        self.UTILS.touchHomeButton()
       
        # Find the app icon and Verify that the app is installed.
        self.UTILS.TEST(self.UTILS.findAppIcon(self.APP_NAME), "App icon is present in the homescreen.")
        if not self.UTILS.isAppInstalled(self.APP_NAME):
            return False
        
        x = ('css selector', DOM.Home.app_icon_css % self.APP_NAME)
        myApp = self.UTILS.getElement(x, "App icon")
        
        # Move App to other screen
        actions = Actions(self.marionette)
        actions.press(myApp).wait(5).move_by_offset(-120, 190).wait(5).release()
        actions.perform()
        self.UTILS.touchHomeButton()
        time.sleep(5)
        self.UTILS.touchHomeButton()
        
        
        #
        # Launch the app icon to the dock.
        #
        time.sleep(1)
        # Find the app icon and Verify that the app is installed.
        self.UTILS.TEST(self.UTILS.findAppIcon(self.APP_NAME), "App icon is present in the homescreen.")
        if not self.UTILS.isAppInstalled(self.APP_NAME):
            return False
        
        x = ('css selector', DOM.Home.app_icon_css % self.APP_NAME)
        myApp = self.UTILS.getElement(x, "App icon")

       
        # Move App to 'dock'
        actions.press(myApp).wait(5).move_by_offset(2, 80).wait(5).release()
        actions.perform()
        self.UTILS.touchHomeButton()
   
        
