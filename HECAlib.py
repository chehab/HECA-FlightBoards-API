# -*- coding: UTF-8 -*-
#!/usr/bin/python

##############################################################
##############################################################
##                                                          ##
##      HECA-FB v2.3.1         HECA/CAI Flight Baord        ##
##      HECA Parser for cairo-airport.com/flight_**         ##
##                                                          ##
##           by: Chehab Mustafa-Hilmy                       ##
##          url: Chehab.me                                  ##
##      contact: apis@chehab.me                             ##
##                                                          ##
##############################################################

###### Update logg #######################

    
    ### 2.1.1 #######################
            # minorfix: encoding/charset UTF-8
    
    ### 2.1 ##########################
            # Minor Bugfixes
            # CGI script rewriten
    
    ### 2.0 ##########################
            # API Rewriten
            # API Changed
            # Faster Parsing
            # Faster Exporting
            # Less memory footprint
    
    ### 1.3 ##########################
            # Minor Enhancement 
            # Less memory footprint
    
    ### 1.0 ##########################
            # Stable Version
    
##########################################

from HTMLParser import HTMLParser
from urllib import urlopen
import json, yaml, time, os

def enum(**enums):
    return type('Enum', (), enums)

def HECAVersion():
    return "2.3.1"

class HECAParser(HTMLParser):
    '''
     subclasing HTMLParser to customize HECA parsing results
     and provide more custom methods HECA-API specific  
    '''

    ## Def enums 
    HECAHeading = enum(Arrival=0, Departure=1, Both=2)
    HECAFormat  = enum(JSON=0, XML=1, Plain=2)
    DebugMode   = enum(Off=False, On=True, Verbose=2, file=3)

    #####################
    flight        = {}
    arrivalList   = []
    departureList = []
    flightTemplet = {"airline":"","flightno":"","date":"","sch":"","eta":"","actual":"",
                     "airport":"","via":"","terminal":"","hall":"","status":""}

    #####################
    flightmode   = None
    insertIndex  = 0
    currentIndex = 0
    titles = ['airline','flightno','date','sch','eta','actual',"airport",'via','terminal','hall','status']

    #####################
    timestamp   = None #unix timestamp
    openRow     = False
    insertCell  = False
    debug       = DebugMode.Off
    watch       = None


##########################################################################################
### Super over-ride ######################################################################


    def handle_starttag(self, tag, attrs):
        if not self.timestamp: # get unix timestamp on first parse
            self.timestamp = int(time.time())
        # Open New Raw in case "<tr align=center>"
        if len(attrs) and not self.openRow:
            if tag == "tr" and attrs[0] == ('align', 'center'):
                self.openRow = True
                self.flight = {"airline":"","flightno":"","date":"","sch":"","eta":"","actual":"",
                                 "airport":"","via":"","terminal":"","hall":"","status":""}
        # New Cell if Raw Open add <td> tag found
        # self.insertCell = True if tag == "td" and self.openRow else False
        if self.openRow:
            if tag == "td":
                self.insertCell = True
            elif tag == "div" and self.titles[ self.currentIndex ] in ["date","sch","eta"]:
                self.insertCell = True
            else:
                self.insertCell = False
    #end:handle_starttag


    def handle_endtag(self, tag):
        if tag == "tr" and self.openRow:
            self.openRow = False
            self.currentIndex = 0
            self.__debug_flight__()
            if self.HECAisAPExists(self.flight["airport"]):
                self.flight.update( self.HECAGetAPCodes( self.flight["airport"] ) )
            if self.flightmode == self.HECAHeading.Arrival:
                self.arrivalList.append(self.flight)
            if self.flightmode == self.HECAHeading.Departure:
                self.departureList.append(self.flight)
        if tag == "td" and self.insertCell:
            self.insertCell = False
            if self.currentIndex == 10:
                self.currentIndex = 0
            else:
                self.currentIndex += 1
    #end:handle_endtag


    def handle_data(self, data):   
        fieldData = ''
        for i in range(len(data)):
            if data[i] != '\n' and data[i] != '\r' and data[i] != '\t' and data[i] != '  ':
                fieldData += data[i]
        if self.insertCell:
            self.flight[ self.titles[ self.currentIndex ] ] = fieldData.strip()
            
        if self.watch and self.openRow:# and self.insertCell:
            if self.watch == "all":
                print "insertCell = " + str(self.insertCell)
                print "@ ?-{}::{}::".format(self.titles[ self.currentIndex ],data)
            else:
                for wky in self.watch.keys():
                    if self.watch[wky] == True and self.watch[wky] == self.titles[ self.currentIndex ]:
                        print "@ {} : {} :: {}".format(wky,self.flight[ self.titles[ self.currentIndex ] ],data)
    #end:handle_data


