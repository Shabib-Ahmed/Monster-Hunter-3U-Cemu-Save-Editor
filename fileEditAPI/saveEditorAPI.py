from data.globalData import *
from data.itemCodes import *
from data.equipmentCodes import *

currentFilePath = None

def openSaveFile(fileName):
    global saveFileData, currentFilePath
    currentFilePath = fileName
    with open(fileName, "rb") as f:
        data = f.read()
    saveFileData = bytearray(data)

def saveSaveFile(fileName):
    with open(fileName, "wb") as f:
        f.write(saveFileData)

def changePlayerName(changedName):
    global saveFileData
    characters = list(changedName)
    offset = nameOffset
    for i in characters:
        saveFileData[offset] = int.from_bytes(i.encode('utf-8'), byteorder='big')
        offset = offset + 1
    
    while (offset < nameOffset + 10):
        saveFileData[offset] = 0
        offset = offset + 1

def getPlayerName():
    name = saveFileData[nameOffset:nameOffset + 10]
    return name.decode('utf-8', errors='ignore').rstrip('\x00')


def getEquipmentList(pageNumber):
    tempList = []
    offset = equipmentOffset + (16 * pageNumber * 100) 
    for i in range(pageNumber * 100, (pageNumber * 100) + 100):
        tempList.append(getEquipmentFromHex(saveFileData[offset], saveFileData[offset+2], saveFileData[offset+3]))
        offset = offset + 16
    return tempList

def changeEquipment(equipmentLocation, equipmentName):
    global saveFileData
    offset = equipmentOffset + (16 * equipmentLocation)
    hexValue = getEquipmentFromName(equipmentName)
    saveFileData[offset] = hexValue[0]
    saveFileData[offset+2] = hexValue[1]
    saveFileData[offset+3] = hexValue[2]

def getItemList(pageNumber):
    tempList = []
    offset = itemBoxOffset + (4 * pageNumber * 100)
    for i in range(pageNumber * 100, (pageNumber * 100) + 100):
        tempList.append((getItemFromHex(saveFileData[offset], saveFileData[offset+1]), saveFileData[offset+3]))
        offset = offset + 4
    return tempList

def changeItem(itemLocation, itemName, itemQuantity):
    global saveFileData
    offset = itemBoxOffset + (4 * itemLocation)
    hexValue = getItemFromString(itemName)
    saveFileData[offset] = hexValue[0]
    saveFileData[offset + 1] = hexValue[1]
    saveFileData[offset + 3] = itemQuantity
    
def getZennyAmount():
    return int.from_bytes(saveFileData[zennyOffset:zennyOffset + 3], byteorder='big')

def changeZennyAmount(value):
    global saveFileData
    valueBytes = value.to_bytes(3, byteorder='big')
    saveFileData[zennyOffset:zennyOffset + 3] = valueBytes