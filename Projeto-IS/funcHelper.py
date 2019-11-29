class FuncHelper:
	def __init__(self):
		self.listDict = []

	def setListDict(self, newlistDict):
		self.listDict = newlistDict

	def getListDict(self):
		return self.listDict

	def checkMemorySize(self, machine):
		if(machine.find("Memory size:") == -1):
			machine = machine.replace("Memory size", "Memory size:")
		return machine

	def stringToDict(self, string):
		dic = dict()
		stringList = string.split("\r\n")
		for name in stringList:
			posSep = name.find(":")
			key = name[:posSep]
			value = name[posSep+1:].strip()
			dic[key] = value

		return dic

	def stringToDictList(self, stringMachine):
		listDict = []
		listMachine = stringMachine.split("Name:")
		listMachine.pop(0)
		for machine in listMachine:
			addNameMachine = "Name:" + machine
			newStringMachine = self.checkMemorySize(addNameMachine)
			dic = self.stringToDict(newStringMachine)
			listDict.append(dic)
		self.setListDict(listDict)
