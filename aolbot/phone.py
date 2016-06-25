# -*- coding: utf-8 -*-

"""Twilio utilities."""

import logging
from twilio.rest import TwilioRestClient

import logging


# Phoney call
# Initiate phone_object = phoney()
# Initiate phone_number = phone_object.buy_foreign_number() <--- These Numbers are for Hotmail
# Initiate phone_number = phone_object.buy_us_number() <--- These Numbers are for Facebook
# The page for this should have a select form for choosing US or Foreign, Us should prompt for areacode



class phoney():
    #hamik - APc7dd243d30203828b1da987678500df8
    def __init__(self,country="US",areacode="818",message_id="AP10bc4b612535a5248810fc85719437e0"):
        if country != "US":
            self.foreign=True
            self.country = country
            self.areacode=None
        else:
            self.foreign=False
            self.areacode = areacode
        ACCOUNT_SID = "ACc48c89de40a4dd432b67c0ae629df3db"
        AUTH_TOKEN = "3777482f04b561ee7adfe4e50bfca978"
        auth_token = "3777482f04b561ee7adfe4e50bfca978"
        self.intnumber = ""
        self.usnumber = ""
        self.message_service_id  = message_id
        self.client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
#Return phone number
    def buy_us_number(self,areacode=None):
        if areacode==None:
            areacode_serach = self.areacode
        else:
            areacode = areacode

        numbers = self.client.phone_numbers.search(area_code=int(areacode))
        buythis = None
        if numbers:
            iteration = 0
            for x in numbers:
                if x.capabilities['SMS']==True and len(str(x.rate_center))>1 :
                    buythis = numbers[iteration]
                iteration = iteration +1
        res = buythis.purchase()
        numberz = self.client.phone_numbers.update(res.sid, sms_application_sid=self.message_service_id)
        numberz = res.phone_number
        numberz = numberz.replace("+1","")
        self.usnumber = numberz
        return numberz
    #Return phone number
    def buy_foreign_number(self,country="DE"):
        numbers = self.client.phone_numbers.search(country=country,type="mobile")
        buythis = None
        if numbers:
            iteration = 0
            for x in numbers:
                #print  x
                if x.capabilities['SMS']==True:
                    buythis = numbers[iteration]
                iteration = iteration +1
            res = buythis.purchase()
            numberz = self.client.phone_numbers.update(res.sid, sms_application_sid=self.message_service_id)
            self.intnumber = res.phone_number
            return res.phone_number

    def find_message(self,stringz,to = None):
        if to==None:
            to = self.intnumber
        for message in self.client.messages.list():
            if message.direction == 'inbound' and to ==self.intnumber:
                if stringz.upper() in str(message.body).upper():
                    return message.body


    def get_fb_code(self,stringz = 'Facebook code',to = None):
        if to==None:
            to = self.usnumber
        for message in self.client.messages.list():
            if message.direction == 'inbound' and to ==self.usnumber:
                if stringz.upper() in str(message.body).upper():
                    fbz = message.body.replace("Your Facebook code is: ","")
                    fbz = fbz.split(".")[0]
                    return fbz