##########################################################################################
### Generate #############################################################################


    def HECARefreshFlightData(self):
        self.HECAGenerateFlightData()
    #end:HECARefreshFlightData


    def HECAUpdateFlightData(self):
        self.HECAGenerateFlightData()
    #end:HECAUpdateFlightData


    def HECAGenerateFlightData(self):
        if self.debug:
            print " %>Parsing Flight Data"
        self.HECAGenerateArrival()
        self.HECAGenerateDeparture()
    #end:HECAGenerateFlightData


    def HECAGenerateArrival(self, withCache=True):
        if self.HECAisCacheAvailable(self.HECAHeading.Arrival) and withCache:
            self.HECAloadCached(self.HECAHeading.Arrival)
            return True
        if self.debug:
            print " %>Parsing Arrival Data"
        f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
        self.flightmode = self.HECAHeading.Arrival
        self.feed( f.read() )
        f.close()
        self.flightmode = None
        self.arrivalList.reverse()
        self.HECAWriteCache()
    #end:HECAGenerateArrival


    def HECAGenerateDeparture(self, withCache=True):
        if self.HECAisCacheAvailable(self.HECAHeading.Departure) and withCache:
            self.HECAloadCached(self.HECAHeading.Departure)
            return True
        if self.debug:
            print " %>Parsing Departure Data"
        f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
        self.flightmode = self.HECAHeading.Departure
        self.feed( f.read() )
        f.close()
        self.flightmode = None
        self.departureList.reverse()
        self.HECAWriteCache()
    #end:HECAGenerateDeparture


##########################################################################################
### Return JSON ##########################################################################


    def HECAGetAsJSON(self, _heading = HECAHeading.Both):
        if self.debug:
            print " %>Generating JSON"            
        if _heading == self.HECAHeading.Departure:
            if not self.departureList:
                self.HECAGenerateDeparture()
            return json.dumps( { "departure":self.departureList } )
        if _heading == self.HECAHeading.Arrival:
            if not self.arrivalList:
                self.HECAGenerateArrival()
            return json.dumps( { "arrival":self.arrivalList } )
        if _heading == self.HECAHeading.Both:
            if not self.arrivalList and not self.departureList:
                self.HECAGenerateFlightData()
            return json.dumps( { "arrival":self.arrivalList, "departure":self.departureList } )
    #end:HECAGetAsJSON


    def HECAGetArrivalAsJSON(self):
        if self.debug:
            print " %>Generating Arrival JSON"
        if not self.arrivalList:
            self.HECAGenerateArrival()
        return json.dumps( {"Arrival":self.arrivalList} )
    #end:HECAGetArrivalAsJSON


    def HECAGetDepartureAsJSON(self):
        if self.debug:
            print " %>Generating Departure JSON"
        if not self.departureList:
            self.HECAGenerateDeparture()
        return json.dumps( {"departure":self.departureList} )
    #end:HECAGetArrivalAsJSON


