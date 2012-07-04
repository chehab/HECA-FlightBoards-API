# -*- coding: UTF-8 -*-

def writeToFile(filename, writedata):
    f = open( filename, 'w')
    f.write("")
    f.close()
    f = open( filename, 'w')
    f.write( writedata )
    f.close()

def appendToFile(filename, writedata):
    f = open( filename, 'a')
    f.write( writedata )
    f.close()

def getAirportDetails(search):
    Airports = {}
    #{"IATA":"","ICAO":"","City":"","Country":""}
    Airports["Asmara"] = {"IATA":"ASM","ICAO":"HHAS","City":"Asmara","Country":"Eritrea"}
    Airports["Riyadh"] = {"IATA":"RUH","ICAO":"OERK","City":"Riyadh","Country":"Saudi Arabia"}
    Airports["Bangkok"] = {"IATA":"BKK","ICAO":"VTBS","City":"Bang Phli, Samut Prakan","Country":"Thailand"}
    Airports["johannesburg"] = {"IATA":"JNB","ICAO":"FAJS","City":"Kempton Park, Ekurhuleni, Gauteng","Country":"South Africa"}
    Airports["Beijing"] = {"IATA":"PEK","ICAO":"ZBAA","City":"Chaoyang District, Beijing","Country":"China"}
    Airports["Kano"] = {"IATA":"KAN","ICAO":"DNKN","City":"Kano","Country":"Nigeria"}
    Airports["Jeddah"] = {"IATA":"JED","ICAO":"OEJN","City":"Jeddah","Country":"Saudi Arabia"}
    Airports["Bahrain"] = {"IATA":"BAH","ICAO":"OBBI","City":"Al Muharraq","Country":"Bahrain"}
    Airports["Abu Dhabi"] = {"IATA":"AUH","ICAO":"OMAA","City":"Abu Dhabi","Country":"United Arab Emirates"}
    Airports["Aden"] = {"IATA":"ADE","ICAO":"OYAA","City":"Aden","Country":"Yemen"}
    Airports["Frankfurt"] = {"IATA":"FRA","ICAO":"EDDF","City":"Frankfurt","Country":"German"}
    Airports["Casablanca"] = {"IATA":"CAS","ICAO":"GMMC","City":"Casablanca","Country":"Morocco"}
    Airports["Kuwait"] = {"IATA":"KWI","ICAO":"OKBK","City":"Al Farwaniyah","Country":"Kuwait"}
    #Airports[""] = {"IATA":"","ICAO":"","City":"","Country":""}
    
    if search in Airports.keys():
        return Airports[search]
    else:
        appendToFile( "missing_airports", search)
        return {"IATA":"","ICAO":"","City":"","Country":""}