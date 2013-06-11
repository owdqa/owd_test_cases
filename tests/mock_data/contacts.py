class MockContacts(dict):
    #
    # The key values here match the data structure in the contacts db
    # so that the json output of this mock can be inserted directly 
    # into the device's db.
    #
    def __init__(self):
        self.Contact_1 = {
                "givenName" : "John",
                "familyName": "Smith",
                "name"      : "John Smith",
                "email"     : {"type": "", "value": "john.smith@nowhere.com"},
                "tel"       : {"type": "Mobile", "carrier": "MoviStar", "value": "111111111"},
                "adr"       : {"streetAddress"    : "One Street",
                               "postalCode"       : "00001",
                               "locality"      : "City One",
                               "countryName"   : "Country One"},
                "bday"      : "1981-01-21",
                "jobTitle"  : "Runner number one",
                "comment"   : "Mock test contact 1"
            }
        self.Contact_2 = {
                "givenName" : "Wilma",
                "familyName": "Wiggle",
                "name"      : "Wilma Wiggle",
                "email"     : {"type": "", "value": "wilma.wiggle@nowhere.com"},
                "tel"       : {"type": "Mobile", "carrier": "MoviStar", "value": "222222222"},
                "adr"       : {"streetAddress"    : "Two Street",
                               "postalCode"       : "00002",
                               "locality"      : "City Two",
                               "countryName"   : "Country Two"},
                "bday"      : "1982-02-22",
                "jobTitle"  : "Dancer number two",
                "comment"   : "Mock test contact 2"
            }
        self.Contact_longName = {
                "givenName" : "AAAAAAAAAAAAAAAALEX",
                "familyName": "SMITHXXXXXXXX",
                "name"      : "AAAAAAAAAAAAAAAALEX SMITHXXXXXXXX",
                "email"     : {"type": "", "value": "alex.smith@nowhere.com"},
                "tel"       : {"type": "Mobile", "carrier": "MoviStar", "value": "333333333"},
                "adr"       : {"streetAddress"    : "Two Street",
                               "postalCode"       : "00002",
                               "locality"      : "City Two",
                               "countryName"   : "Country Two"},
                "bday"      : "1982-02-22",
                "jobTitle"  : "Dancer number two",
                "comment"   : "Mock test contact with long name"
            }
        self.Contact_multiplePhones = {
                "givenName" : "Bobby",
                "familyName": "Bobson",
                "name"      : "Bobby Bobson",
                "email"     : {"type": "", "value": "bobby.bobson@nowhere.com"},
                "tel"       : ({"type": "Mobile 1", "carrier": "MoviStar1", "value": "444444444"},
                               {"type": "Mobile 2", "carrier": "MoviStar2", "value": "555555555"},
                               {"type": "Mobile 3", "carrier": "MoviStar3", "value": "666666666"}),
                "adr"       : {"streetAddress"    : "Two Street",
                               "postalCode"       : "00002",
                               "locality"      : "City Two",
                               "countryName"   : "Country Two"},
                "bday"      : "1982-02-22",
                "jobTitle"  : "Dancer number two",
                "comment"   : "Mock test contact 2"
            }
        self.Contact_multipleEmails = {
                "givenName" : "Holy",
                "familyName": "Moley",
                "name"      : "Holy Moley",
                "email"     : ({"type": "", "value": "email1@nowhere.com"},
                               {"type": "", "value": "email2@nowhere.com"},
                               {"type": "", "value": "email3@nowhere.com"}),
                "tel"       : {"type": "Mobile", "carrier": "MoviStar", "value": "333333333"},
                "adr"       : {"streetAddress"    : "Two Street",
                               "postalCode"       : "00002",
                               "locality"      : "City Two",
                               "countryName"   : "Country Two"},
                "bday"      : "1982-02-22",
                "jobTitle"  : "Dancer number two",
                "comment"   : "Mock test contact 2"
            }

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
