import csv

# Initialize lists
uniCountryList = []
uniCapitalList = []

# Class for the output file
class OutputFile:

    # Constructor, initializes objects
    def __init__(self, fileName, mode):
        self.fileName = fileName
        self.mode = mode
        self.uniInfo = open(fileName, mode)

    # The following three functions allows for writing, closing and flushing the file
    def write(self, string):
        self.uniInfo.write(string)

    def close(self):
        self.uniInfo.close()

    def flush(self):
        self.uniInfo.flush()

# Class to read and cleanup the CSV files
class CSVData:
    # Constructor, initializes objects
    def __init__(self, rankingFileName, capitalFileName):
        self.rankingFileName = rankingFileName
        self.capitalFileName = capitalFileName
        self.uniData = self.cleanUpFile()
        self.capitalData = self.cleanupContinents()
        self.uniDataCapital = self.cleanUpCapital()

    # Getter for uniData list, allowing other functions to access uniData from cleanUpFile,
    # which cleans up TopUni.csv
    def getUniData(self):
        return self.uniData

    # Getter for capitalData list, allowing other functions to access capitalData from cleanUpContinents,
    # which cleans up capitals.csv
    def getCapitalData(self):
        return self.capitalData

    # Getter for uniDataCapital list, allowing other functions to access uniDataCapital from cleanUpFile,
    # which merges the useful elements from TopUni.csv and capitals.csv
    def getUniDataCapital(self):
        return self.uniDataCapital

    # Removes unused columns in TopUni.csv and puts into a uniData list
    def cleanUpFile(self):
        try:
            with open(self.rankingFileName, "r", newline="") as f:
                reader = csv.reader(f)
                uniData = list(reader)
                for column in uniData:
                    del column[4:8]
                del uniData[0]

                print(uniData)
                return uniData
        except:
            print("file not found")

    # Removes unused columns in capitals.csv and puts into a uniData list
    def cleanupContinents(self):
        try:
            with open(self.capitalFileName, "r", newline="") as f:
                reader = csv.reader(f)
                capitalData = list(reader)
                for column in capitalData:
                    del column[2:5]
                del capitalData[0]

                print(capitalData)
                return capitalData
        except:
            print("file not found")

    # Adds uniData and the respective capitals and continents to a new uniDataCapital list
    def cleanUpCapital(self):
        uniDataCapital = self.uniData.copy()
        for uniList in uniDataCapital:
            for capital in self.capitalData:
                if capital[0] == uniList[2]:
                    uniList.append(capital[1])
            for continent in self.capitalData:
                if continent[0] == uniList[2]:
                    uniList.append(continent[2])
        print(uniDataCapital)
        return uniDataCapital

# ...
def uniNum(uniInfo, cleanData):
    totalUni = (cleanData.getUniData()[-1][0])
    uniInfo.write("Total number of universities => {}".format(totalUni))


def countriesAndConts(uniInfo, cleanData):
    # Loops through uniData and adds unique values to list of countries
    for uniCountry in cleanData.getUniData():
        if uniCountry[2] not in uniCountryList:
            uniCountryList.append(uniCountry[2])
            # Loops through the countries that were added to uniCountryList in previous block
    for country in uniCountryList:
        # Loops through capitals and find corresponding continent for the uniCountryList
        for capital in cleanData.getCapitalData():
            if country == capital[0]:
                if capital[2] not in uniCapitalList:
                    uniCapitalList.append(capital[2])
    uniInfo.write("\nAvailable countries => {}".format(uniCountryList).upper())
    uniInfo.write("\nAvailable continents => {}".format(uniCapitalList).upper())


def uniRanks(selectedCountry, uniInfo, cleanData):
    # global userCountryRank
    userCountryRank = 100
    # selectedCountry = input("Please enter the country name: ").upper()
    for rank in cleanData.getUniData():
        if rank[2].upper() == selectedCountry.upper():
            if userCountryRank > int(rank[0]):
                userCountryRank = int(rank[0])
                # global topUniName
                topUniName = rank[1]

    # global userNationalRank
    userNationalRank = 1
    for rank in cleanData.getUniData():
        if rank[2].upper() == selectedCountry.upper():
            if userNationalRank == int(rank[3]):
                # global topNatUniName
                topNatUniName = rank[1]
    uniInfo.write("\nAt international rank => {} the university name is => {}".format(userCountryRank, topUniName).upper())
    uniInfo.write("\nAt national rank => {} the university name is => {}".format(userNationalRank, topNatUniName).upper())


def averageScore(selectedCountry, uniInfo, cleanData):
    numUniNat = 0
    avgScoreUni = 0
    continent = []
    continentHighScore = 0
    for score in cleanData.getUniData():
        if score[2].upper() == selectedCountry.upper():
            numUniNat += 1
            avgScoreUni += round(float(score[4]), 1)
    avg = avgScoreUni / numUniNat

    for country in cleanData.getUniDataCapital():
        if country[2].upper() == selectedCountry.upper():
            continent = country[6]
    for country in cleanData.getUniDataCapital():
        if country[6].upper() == continent.upper():
            if float(country[4]) > float(continentHighScore):
                continentHighScore = country[4]

    relScore = round(avg/float(continentHighScore)*100.00,2)

    uniInfo.write("\nThe average score => {}%".format(avg))
    uniInfo.write("\nThe relative score to the top university in {} is => ({} / {}) x 100% = {}%".format(continent.upper(), avg, float(continentHighScore), relScore))

def capitalCity(selectedCountry, uniInfo, cleanData):
    capital = []
    for country in cleanData.getCapitalData():
        if country[0].upper() == selectedCountry.upper():
            capital = country[1]

    uniInfo.write("\nThe capital is => {}".format(capital).upper())

def containCapital(selectedCountry, uniInfo, cleanData):
    capitalUniNames = []
    univWithRank = []
    capital = []
    increment = 1
    for country in cleanData.getCapitalData():
        if country[0].upper() == selectedCountry.upper():
            capital = country[1]
    for uni in cleanData.getUniDataCapital():
        if str(capital.upper()) in uni[1].upper():
            univWithRank.append("#" + str(increment))
            univWithRank.append(uni[1])
            capitalUniNames.append(univWithRank)
    print(capitalUniNames)


    uniInfo.write("\nThe universities that contain the capital name => {}".format(capitalUniNames).upper())
    uniInfo.close()


def getInformation(selectedCountry, rankingFileName, capitalsFileName):
    uniInfo = OutputFile("output.txt", "w")
    cleanData = CSVData(rankingFileName, capitalsFileName)
    uniNum(uniInfo, cleanData)
    countriesAndConts(uniInfo, cleanData)
    uniRanks(selectedCountry, uniInfo, cleanData)
    averageScore(selectedCountry, uniInfo, cleanData)
    capitalCity(selectedCountry, uniInfo, cleanData)
    containCapital(selectedCountry, uniInfo, cleanData)


#
# getInformation("japan", "TopUni.csv", "capitals.csv")
getInformation("USA", "TopUni.csv", "capitals.csv")
