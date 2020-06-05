#!/usr/bin/python3
#################################################################
# Email Validator v1.0                                          #
# By: Carlos Alvarez del Castillo <psykher[AT]gmail.com>        #
# Verify if email addresses are valid by checking SMTP server   #
#################################################################

import re, sys, smtplib

#Check if pythondns libraries exist and import them
try:
    import dns.resolver
except Exception as exc:
    print('EmailValidator requires "pythondns" libraries')
    print(exc)
    quit()

#Address used for SMTP MAIL FROM command
fromAddress = 'test@google.com'

#Check the syntax
def checkSyntax(emailAddress):
    try:
        regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
        addressToVerify = str(emailAddress)

        match = re.match(regex, addressToVerify)
        if match == None:
            print(emailAddress + ' is not a valid email address')
            return -1
        else:
            return addressToVerify
    except Exception as exc:
        print(emailAddress + ' is not a valid email address')
        print(exc)
        return -1

#Get domain for DNS lookup
def getHost(emailAddress):
    try:
        return emailAddress.split('@')[1]
    except Exception as exc:
        print(emailAddress + ' is not a valid email address')
        print(exc)
        return -1

#DNS MX records lookup
def resolveMX(emailHost):
    global hostItems
    hostDict={}
    try:
        records = dns.resolver.query(emailHost, 'MX')
    except Exception as exc:
        print('Could not extract records from host.')
        print(exc)
        return -1
    for r in records:
        hostDict[r.exchange] = r.preference
    hostItems = list(hostDict.items())
    hostItems.sort()

#Email user lookup
def checkEmail(emailAddress):
    result = True
    code = 400
    smtp = smtplib.SMTP()
    smtp.set_debuglevel(0)
    for x in hostItems:
        try:
            host = x[0][:-1]
            host = b'.'.join(host).decode("utf-8")
            print(host)
            connectLog = smtp.connect(host)
            heloLog = smtp.helo(smtp.local_hostname)
        except Exception as exc:
            print(exc)
            continue
        else:
            result = False
            break
    if result:
        print('Could not resolve any hosts for: ' + emailAddress)
        return -1
    try:
        smtp.mail(fromAddress)
        code, message = smtp.rcpt(emailAddress)
        smtp.quit()
        print(code)
    except Exception as exc:
        print('Email is not valid.')
        print(exc)
    else:
        if code == 250:
            print('Email: ' + emailAddress + ' is valid!')
            validList.append(emailAddress)
        else:
            print('Email is not valid.')

def printHelp():
    print('')
    print('Verify if email addresses are valid by checking SMTP server\n')

    print('Usage:\n\tpython3 emailValidator.py -e <email> -v\n')
    print('Arguments:\n')
    print(' -h or --help','This help'.rjust(28))
    print(' -v or --verbose','Increases verbosity'.rjust(35))
    print(' -e or --email <email>','Specify one email address to check'.rjust(44))
    print(' -f or --file <file>','Specify a file of emails delimeted by line'.rjust(54))
    print('\nExample:\n\tpython3 emailValidator.py -e admin@example.org -v')
    print('\tpython3 emailValidator.py --file emails.txt\n')
    quit()

verbose=False
suppliedInput = 0
validList = []

if not (len(sys.argv) == 3 or len(sys.argv) == 4):
    printHelp()
for i in range(1,len(sys.argv)):
    if sys.argv[i] == '-h' or sys.argv[i] == '--help':
        printHelp()
    elif sys.argv[i] == '-v' or sys.argv[i] == '--verbose':
        verbose=True
        continue
    elif sys.argv[i] == '-e' or sys.argv[i] == '--email':
        if suppliedInput == 0:
            inputEmail = sys.argv[i+1]
            suppliedInput = 1
        else:
            printHelp()
    elif sys.argv[i] == '-f' or sys.argv[i] == '--file':
        if suppliedInput == 0:
            inputFile = sys.argv[i+1]
            suppliedInput = 2
        else:
            printHelp()

try:
    if suppliedInput == 0:
        printHelp()
    elif suppliedInput == 1:
        if not checkSyntax(inputEmail) == -1:
            host = getHost(inputEmail)
            if not host == -1:
                if not resolveMX(host) == -1:
                    checkEmail(inputEmail)
    elif suppliedInput == 2:
        try:
            file = open(inputFile,'r')
        except Exception as exc:
            print('Could not open "' + inputFile + '" for reading')
            output(exc)
            quit()
        else:
            for email in file:
                email = email.replace('\n','')
                print('Checking: ' + email)
                if not checkSyntax(email) == -1:
                    host = getHost(email)
                    if host == -1:
                        continue
                    elif resolveMX(host) == -1:
                        continue
                    elif checkEmail(email) == -1:
                        continue
except KeyboardInterrupt:
    print('Keyboard Interrupt Detected.')

if validList:
    print('\nValid Emails: \n==========')
    for item in validList:
        print(item)
    print('')
