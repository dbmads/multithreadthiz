# -*- coding: utf-8 -*-
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException, NoAlertPresentException, NoSuchFrameException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import re
import platform
import os
import time
import inspect
from selenium.webdriver.chrome.options import Options
import random

class js:
    prefix = "auto_"

    #http://ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js
    jQueryLoader = """(function(jqueryUrl, callback) {
                        if (typeof jqueryUrl != 'string') {
                            jqueryUrl = 'jquery.min.js';
                        }
                        if (typeof jQuery == 'undefined') {
                            var script = document.createElement('script');
                            var head = document.getElementsByTagName('head')[0];
                            var done = false;
                            script.onload = script.onreadystatechange = (function() {
                                if (!done && (!this.readyState || this.readyState == 'loaded'
                                        || this.readyState == 'complete')) {
                                    done = true;
                                    script.onload = script.onreadystatechange = null;
                                    head.removeChild(script);
                                    callback();
                                }
                            });
                            script.src = jqueryUrl;
                            head.appendChild(script);
                        }
                        else {
                            callback();  // these calls to callback supposedly are correct for finishing the async call...
                        }
                    })(arguments[0], arguments[arguments.length - 1]);
                    return true;
                    """

    bruteForceLoadJQuery = """
                            """

    isJQueryLoaded = """if (typeof jQuery == 'undefined') {
                        return false; // jQuery is not loaded
                    } else {
                        return true;  // jQuery is loaded
                    }"""

    loadJQueryIfNotLoaded = """if (!window.jQuery) {
                              var jq = document.createElement('script'); jq.type = 'text/javascript';
                              // Path to jquery.js file, eg. Google hosted version
                              jq.src = 'jquery.min.js';
                              document.getElementsByTagName('head')[0].appendChild(jq);
                            }"""

    hideElement = "$(arguments[0]).hide()"

    loadJQueryUI = """var scriptElt = document.createElement('script');
                    scriptElt.type = 'text/javascript';
                    scriptElt.src = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js';
                    var head = document.getElementsByTagName('head')[0];
                    head.appendChild(scriptElt);
                    head.innerHTML = head.innerHTML + '<link rel=\'stylesheet\' href=\'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css\' />';";
                    """

    setupClickIntercept = ("""$('input[type=text], input[type=password], textarea').not('#idontknow').unbind('focus').focus(function() {
                                window.""" + prefix + """clickedElement = $(this);
                                $(this).blur(); // super important to remove the focus from the input, otherwise focus will be returned to the input once the dialog is closed and the click intercepted again
                                openPrompt();
                            });
                            function openPrompt() {
                                $('#""" + prefix + """inputDialog').dialog('open');
                            };
                            """)

    getInputs =  "$('input').each(function(){var input = $(this);});"

    teardownClickIntercept = "$('input[type=text], input[type=password], textarea').unbind('focus');"

    setupGlobalVariables = ("window." + prefix + "clickedElement = null;"
                            + "window." + prefix + "clickedElement = null;"
                            + "window." + prefix + "randomString = 'Shmoop';"
                            + "window." + prefix + "typedKeys = '';")

    getTypedKeys = "return window." + prefix + "typedKeys;"

    removeWaitDialog = "$('#" + prefix + "waitDialog').dialog('close');"

    getClickedElement = "return window." + prefix + "clickedElement;"

    highlightElement = ("var o = $(arguments[0]);"
                        + "o.addClass('element-highlight');"
                        + "o.attr('style', arguments[1]);")

    unhighlightElement = ("var o = $(arguments[0]);"
                                            + "o.attr('style', arguments[1]);")

    getElementStyle = ("var o = $(arguments[0]);"
                        + "var pastStyle = o.attr('style');"
                        + "return pastStyle;")

    initDialogs = ("var inputDialog = $('<div id=\'" + prefix + """inputDialog\'></div>');
                    inputDialog.append('<br /><input type=\'text\' id=\'idontknow\' />');
                    $('body').append(inputDialog);
                    $('#""" + prefix + """inputDialog').dialog({
                        modal: true,
                        autoOpen: false,
                        buttons: {
                            StupendousButton:function() {
                                window.""" + prefix + """typedKeys = $('#idontknow').val();
                                console.log(window.""" + prefix + """typedKeys);
                                $(this).dialog('close');
                                $('#""" + prefix + """waitDialog').dialog('open');
                                $('#""" + prefix + """waitDialog').append('<div id=\'""" + prefix + """waitDialogIsOpen\'></div>');
                            },
                            Cancel:function() {
                                $(this).dialog('close');
                            }
                        },
                        open:function() {
                            $('.ui-widget-overlay').css('background-image', 'none');
                        }
                    });

                    var waitDialog = $('<div id=\'""" + prefix + """waitDialog\'>Please Wait...</div>');
                    $('body').append(waitDialog);
                    $('#""" + prefix + """waitDialog').dialog({
                        modal: true,
                        autoOpen: false,
                        open:function() {
                            $('.ui-widget-overlay').css('background-image', 'none');
                        },
                        close:function() {
                            $('#""" + prefix + """waitDialogIsOpen').remove();
                        }
                    });""")

    getCssSelector = """jQuery.fn.getPath = function () {
                        if (this.length != 1) throw 'Requires one element.';

                        var path, node = this;
                        while (node.length) {
                            var realNode = node[0], name = realNode.localName;
                            if (!name) break;

                            name = name.toLowerCase();
                            if (realNode.id) {
                                // As soon as an id is found, there's no need to specify more.
                                return name + '#' + realNode.id + (path ? '>' + path : '');
                            } else if (realNode.className) {
                                name += '.' + realNode.className.split(/\s+/).join('.');
                            }

                            var parent = node.parent(), siblings = parent.children(name);
                            if (siblings.length > 1) name += ':nth-of-type(' + (siblings.index(node) + 1) + ')';
                            path = name + (path ? '>' + path : '');

                            node = parent;
                        }

                        return path;
                    };
                    return $(arguments[0]).getPath();"""

