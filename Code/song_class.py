import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Song(object):
    """This class defines a 'song' object"""
    songCount = 0

    def __init__(self, ID, name, duration=None, smartphonePlayCount=None, laptopPlayCount=None):
        self.name = name
        self.ID = ID
        if (duration is None):
            self.duration = 0
        else:
            self.duration = duration
        if (smartphonePlayCount is None):
            self.smartphonePlayCount = 0
        else:
            self.smartphonePlayCount = smartphonePlayCount
        if (laptopPlayCount is None):
            self.laptopPlayCount = 0
        else:
            self.laptopPlayCount = laptopPlayCount

    def __str__(self):
        return self.name

    def setName(self, name):
        self.name = name
    
    def setDuration(self, duration):
        self.duration = duration

    def addSmartphonePlayCount(self, smartphonePlayCount):
        self.smartphonePlayCount += int(smartphonePlayCount)
    
    def addLaptopPlayCount(self, laptopPlayCount):
        self.laptopPlayCount += int(laptopPlayCount)

    def getName(self):
        return self.name

    def getDuration(self):
        return self.duration

    def getSmartphonePlayCount(self):
        return self.smartphonePlayCount

    def getLaptopPlayCount(self):
        return self.laptopPlayCount

    def updateRepetitions(self, device, repetitions):
        if (device == 'Smartphone'):
            logging.info('         Adding +' + str(repetitions) + ' to this song (listening source: Smartphone)')
            self.addSmartphonePlayCount(repetitions)
        elif (device == 'Laptop'):
            logging.info('         Adding +' + str(repetitions) + ' to this song (listening source: Laptop)')
            self.addLaptopPlayCount(repetitions)