##########################################################################################
### Return XML ###########################################################################


    def HECAGetAsXML(self, heading = HECAHeading.Both):
        if heading == self.HECAHeading.Departure:
            return self.HECAGetDepartureAsXML()
        
        if heading == self.HECAHeading.Arrival:
            return self.HECAGetArrivalAsXML()
        
        if heading == self.HECAHeading.Both:
            xmlexport = '<?xml version="1.0"?>\n'
            xmlexport += "\n\t<HECAFlights>\n"
            xmlexport += self.HECAGetArrivalAsXML(XMLTag=False)
            xmlexport += self.HECAGetDepartureAsXML(XMLTag=False)
            xmlexport += "\n\t</HECAFlights>\n"
            return xmlexport
        
        if self.debug:
            print " %>Generating XML"
    #end:HECAGetAsXML


    def HECAGetArrivalAsXML(self, XMLTag=True):
        if self.debug:
            print " %>Generating Arrival XML"
        
        if not self.arrivalList:
            self.HECAGenerateArrival()
        
        xmlexport = '<?xml  version="1.0"?>\n\n\t<HECAFlights>\n' if XMLTag else ""
        xmlexport += "\n\t\t<arrival>\n"
        
        for fl in self.arrivalList:
            xmlexport += "\n\t\t\t<flight>"
            for key in self.titles:
                xmlexport += "\n\t\t\t\t<{0}>{1}</{2}>".format(key, fl[key], key)
            xmlexport += "\n\t\t\t</flight>\n"
            
        xmlexport += "\n\t\t</arrival>\n"
        xmlexport += '\n\t</HECAFlights>\n' if XMLTag else ""
        
        return xmlexport
    #end:HECAGetArrivalAsXML


    def HECAGetDepartureAsXML(self, XMLTag=True):
        if self.debug:
            print " %>Generating Departure XML"
        if not self.departureList:
            self.HECAGenerateDeparture()
        xmlexport = '<?xml  version="1.0"?>\n\n\t<HECAFlights>\n' if XMLTag else ""
        xmlexport += "\n\t\t<departure>\n"
        for fl in self.departureList:
            xmlexport += "\n\t\t\t<flight>"
            for key in self.titles:
                xmlexport += "\n\t\t\t\t<{0}>{1}</{2}>".format(key, fl[key], key)
            xmlexport += "\n\t\t\t</flight>\n"
        xmlexport += "\n\t\t</departure>\n"
        xmlexport += '\n\t</HECAFlights>\n' if XMLTag else ""
        return xmlexport
    #end:HECAGetDepartureAsXML


##########################################################################################
### File Export ##########################################################################


    def HECAExportToFile(self, filename, _format, _heading=HECAHeading.Both):
        pass
    #end:HECAExportToFile


    def HECAExportArrivalToFile(self, filename, _format):
        pass
    #end:HECAExportArrivalToFile


    def HECAExportDepartureToFile(self, filename, _format):
        pass
    #end:HECAExportDepartureToFile


### Export to JSON #######################################################################


    def HECAExportToJSONFile(self, filename="HECA-flighdata.json", _heading=HECAHeading.Both):
        self.__writeToFile__(filename, json.dumps( { "arrival":self.arrivalList, "departure":self.departureList } ) )
        if self.debug:
            print " %>Exporting JSON file"
    #end:HECAExportToJSONFile


    def HECAExportArrivalToJSONFile(self, filename="HECA-Arrival.json"):
        self.__writeToFile__(filename, json.dumps( { "arrival":self.arrivalList } ) )
        if self.debug:
            print " %>Exporting Arrival JSON file"
    #end:HECAExportArrivalToJSONFile


    def HECAExportDepartureToJSONFile(self, filename="HECA-Departure.json"):
        self.__writeToFile__(filename, json.dumps( { "departure":self.departureList } ) )
        if self.debug:
            print " %>Exporting Departure JSON file"
    #end:HECAExportDepartureToJSONFile


### Export to XML ########################################################################


    def HECAExportToXMLFile(self, filename="HECA-flighdata.xml", _heading=HECAHeading.Both):
        self.__writeToFile__(filename, self.HECAGetAsXML() )
        if self.debug:
            print " %>Generating XML File"    
    #end:HECAExportToXMLFile


    def HECAExportArrivalToXMLFile(self, filename="HECA-Arrival.xml"):
        self.__writeToFile__(filename, self.HECAGetArrivalAsXML() )
        if self.debug:
            print " %>Generating Arrival XML file"
    #end:HECAExportArrivalToXMLFile


    def HECAExportDepartureToXMLFile(self, filename="HECA-Departure.xml"):
        self.__writeToFile__(filename, self.HECAGetDepartureAsXML() )
        if self.debug:
            print " %>Generating Departure XML"
    #end:HECAExportDepartureToXMLFile