class Browser(webdriver.Chrome, webdriver.Firefox, webdriver.Ie):

    def __init__(self, browser, *args):
        if browser.lower() == "ie":
            webdriver.Ie.__init__(self)
            log("User opens IE browser.")
        elif browser.lower() == "chrome":
            if args: option = args[0]
            else: option = None
            log_level = DesiredCapabilities.CHROME
            log_level['loggingPrefs'] = {'browser': 'SEVERE'}
            webdriver.Chrome.__init__(self, desired_capabilities=log_level, chrome_options=option)
            log("User opens Chrome Browser")
        elif browser.lower() == "firefox":
            webdriver.Firefox.__init__(self)
            log("User opens Firefox Browser")
        self.action = webdriver.ActionChains(self)
        self.status = True
        self.cookie = ''

    def go(self, url):
        start = time.time()
        self.get(url)
        end = time.time() - start
        log("User opens URL: %s for %s seconds" % (url, round(end, 3)))
        self.check_console_errors()

    def in_html(self,substring):
        if substring in self.page_source:
            return True
        else:
            return False

    def switchtowindow(self, window):
        self.switch_to.window(self.window_handles[window])
        log("User switches to %d window" % window)

    def closewindow(self):
        self.close()
        log("Window is closed.")

    def closebrowser(self):
        self.quit()
        log("Browser is closed.")

    def maximize(self):
        self.maximize_window()
        log("The window is maximized.")

    def snapshot(self):
        path = os.path.dirname(__file__) + '/Log/'
        brand = ''
        try:
            for i in 'vulkan', 'mobile', 'admiral', 'sikuli':
                if i not in inspect.stack()[2][1]:
                    continue
                else:
                    brand = '%s/' % i
                    break
        except Exception:
            pass
        screen_dir = path + brand + time.strftime("%d.%m.%y") + "/"
        if not os.path.exists(screen_dir):
            os.makedirs(screen_dir)
        if inspect.currentframe().f_back.f_code.co_name == 'error':
            if inspect.stack()[2][3] == 'test':
                screen_name = inspect.stack()[3][3] + time.strftime(" %H.%M.%S") + ".png"
            else:
                screen_name = inspect.stack()[2][3] + time.strftime(" %H.%M.%S") + ".png"
        else:
            screen_name = inspect.currentframe().f_back.f_code.co_name + time.strftime(" %H.%M.%S") + ".png"
        self.get_screenshot_as_file(screen_dir + screen_name)
        print('<img class="hidden" src="%s">' % screen_name)

    def scroll_down(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def click(self, element, name):
        if element.lower() == 'id': elements = self.find_elements_by_id(name)
        elif element.lower() == 'name': elements = self.find_elements_by_name(name)
        elif element.lower() == 'class_name': elements = self.find_elements_by_class_name(name)
        elif element.lower() == 'text': elements = self.find_elements_by_xpath("//*[contains(text(), '%s')]" % name)
        elif element.lower() == 'xpath': elements = self.find_elements_by_xpath(name)
        else: log("Entered element is incorrect", 'red')
        if elements:
            for e in elements:
                try:
                    e.click()
                    if '*' in str(inspect.stack()[1][4]):
                        name = re.findall('[A-Z_]+', str(inspect.stack()[1][4]))[0]
                    log("User clicks on: %s" % name)
                    self.check_console_errors()
                    break
                except Exception:
                    if e == elements[-1]:
                        log("Can't click on element with %s : %s" % (element, name), 'red')
                        raise Error
        else:
            log("Can't find %s with name: %s" % (element, name), 'red')
            raise Error

    def type(self, element, name, text):
        if element.lower() == 'id': elements = self.find_elements_by_id(name)
        elif element.lower() == 'name': elements = self.find_elements_by_name(name)
        elif element.lower() == 'class_name': elements = self.find_elements_by_class_name(name)
        elif element.lower() == 'text': elements = self.find_elements_by_xpath("//*[contains(text(), '%s')]" % name)
        else: log("Entered element is incorrect", 'red')
        if elements:
            for e in elements:
                try:
                    e.click()
                    addtoclipboard(text)
                    e.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                    e.send_keys(Keys.CONTROL, 'v')
                    if '*' in str(inspect.stack()[1][4]):
                        name = re.findall('[A-Z_]+', str(inspect.stack()[1][4]))[0]
                    log("User types into: %s text: %s" % (name, text))
                    return e
                except Exception:
                    if e == elements[-1]:
                        log("Can't type on %s with name: %s" % (element, name), 'red')
                        raise Error
        else:
            log("Can't find %s with name: %s" % (element, name), 'red')
            raise Error


    def type2(self, element, name, text):
        if element.lower() == 'id': elements = self.find_elements_by_id(name)
        elif element.lower() == 'name': elements = self.find_elements_by_name(name)
        elif element.lower() == 'class_name': elements = self.find_elements_by_class_name(name)
        elif element.lower() == 'text': elements = self.find_elements_by_xpath("//*[contains(text(), '%s')]" % name)
        else: log("Entered element is incorrect", 'red')
        if elements:
            for e in elements:
                try:
                    e.click()
                    for letter in text:
                        e.send_keys(letter)
                        time.sleep(random.uniform(0.1,0.5))
                    e.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                    e.send_keys(Keys.CONTROL, 'v')
                    if '*' in str(inspect.stack()[1][4]):
                        name = re.findall('[A-Z_]+', str(inspect.stack()[1][4]))[0]
                    log("User types into: %s text: %s" % (name, text))
                    return e
                except Exception:
                    if e == elements[-1]:
                        log("Can't type on %s with name: %s" % (element, name), 'red')
                        raise Error
        else:
            log("Can't find %s with name: %s" % (element, name), 'red')
            raise Error

    def hover(self, element, name):
        if element.lower() == 'id': elements = self.find_elements_by_id(name)
        elif element.lower() == 'name': elements = self.find_elements_by_name(name)
        elif element.lower() == 'class_name': elements = self.find_elements_by_class_name(name)
        elif element.lower() == 'text': elements = self.find_elements_by_xpath("//*[contains(text(), '%s')]" % name)
        elif element.lower() == 'xpath': elements = self.find_elements_by_xpath(name)
        if elements:
            for e in elements:
                try:
                    self.action.move_to_element(e).perform()
                    time.sleep(1)
                    if '*' in str(inspect.stack()[1][4]):
                        name = str(inspect.stack()[1][4]).split('*')[-1].split(')')[0]
                    log("User hovers on: %s " % name)
                    return e
                except Exception:
                    if e == elements[-1]:
                        log("Can't hover on %s with text: %s" % (element, name), 'red')
                        raise Error
        else:
            log("Can't find %s with name: %s" % (element, name), 'red')
            raise Error

    def waitfor(self, element, name, delay=10):
        try:
            start = time.time()
            if element.lower() == 'id': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.ID, name)))
            elif element.lower() == 'name': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.NAME, name)))
            elif element.lower() == 'class_name': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.CLASS_NAME, name)))
            elif element.lower() == 'text': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.XPATH, "//*[contains(text(), '%s')]" % name)))
            else: log("Entered element is incorrect", 'red')
            end = time.time() - start
            if '*' in str(inspect.stack()[1][4]):
                name = re.findall('[A-Z_]+', str(inspect.stack()[1][4]))[0]
            log("User waits for: %s %s seconds" % (name, round(end, 3)))
        except Exception:
            log("%s: %s wasn't shown in %d seconds" % (element, name, delay), 'red')
            raise Error

    def exists(self, element, name, delay=10, reverse=0):
        if reverse == 0:
            pos = 'green'
            neg = 'red'
        else:
            pos = 'red'
            neg = 'green'
        try:
            if element.lower() == 'id': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.ID, name)))
            elif element.lower() == 'name': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.NAME, name)))
            elif element.lower() == 'class_name': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.CLASS_NAME, name)))
            elif element.lower() == 'text': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.XPATH, "//*[contains(text(), '%s')]" % name)))
            elif element.lower() == 'xpath': WebDriverWait(self, delay).until(ec.element_to_be_clickable((By.XPATH, name)))
            else: log("Entered element is incorrect", 'red')
            if '*' in str(inspect.stack()[1][4]):
                name = re.findall('[A-Z_]+', str(inspect.stack()[1][4]))[0]
            log("%s: exists" % name, color=pos)
            return True
        except Exception:
            log("%s: %s doesn't exist" % (element, name), color=neg)
            return False

    def count(self, element, name, displayed=1):
        count = 0
        if element.lower() == 'id': elements = self.find_elements_by_id(name)
        elif element.lower() == 'name': elements = self.find_elements_by_name(name)
        elif element.lower() == 'class_name': elements = self.find_elements_by_class_name(name)
        elif element.lower() == 'text': elements = self.find_elements_by_xpath("//*[contains(text(), '%s')]" % name)
        else: log("Entered element is incorrect", 'red')
        if elements:
            if displayed:
                for e in elements:
                    if not e.is_displayed():
                        continue
                    count += 1
            else:
                count = len(elements)
        return count

    def find_all(self, element, name):
        if element.lower() == 'id': elements = self.find_elements_by_id(name)
        elif element.lower() == 'name': elements = self.find_elements_by_name(name)
        elif element.lower() == 'class_name': elements = self.find_elements_by_class_name(name)
        elif element.lower() == 'text': elements = self.find_elements_by_xpath("//*[contains(text(), '%s')]" % name)
        elif element.lower() == 'xpath': elements = self.find_elements_by_xpath(name)
        else: log("Entered element is incorrect", 'red')
        if elements:
            return [x for x in elements if x.is_displayed()]
        else:
            log("Can't find %s with name: %s" % (element, name), 'red')
            raise Error

    def save_cookie(self, cookie):
        self.cookie = self.get_cookie(cookie)['value']


    def get_cookie_dict(self):
        cookies_dict = {}
        cookies_list = self.get_cookies()
        for cookie in cookies_list:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict


    def close_popup(self):
        popup = self.find_all('class_name', 'popup-close')[0]
        try:
            while popup.is_displayed():
                popup.click()
                time.sleep(0.1)
        except Exception:
            pass
        log('Popup closed')

    def error(self, *message):
        if message:
            log(message, 'red')
        self.status = False
        self.snapshot()
        return self.status

    def warning(self, *message):
        if message:
            log(message, 'yel')
        self.status = False
        return self.status

    def check_console_errors(self):
        errors = self.get_log('browser')
        if errors:
            for i in errors:
                log_console_errors("Console error: %s" % i['message'])



    def load_jquery(self, filename="jquery.min.js"):
        jqfile = open(filename, 'r')
        jqueryLoad = jqfile.read()
        jqfile.close()
        self.execute_script(jqueryLoad)


    def select_option(self, element, name, text):
        if element.lower() == 'id': elements = self.find_elements_by_id(name)
        elif element.lower() == 'name': elements = self.find_elements_by_name(name)
        elif element.lower() == 'class_name': elements = self.find_elements_by_class_name(name)
        elif element.lower() == 'text': elements = self.find_elements_by_xpath("//*[contains(text(), '%s')]" % name)
        else: log("Entered element is incorrect", 'red')
        if elements:
            for e in elements:
                try:
                    eselect = Select(e)
                    e.click()
                    options = eselect.options
                    for option in options:
                        try:
                            loweroption = option.text.lower()
                        except:
                            loweroption = option.text
                        if text.lower() == loweroption:
                            option.click()


                    return e
                except Exception:
                    if e == elements[-1]:
                        log("Can't type on %s with name: %s" % (element, name), 'red')
                        raise Error
        else:
            log("Can't find %s with name: %s" % (element, name), 'red')
            raise Error

    def hover_type(self,element,name,text):
        self.hover(element,name,)
        time.sleep(random.uniform(1,2))
        self.type2(element,name,text)

    def select_value(self, element, name, value):
        if element.lower() == 'id': elements = self.find_elements_by_id(name)
        elif element.lower() == 'name': elements = self.find_elements_by_name(name)
        elif element.lower() == 'class_name': elements = self.find_elements_by_class_name(name)
        elif element.lower() == 'text': elements = self.find_elements_by_xpath("//*[contains(text(), '%s')]" % name)
        else: log("Entered element is incorrect", 'red')
        if elements:
            for e in elements:
                try:
                    eselect = Select(e)
                    e.click()
                    options = eselect.options
                    for option in options:
                        if value in  option.get_attribute('value'):
                            option.click()


                    return e
                except Exception:
                    if e == elements[-1]:
                        log("Can't type on %s with name: %s" % (element, name), 'red')
                        raise Error
        else:
            log("Can't find %s with name: %s" % (element, name), 'red')
            raise Error

    def inject_jquery(self):
        jq = requests.get("https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js").text
        self.execute_script(jq)
    def set_text(self, selector, text):
        self.inject_jquery(self)
        self.execute_script("""jQuery("%s").text("%s")""" % (selector, text))
    def set_value(self, selector, value):
        self.inject_jquery(self)
        self.execute_script("""jQuery("%s").val("%s")""" % (selector, value))
    def get_text_from_id(self, id):
        return self.find_element_by_id(id).text
    def get_text_from_class(self, class_name):
        return self.find_element_by_class_name(class_name).text
    def get_value_from_id(self, id):
        return self.find_element_by_id(id).get_attribute('value')
    def get_value_from_class(self, class_name):
        return self.find_element_by_class_name(class_name).get_attribute('value')
    def trigger(self,class_name):

        js_scripts ='''$('.'''+class_name+'''').trigger('touchstart');'''
        end_js_scripts ='''$('.'''+class_name+'''').trigger('touchend');'''
        try:
            self.browser.execute(js_scripts)
        except:
            pass
        time.sleep(2)
        try:
            self.browser.execute(end_js_scripts)
        except:
            pass
