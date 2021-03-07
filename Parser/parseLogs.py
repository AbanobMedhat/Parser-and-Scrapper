import re

# Functions
# Extract IPs


def generalIpExt(lines, patternIPS):
    try:
        print("Ips: ")
        newFile = open("IPS.txt", "w+")
    except OSError:
        print("Can not open the file")
    for line in lines:
        result = patternIPS.findall(line)
        if len(result) > 0:
            # print(len(result))
            for i in result:
                print(i)
                try:
                    newFile.write(i+"\n")
                except OSError:
                    print("Can not write the file")
    try:
        newFile.close()
    except OSError:
        print("Can not close the file")

# Extract Methouds


def generalMethodsExt(lines, patternMethods):
    try:
        print("Methods: ")
        newFile = open("Methouds.txt", "w+")
    except OSError:
        print("Can not open the file")
    for line in lines:
        result = patternMethods.findall(line)
        if len(result) > 0:
            for i in result:
                try:
                    newFile.write(i+"\n")
                    print(i)
                except OSError:
                    print("Can not write the file")
    try:
        newFile.close()
    except OSError:
        print("Can not close the file")

# Extract URIs


def generalURIExt(lines, patternURIs):
    try:
        print("URIs")
        newFile = open("URIs.txt", "w+")
    except OSError:
        print("Can not open the file")
    for line in lines:
        if "]" in line:
            minValue = (line.index("]"))
            if "?" not in line:
                maxValue = (line.index("HTTP"))
            else:
                maxValue = (line.index("?"))

            trimmedLine = line[minValue:maxValue]
            result = patternURIs.findall(trimmedLine)

            if len(result) > 0:
                for i in result:
                    try:
                        newFile.write(i+"\n")
                        print(i)
                    except OSError:
                        print("Can not write on the file")
    try:
        newFile.close()
    except OSError:
        print("Can not close the file")

# Extract Agents (UNIQUE)
def genearlUniAgent(lines, pattern):
    uniqueList = []
    try:
        print("Agents: ")
        newFile = open("Agents.txt", "w+")
    except OSError:
        print("Can not open the file")
    for line in lines:
        result = pattern.findall(line)
        if len(result) > 0:
            # print((result))
            for i in result:
                if i[0] not in uniqueList:
                    uniqueList.append(i[0])
                    try:
                        newFile.write(i[0]+"\n")
                        print(i)
                    except OSError:
                        print("Can not write the file")
    try:
        newFile.close()
    except OSError:
        print("Can not close the file")

# Extract from Input IP


def extractReq(lines, patternIPS, userIP):
    for line in lines:
        ipTemp = patternIPS.findall(line)
        if len(ipTemp) > 0:
            if ipTemp[0] == userIP:
                print(line)

# Extract from Input Status Request


def statusReq(patternStatus, status, lines):
    for line in lines:
        outReqs = patternStatus.findall(line)
        if len(outReqs) > 0 and int(outReqs[0][1]) == status:
            print(line)

# Our main Function


def main():
    # patterns

    patternIPS = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    patternInpIPS = re.compile(r"(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$)")
    patternMethods = re.compile(r"(GET|POST|OPTIONS|PUT|DELETE|TRACE|PATCH)")
    patternAgents = re.compile(r"((Chrome|Mozilla|AppleWebKit|Safari)\S+)")
    patternURIs = re.compile(r"(\/\S+)")
    patternStatus = re.compile(r"(\"\s(200|404|301))")
    patternInpStatus = re.compile(r"([1-3])")

    # arrays
    statusCode = [200, 301, 404]
    try:
        # Open Log File
        logFile = open("access.log", "r")
        lines = logFile.readlines()
    except OSError:
        print("Can not open the file")

    # Function Calls
    generalIpExt(lines, patternIPS)
    generalMethodsExt(lines, patternMethods)
    generalURIExt(lines, patternURIs)
    genearlUniAgent(lines, patternAgents)

    # user interaction part
    choice = "y"
    while choice == "y":
        userIp = input("Please enter your Ip \n")
        ipValidate = patternInpIPS.findall(userIp)
        if len(ipValidate) > 0:
            extractReq(lines, patternIPS, userIp)
        else:
            print("Wrong Ip")
        choice = input("do u want to enter another IP? y or n \n").lower()

    # choose your status code
    choice = "y"
    while choice == "y":
        print("Choose status code: ")
        for i in range(0, 3):
            print(str(i + 1) + ": " + str(statusCode[i]))
        inpStatus = int(input("your choice: \n"))
        statusValidate = patternInpStatus.findall(str(inpStatus))
        if len(statusValidate) > 0:
            statusReq(patternStatus, statusCode[inpStatus - 1], lines)
        else:
            print("Wrong Input")
        choice = input("do u want to enter another status? y or n \n").lower()
    # Close Log File
    logFile.close()

# Call Main Function


main()
