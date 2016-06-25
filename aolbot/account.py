import datetime
import random
import time
from random import sample,choice

from helpers import readInNames
import phone
from faker import Faker

ALPHNUM = (
        'abcdefghijklmnopqrstuvwxyz' + \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + \
        '01234567890'
    )

class Account:
    'Variables common to all facebookAccount classes'
    boysFirstNames = readInNames('input/maleNames.txt')
    girlsFirstNames = readInNames('input/femaleNames.txt')
    lastNames = readInNames('input/lastNames.txt')
    oldestAcceptableAge = 55
    youngestAcceptableAge = 35
    def __init__(self,email=None,password=None,intnum=None,usnum=None):
        self.gender = choice([0, 1])
        self.firstName = self.getFirstName()
        self.lastName = self.getLastName()
        self.email =  email
        if password == None:
            self.passWord = self.generate()+"$!"
        else:
            self.passWord = password
        self.birthMonth = self.getBirthMonth()
        monthDict={1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        self.birthMonthString = monthDict[int(self.birthMonth)]
        self.birthDay = str(self.getBirthDay())
        self.birthYear = str(self.getBirthYear())
        self.intnumber = intnum
        self.usnumber = usnum
        self.postal_code = str(random.randint(20000,95000))
        self.city = self.genCity()
        self.aol_id = ''
        self.security_answer = ''
    def genCity(self):
        cities = [ "Hollywood",'Los Angeles','Austin','New York','Houston','Seattle','Las Vegas','New Orleans','Miami']
        self.security_answer = random.choice(cities)
        return self.security_answer

    def getFirstName(self):
        if self.gender == 0:
            firstName = random.choice(Account.boysFirstNames)
        elif self.gender == 1:
            firstName = random.choice(Account.girlsFirstNames)
        return firstName

    def getLastName(self):
        lastName = random.choice(Account.lastNames)
        return lastName

    def generate(self,count=1, length=12, chars=ALPHNUM):
        if count == 1:
            return ''.join(sample(chars, length))
        passwords = []
        while count > 0:
            passwords.append(''.join(sample(chars, length)))
            count -= 1
        return passwords


    def getBirthMonth(self):
        monthList = [x+1 for x in list(range(12))]
        chosenMonth = random.choice(monthList)
        return chosenMonth

    def getBirthDay(self):
        dayList = [x+1 for x in list(range(28))]
        chosenDay = random.choice(dayList)
        return chosenDay

    def getBirthYear(self):
        currentYear = int(str(datetime.datetime.now()).split('-')[0])
        oldestAcceptableYear = currentYear - Account.oldestAcceptableAge
        newestAcceptableYear = currentYear - Account.youngestAcceptableAge + 1
        yearList = range(oldestAcceptableYear, newestAcceptableYear)
        chosenYear = random.choice(yearList)
        return chosenYear
