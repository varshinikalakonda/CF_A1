import mailbox
import sys
import email
import os
import glob
import shutil

#formating the input string by removing duplicates and coverting the entire string to lower case 
def stringConversion(inpString):
    stringList = []
    splittedString = inpString.split(" ")
    for i in splittedString:
        if (splittedString.count(i)>=1 and i not in stringList):
            stringList.append(i.lower())
    return stringList 

#storing all the paths of the files into a list called path
path = []
for root, dirs, files in os.walk("C:\\Users\\varsh\\Downloads\\enron (1)\\enron"):
    if files:
        for i in files:
            path.append(root + "\\" + i)

#our complete input is stored in stringInput           
stringInput = input()

#This is the first functionality where we are searching for a term 
if "enron_search term_search " in stringInput:
    #taking only term value
    x = stringInput.replace("enron_search term_search ", "")
    #sending the term value to strinConversion function and formating it
    y = stringConversion(x)
    messages = []
    k=0
    s = ""
    for m in path:
        #we are converting all the files into mbox format 
        mbox_file = mailbox.mbox(m)
        for i, mes in enumerate(mbox_file):
            flag = 0
          #trying to extract only content from the entire mail
            if mes.is_multipart():
                content = ''.join(part.get_payload(decode=True) for part in mes.get_payload())
            else:
                content = str(mes.get_payload(decode=True))
            #checking if input terma are there in the content or not
            for term in y:
                if not term in content.lower():
                    flag = 1
                    break

            # prints details of the messages if the given terms are there in the mails
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

#this is the second functionality where we are searching for an address of a given person
elif "enron_search address_search " in stringInput:
    x = stringInput.replace("enron_search address_search ", "")
    y = stringConversion(x)
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
            #getting the name of the person from the mails
            from_address = mes['X-From']
            for l in name:
                if from_address is not None and type(from_address) == type(s):
                    #comparing if the person name matches with the input given name
                    if not l in from_address.lower():
                        flag = 1
                        break
                elif from_address is None or type(from_address) != type(s):
                    flag = 1
                    break
            # if name matches we are taking the email address of that person
            if flag != 1 and (not mes['from'] in mails):
                mails.append(mes['from'])
                print(str(k + 1) + ". " + mails[k])
                k += 1
    print("Results found: " + str(k))

#this is the third functionality where we are searching for all the interaction mails between the given persons
elif "enron_search interaction_search " in stringInput:
    x = stringInput.replace("enron_search interaction_search ", "")
    y = stringConversion(x)
    messages = []
    k = 0
    for m in path:
        mbox = mailbox.mbox(m)
        for i, mes in enumerate(mbox):
            #checking if the from address is eual to first input mail and to address is eual to second input name
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
