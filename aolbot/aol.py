

import time
from account import Account
from tbrowser import Browser
import random
from helpers import sleepy
from selenium.webdriver.chrome.options import Options
from faker import Faker
import os
from phone import phoney
ipad_emulation = {
    "deviceMetrics": {"width": 1680, "height": 950, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"}


iphone_emulator = {
    "deviceMetrics": {
        "width": 360, "height": 640, "pixelRatio": 3.0
    },
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4"
}


android = {
"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }


def decaptcha_check(browser):
    captch_existance=False

    if browser.exists('id','regImageCaptcha'):
        return False
    else:
        return True
        #wordVerify

def create_AOL(browser,account,phone_object):
    PHONE_VERIFY_TEXT = "You're almost there"
    FINAL_VERIFY_TEXT = 'Here is your account information'
    browser.go('https://i.aol.com/reg/signup')
    number_app = str(random.randint(11,99))
    email_to_use = account.firstName+""+account.lastName+number_app
    account.email = email_to_use
    browser.hover_type('name','firstName', account.firstName)
    browser.hover_type('name','lastName', account.lastName)
    browser.hover_type('name','userName', account.email)
    browser.hover_type('id','password', account.passWord)
    browser.hover_type('id','verifyPassword', account.passWord)
    browser.select_option('id','dobMonth',account.birthMonthString)
    sleepy(1,2)
    try:
        browser.hover_type('id','dobDay', account.birthDay)
    except:
        browser.type2('name','birthDay',account.birthDay)

    browser.hover_type('id','dobYear', account.birthYear)
    sleepy(1,2)

    browser.select_option('id','acctSecurityQuestion',"In which city did your parents meet?")
    sleepy(1,2)

    browser.scroll_down()
    sleepy(2,3)


    browser.hover_type('id','acctSecurityAnswer',account.city)
    browser.hover('id','gender')
    sleepy(1,2)

    browser.select_option('id','gender',"Female")
    sleepy(1,2)
    browser.hover_type('id','zipCode', account.postal_code)
    sleepy(1,2)

    browser.hover_type('name','mobileNum', str(phone_object.intnumber))
    sleepy(1,2)

    alt_email = account.email.replace("_","")
    alt_email = alt_email+"@gmail.com"
    #browser.type2('name','alternateEmail', alt_email)

    browser.click('id','signup-btn')
    sleepy(4,6)
    if PHONE_VERIFY_TEXT in browser.page_source:
        valid_code = phone_object.find_message("AOL verification code")
        valid_code = valid_code.split(" is")[0]
        browser.type2('id','mobileConfirmCode', str(valid_code))
        browser.click('id',"signup-btn")

    if FINAL_VERIFY_TEXT in browser.page_source:
        browser.execute_script('$("#congratsForm").submit()')
        account.aol_id = email_to_use+"@aol.com"
        account.aol_cookies  = browser.get_cookies()

        sleepy(4,5)




def login(browser,account,password,phone):
    browser.go('https://mail.aol.com/webmail/en-us/mobile')
    sleepy(2,3)
    needs_login = 'Get a Free Username'
    if browser.in_html(needs_login):

        browser.hover_type('id','lgnId1',account.aol_id)

        browser.hover_type('id','pwdId1',account.passWord)
        browser.hover('id','submitID')
        browser.click('id','submitID')
    #browser.go('https://mail.aol.com/webmail/en-us/mobile')
    city_string = 'In which city did your parents meet?'
    if browser.in_html(city_string):
        browser.type2('name','asqAnswer',account.security_answer)
        browser.click('id','continueID')
    if browser.in_html('Get The App'):
        print "found the get app"
        browser.click('xpath','/html/body/div/button[2]')
        browser.inject_jquery()
        sleepy(1,2)

        browser.trigger('continue-btn')
        browser.refresh()

def send_email(browser,to='none@gmail.com', subject='none',text='none'):
    browser.trigger('main-view')
    browser.click('xpath','/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/button[4]')
    browser.go('https://mail.aol.com/webmail/en-us/mobile#compose=1')
    time.sleep(5)
    browser.trigger('btn-tb btn-bubble f-right')

def write_file(email,password,international,domestic):
    stringz_to_write = ""
    stringz_to_write = stringz_to_write + "Email : "+email + "\n"
    stringz_to_write = stringz_to_write + "Password : "+password + " \n"
    stringz_to_write = stringz_to_write + "AOL Phone Number: "+international+" \ n"
    stringz_to_write = stringz_to_write + "Facebook Phone Number" + domestic+" \n"
    with open("account.txt","w") as b:
        b.write(stringz_to_write)

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option("mobileEmulation", iphone_emulator)
testdir = os.path.dirname(os.path.abspath(__file__))
chrome_options.add_argument("nwapp=" + testdir)
chrome_options.add_argument("user-data-dir=" + os.path.join(testdir, 'userdata'))
mobile = Browser('Chrome', chrome_options)
phone = phoney(message_id='AP10bc4b612535a5248810fc85719437e0')
usnumber = phone.buy_us_number('818')

intnumber = phone.buy_foreign_number()
account = Account(password="DeskjAt1$$",intnum = intnumber, usnum=usnumber)
create_AOL(browser=mobile,account=account,phone_object=phone)
send_email(mobile)
write_file(account.aol_id,account.passWord,str(account.intnumber),str(account.usnumber))
needs_fb = raw_input("TYPE IN 'FB' without quotes, once you have verified the phone number and need the code")
if needs_fb.upper()=="FB":
    print "CODE IS "+phone.get_fb_code()
