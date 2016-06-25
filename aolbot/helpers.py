from bs4 import  BeautifulSoup
import time
import random
def extract( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""




def extract_form_fields( soup):
    "Turn a BeautifulSoup form in to a dict of fields and default values"
    fields = {}
    for input in soup.findAll('input'):


        # single element nome/value fields
        if input['type'] == 'hidden':
            value = ''
            if input.has_attr('value'):
                value = input['value']
            fields[input['name']] = value
            continue




    return fields


def extract_field(soup,fieldname):
    "Turn a BeautifulSoup form in to a dict of fields and default values"
    fields = {}
    for input in soup.findAll('input'):


        # single element nome/value fields
        if input['type'] == 'hidden':
            value = ''
            if input['name']==fieldname:

                if input.has_attr('value'):
                    value = input['value']
                fields[input['name']] = value
                continue

def readInNames(fileName):
    nameList = []
    with open( fileName, "r") as ifile:
        for line in ifile:
            name = line.rstrip()
            nameList.append(name)
    return nameList

def sleepy(f1=1,f2=2):
    time.sleep(random.uniform(f1,f2))