def addtoclipboard(text):
    if 'Windows' in platform.platform():
        command = 'echo ' + text.strip() + '| clip'
    else:
        command = 'echo ' + text.strip() + '| xclip -d :0 -selection clipboard'
    os.system(command)


def log(message, color='green'):
    if color.lower() == 'red': template = '<span class="error" style="color:red">%s</span>'
    elif color.lower() == 'yel': template = '<span style="color:orange">%s</span>'
    else: template = '<span style="color:green">%s</span>'
    print(template % message)


def log_console_errors(message):
    template = '<span class="console_error" style="color:blue">%s</span>'
    print(template % message)


class Error(Exception):
    pass


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

'''
chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option("mobileEmulation", iphone_emulator)
mobile = Browser('Chrome', chrome_options)
mobile.go('http://yahoo.com')
mobile.waitfor('text','✉')
mobile.click('text','✉')
mobile.waitfor('text','mobile site')
mobile.click('text','mobile site')
mobile.waitfor('text','Sign up for a new account')
mobile.click('text','Sign up for a new account')
mobile.load_jquery()
for x in mobile.find_elements_by_tag_name('input'):
    print x.get_attribute('name')

mobile.type2('name','firstName','Jordan')
mobile.type2('name','lastName','James')
mobile.hover('id','usernamereg-yid')
mobile.type2('id','usernamereg-yid','JamesJamesoopa')
mobile.hover('id','usernamereg-password')

mobile.type2('id','usernamereg-password','Deskjet123$')

mobile.hover('name','phone')
mobile.type2('name','phone','15735983670')

mobile.select_option('name','mm','April')
mobile.select_option('name','yyyy','1991')


mobile.select_option('name','dd','4')

mobile.select_option('name','gender','gender')
mobile.click('id','reg-submit-button')

if mobile.exists('name','sendCode'):
    mobile.click('name','sendCode')

if mobile.exists('name','code'):
    mobile.hover('name','code')
    mobile.type2('name','code','')
    mobile.hover('name','verifyCode')
    mobile.click('name','verifyCode')
#https://github.com/wfight/Grab/blob/e260ffe195cd5c994a6b524cbc8487f6514e68cc/liantong.py
#https://github.com/PSUPing/AndroidWA

'''

#mobile.find_element_by_partial_link_text('https://mail.yahoo.com/?.intl=us&.lang=en-US&.src=ym')