import csv, json, sys, os
from os.path import isfile, join

class Park(object):
	def __init__(self, name):
		self.name = name
		self.campers = {}
	
	def getName(self):
		return self.name	
		
	def getCampers(self):
		return self.campers
		
	def updateCampers(self, year, totalCampers):
		campers = self.getCampers()
		campers[year] = totalCampers
		#print self.getName(), campers
		

class NationalPark(Park):
	def __init__(self, name):
		Park.__init__(self, name)
		

class ProcessParkData:
	
	def init(self):
		print "starting process"
		print 
		
		backcountryDataDirPath = "../data/national_parks/raw/backcountry_campers"
		backcountryDestFilePath = "../data/national_parks/processed/backcountry_campers_combined.csv"
		
		tentDataDirPath = "../data/national_parks/raw/tent_campers"
		tentDestFilePath = "../data/national_parks/processed/tent_campers_combined.csv"
		
		rvDataDirPath = "../data/national_parks/raw/rv_campers"
		rvDestFilePath = "../data/national_parks/processed/rv_campers_combined.csv"
		
		recVisitorsDataDirPath = "../data/national_parks/raw/recreation_visitors"
		recVisitorsDestFilePath = "../data/national_parks/processed/recreation_visitors_combined.csv"
		
		self.nationalParkCache = []
		
		self.getFiles(backcountryDataDirPath)
		self.writeCombinedFile(backcountryDestFilePath)
		
		self.getFiles(tentDataDirPath)
		self.writeCombinedFile(tentDestFilePath)
		
		self.getFiles(rvDataDirPath)
		self.writeCombinedFile(rvDestFilePath)
		
		self.getFiles(recVisitorsDataDirPath)
		self.writeCombinedFile(recVisitorsDestFilePath)
	
	def getNationalParkCache(self):
		return self.nationalParkCache
		
	def getFromNationalParkCache(self, name):
		cache = self.getNationalParkCache()
		for park in cache:
			if park.getName() == name:
				return park
		
	def cacheContainsPark(self, name):
		natParkCache = self.getNationalParkCache()
		for natPark in natParkCache:
			if natPark.getName() == name:
				return True
		return False
		
	def getAllDates(self):
		longestLen = 0
		dates = []
		natParkCache = self.getNationalParkCache()
		for natPark in natParkCache:
			parkName = natPark.getName()
			campers = natPark.getCampers()
			if len(campers) > longestLen:
				longestLen = len(campers)
				longest = natPark
		
		campers = longest.getCampers()
		for key, val in sorted(campers.iteritems()):
			dates.append(key)
		return dates
	
	def getFiles(self, dataDirPath):
		allFiles = os.listdir(dataDirPath)
		for file in allFiles:
			if isfile(join(dataDirPath, file)):
				self.readFile(join(dataDirPath, file))
				#break # for testing
	
	def readFile(self, theFile):
		year = theFile.rstrip(".csv")[-4:]
		with open(theFile, 'rb') as csvFile:
			reader = csv.reader(csvFile, delimiter=',', quotechar='"')
			for row in reader:
				if len(row) > 3 and row[0] != "VisitorsLabel1":
					#print ', '.join(row)
					parkName = row[1]
					parkRanking = row[2]
					totalCampers = row[3]
					percentCampers = row[4]
							
					containsPark = self.cacheContainsPark(parkName)
					if containsPark == False:
						natParkCache = self.getNationalParkCache()
						natParkCache.append(NationalPark(parkName))
						
					thisNatPark = self.getFromNationalParkCache(parkName)
					thisNatPark.updateCampers(year, totalCampers)
		
					
	def writeCombinedFile(self, theFile):
		with open(theFile, 'wb') as csvFile:
			writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			
			allDates = self.getAllDates()
			header = ["name"] + allDates
			writer.writerow(header)
				
			natParkCache = self.getNationalParkCache()
			totalCampers = {}
			for natPark in natParkCache:
				parkName = natPark.getName()
				campers = natPark.getCampers()
				
				for date in allDates:
					if date not in campers:
						campers[date] = 0
				
				if len(campers) == len(allDates):
					dateVals = []
					for key, val in sorted(campers.iteritems()):
						dateVals.append(val)
						
						if len(totalCampers) < len(dateVals):
							totalCampers[key] = 0
							totalCampers[key] = int(str(totalCampers[key]).replace(",", "")) + int(str(val).replace(",", "")) 
						else:
							print totalCampers[key]
							totalCampers[key] = int(str(totalCampers[key]).replace(",", "")) + int(str(val).replace(",", ""))

					
					writer.writerow([parkName] + dateVals)
					
			summedDateVals = []			
			for key, val in sorted(totalCampers.iteritems()):
				summedDateVals.append(val)		
			writer.writerow(["Combined"] + summedDateVals)
				


if __name__ == '__main__':
	
	ProcessParkData = ProcessParkData()
	ProcessParkData.init()

	print "DONE"

