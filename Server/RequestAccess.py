from datetime import datetime
from datetime import timedelta
import os

firstRunFile = "/home/tgc/EoLAccess.txt"
toEmail = "tom@cousin.uk"
fromEmail = "noreply@cousin.me.uk"
dateFormat = "%d/%m/%Y-%H:%M:%S"
daysToUnlock = 7
accessCode = "ABC"


def sendNotification():
    willUnlock = datetime.now() + timedelta(days=daysToUnlock)
    emailContent =  "Subject: WARNING: EoL Access Script Executed\\n"
    emailContent += "From: " + fromEmail + "\\n"
    emailContent += "To: " + toEmail + "\\n\\n"
    emailContent += "The EoL Access Script was executed at: " + datetime.now().strftime(dateFormat) + "\\n"
    emailContent += "Without an action access will be granted at: " + willUnlock.strftime(dateFormat) + "\\n"
    command = "echo \"" + emailContent + "\" | sendmail " + toEmail
    os.system(command)

def checkIsFirstRun() -> bool:
    result = False
    try:
        f = open(firstRunFile)
        f.close()
    except IOError:
        result = True
    return result

def createFirstRunFile():
    f = open(firstRunFile, "a")
    f.write(datetime.now().strftime(dateFormat))
    f.close()
    willUnlock = datetime.now() + timedelta(days=daysToUnlock)
    print("Access code avalible at: " + willUnlock.strftime(dateFormat))

def checkEnoughTimePassed() -> bool:
    try:
        with open(firstRunFile) as f:
            file_content = f.read()
            file_content = file_content.replace("\n","")
            if datetime.strptime(file_content, dateFormat) < (datetime.now() + timedelta(days=daysToUnlock)):
                return True
    except IOError:
        print("Error While Reading File, Writing New File")
        return False

    return False

def runEnoughTimePassedActions():
    print("Access code is:")
    print(accessCode)

def run():
    # try:
    #     sendNotification()
    # except:
    #     pass

    if checkIsFirstRun() == True:
        createFirstRunFile()
        print("First run")
        return
    
    if checkEnoughTimePassed() == True:
        print("Waiting Period Passed")
        runEnoughTimePassedActions()
        return
    
    print("Still In Waiting Period")

if __name__ == "__main__":
    print("Running")
    run()