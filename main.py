import mailbox
import sys
import email
import os
import glob
import shutil

def stringConversion(inpString):
    stringList = []
    splittedString = inpString.split(" ")
    for i in splittedString:
        if (splittedString.count(i)>=1 and i not in stringList):
            stringList.append(i.lower())
    return stringList 

path = []
for root, dirs, files in os.walk("C:\\Users\\varsh\\Downloads\\enron (1)\\enron"):
    if files:
        for i in files:
            path.append(root + "\\" + i)
            
stringInput = input()

if "enron_search term_search " in stringInput:
    x = stringInput.replace("enron_search term_search ", "")
    y = stringConversion(x)
    messages = []
    k=0
    s = ""
    for m in path:
        mbox_file = mailbox.mbox(m)
        for i, mes in enumerate(mbox_file):
            flag = 0
          
            if mes.is_multipart():
                content = ''.join(part.get_payload(decode=True) for part in mes.get_payload())
            else:
                content = str(mes.get_payload(decode=True))

            for term in y:
                if not term in content.lower():
                    flag = 1
                    break

            # Prints the message if all the terms are present in the list
            if flag != 1:
                if type(mes['X-From']) != type(s):
                    s = str(mes['X-From'])
                    m = (str(k+1)+". "+s + " <" + mes['from'] + ">  " + mes['date'])
                    messages.append(m)
                    k+=1
                    print(m)
                    print(1)
                else:
                    m = (str(k+1)+". "+mes['X-From'] + " <" + mes['from'] + ">  " + mes['date'])
                    messages.append(m)
                    k+=1
                    print(m)
    print("Results found are: " + str(k))

# Checks if the command line arguments contains string s2
elif "enron_search address_search " in stringInput:
    x = stringInput.replace("enron_search address_search ", "")
    y = stringConversion(x)
    # for i in path:
    name = []
    name.append(y[0])
    name.append(y[1])
    mails = []
    k = 0
    s = ""

    for m in path:
        mbox = mailbox.mbox(m)
        for l, mes in enumerate(mbox):
            flag = 0
            from_address = mes['X-From']
            for l in name:
                if from_address is not None and type(from_address) == type(s):
                    if not l in from_address.lower():
                        flag = 1
                        break
                elif from_address is None or type(from_address) != type(s):
                    flag = 1
                    break
            if flag != 1 and (not mes['from'] in mails):
                mails.append(mes['from'])
                print(str(k + 1) + ". " + mails[k])
                k += 1
    print("Results found: " + str(k))

# Checks if the command line arguments contains string s3
elif "enron_search interaction_search " in stringInput:
    x = stringInput.replace("enron_search interaction_search ", "")
    y = stringConversion(x)
    messages = []
    k = 0
    for m in path:
        mbox = mailbox.mbox(m)
        for i, mes in enumerate(mbox):
            if (mes['from'] == y[0] and mes['to'] == y[1]):

                messages.append(mes)
                print(
                    str(k + 1) + ". " + y[0] + " --> " + y[1] + " [Subject: " + mes['subject'] + "] " + mes[
                        'date'])
                k += 1
            elif (mes['from'] == y[1] and mes['to'] == y[0]):
                messages.append(mes)
                print(
                    str(k + 1) + ". " + y[1] + " --> " + y[0] + " [Subject: " + mes['subject'] + "] " + mes[
                        'date'])
                k += 1

    print("Results found: " + str(k))