### Cacheing ########################################################################

    def HECAisCacheAvailable(self, flightheadig = HECAHeading.Both):
        arrivalCacheStatus = False
        departureCacheStatus = False
        if not self.timestamp:
            self.timestamp = int(time.time())
        if flightheadig == self.HECAHeading.Arrival or flightheadig == self.HECAHeading.Both:
            if int(os.path.getmtime("HECA-Cache-Arrivals.yaml")) + 60*3 > self.timestamp:
                if flightheadig == self.HECAHeading.Both:
                    arrivalCacheStatus = True
                else:
                    return True
        if flightheadig == self.HECAHeading.Departure or flightheadig == self.HECAHeading.Both:
            if int(os.path.getmtime("HECA-Cache-Departures.yaml")) + 60*3 > self.timestamp:
                if flightheadig == self.HECAHeading.Both:
                    departureCacheStatus = True
                else:
                    return True
        if flightheadig == self.HECAHeading.Both:
            return arrivalCacheStatus and departureCacheStatus
        else:
            return False
    #end:HECAisCacheAvailable
           
    def HECAloadCached(self, flightheadig = HECAHeading.Both):
        if flightheadig == self.HECAHeading.Arrival or flightheadig == self.HECAHeading.Both:
            with open( "HECA-Cache-Arrivals.yaml" , 'r') as f:
                read_data = f.read()
            self.arrivalList = yaml.load(read_data)
        if flightheadig == self.HECAHeading.Departure or flightheadig == self.HECAHeading.Both:
            with open( "HECA-Cache-Departures.yaml" , 'r') as f:
                read_data = f.read()
            self.departureList = yaml.load(read_data)
    #end:HECAisCacheAvailable
    
    def HECAWriteCache(self):
        if self.arrivalList:
            f = open( "HECA-Cache-Arrivals.yaml", 'w')
            yaml.dump(self.arrivalList, f)
            f.close()
        if self.departureList:
            f = open( "HECA-Cache-Departures.yaml", 'w')
            yaml.dump(self.arrivalList, f)
            f.close()
    #end:HECAWriteCache

    def HECAUpdateCache(self, flightheadig = HECAHeading.Both):
        if flightheadig == self.HECAHeading.Arrival or flightheadig == self.HECAHeading.Both:
            self.HECAGenerateArrival(withCache=False)
        if flightheadig == self.HECAHeading.Departure or flightheadig == self.HECAHeading.Both:
            self.HECAGenerateDeparture(withCache=False)

### AP Codes ########################################################################


    def HECAGetAPCodes(self,searchPhrase):
        with open( "HECA-AirportsCodes.yaml" , 'r') as f:
            read_data = f.read()
        APCodes = yaml.load(read_data)
        return APCodes[searchPhrase]
    #ed:HECAGetAPCodes

    def HECAisAPExists(self,searchPhrase):
        with open( "HECA-AirportsCodes.yaml" , 'r') as f:
            read_data = f.read()
        APCodes = yaml.load(read_data)
        if searchPhrase in APCodes:
            return True
        else:
            with open("HECA-AirportsCodes.yaml", "a") as f:
                #f.write("\n{}:\n  IATA: N/A\n  ICAO: N/A\n  City: N/A\n  Country: N/A".format(searchPhrase))
                f.write("\n"+searchPhrase+":\n  IATA: N/A\n  ICAO: N/A\n  City: N/A\n  Country: N/A")
        return False
    #END:HECAisAPExists


##########################################################################################
### debug ################################################################################


    def __writeToFile__(self, filename, writedata):
        f = open( filename, 'w')
        f.write("")
        f.close()
        f = open( filename, 'w')
        f.write( writedata )
        f.close()
    #end:__writeToFile__


    def __debug_flightList__(self, force=False):
        if force or self.debug == self.DebugMode.Verbose:
            for row in self.arrivalList:
                print "\n####################################\n"
                for cell in self.titles:
                    print "   "+ cell + ": " + row[cell] + "\n"
    #end:__debug_flightList__


    def __debug_flight__(self, force=False):
        if force or self.debug == self.DebugMode.Verbose:
            print " %>openRow ###########################\n"
            for col in self.titles:
                print "   "+ col + ": " + self.flight[col] + "\n"
            print "######################################\n"
    #end:__debug_flight__


##########################################################################################
################################################################# End of Implemntation ###           