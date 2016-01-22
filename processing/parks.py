import csv, json, sys, os
from os.path import isfile, join

class Park(object):
	def __init__(self, name):
		self.name = name
		self.backcountryCampers = {}
	
	def getName(self):
		return self.name	
		
	def getBackcountryCampers(self):
		return self.backcountryCampers
		
	def updateBackcountryCampers(self, year, totalBackcountryCampers):
		backcountryCampers = self.getBackcountryCampers()
		backcountryCampers[year] = totalBackcountryCampers
		#print self.getName(), backcountryCampers
		

class NationalPark(Park):
	def __init__(self, name):
		Park.__init__(self, name)
		

class ProcessParkData:
	
	def init(self):
		print "starting process"
		print 
		
		dataDirPath = "../data/national_parks/"
		destFilePath = join(dataDirPath, "processed/backcountry_campers_combined.csv")
		self.nationalParkCache = []
		
		self.getFiles(dataDirPath)
		self.writeCombinedFile(destFilePath)
	
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
			backcountryCampers = natPark.getBackcountryCampers()
			if len(backcountryCampers) > longestLen:
				longestLen = len(backcountryCampers)
				longest = natPark
		
		backcountryCampers = longest.getBackcountryCampers()
		for key, val in sorted(backcountryCampers.iteritems()):
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
					totalBackcountryCampers = row[3]
					percentBackcountryCampers = row[4]
							
					containsPark = self.cacheContainsPark(parkName)
					if containsPark == False:
						natParkCache = self.getNationalParkCache()
						natParkCache.append(NationalPark(parkName))
						
					thisNatPark = self.getFromNationalParkCache(parkName)
					thisNatPark.updateBackcountryCampers(year, totalBackcountryCampers)
		
					
	def writeCombinedFile(self, theFile):
		with open(theFile, 'wb') as csvFile:
			writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			
			allDates = self.getAllDates()
			header = ["name"] + allDates
			writer.writerow(header)
				
			natParkCache = self.getNationalParkCache()
			for natPark in natParkCache:
				parkName = natPark.getName()
				backcountryCampers = natPark.getBackcountryCampers()
				
				for date in allDates:
					if date not in backcountryCampers:
						backcountryCampers[date] = -1
				
				if len(backcountryCampers) == len(allDates):
					dateVals = []
					for key, val in sorted(backcountryCampers.iteritems()):
						dateVals.append(val)
					writer.writerow([parkName] + dateVals)
					


if __name__ == '__main__':
	
	ProcessParkData = ProcessParkData()
	ProcessParkData.init()

	print "DONE"

