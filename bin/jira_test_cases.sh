#
# These 'types' and ids need to match the Jira parent item id's
# (the ones that contain a list of 'is tested by' test cases).
#
# Because of the way in which test cases are set up in Jira,
# the new branch includes all the tests of the old branch.
#
# Therefore sometimes there will sometimes be more than one
# jira test id in here (for example 1.1 includes: 1.0.1 and 1.1).
#
JIRA_PARENTS=(
"CAMERA          26964"
"VIDEO           26963"
"SETTINGS        26961"
"WIFI            26960"
"BROWSER         26959"
"MUSIC           26958"
"COSTCONTROL     26957"
"MARKETPLACE     26956"
"GALLERY         26955"
"HOMESCREEN      26954"
"CALENDAR        26953"
"CLOCK           26952"
"EMAIL           26951"
"FM_RADIO        26950"
"BLUETOOTH       26949"
"FACEBOOK        26948"
"FTU             26947 27067"
"CONTACTS        26946 27032"
"DIALER          26945 27004"
"OTA             26944"
"MMS             27003"
"SMS             26942 26940"
"OTHER_FEATURES  25657"
)

