# -*- coding: UTF-8 -*-
#!/usr/bin/python

##############################################################
##############################################################
##                                                          ##
##      HECA-Fb v2.3           HECA/CAI Flight Baord        ##
##      HECA Parser for cairo-airport.com/flight_**         ##
##      HECA CLI v0.1                                       ##
##      HECA CLI tool for runing/testing HECA/CAI-Fb        ##
##                                                          ##
##           by: Chehab Mustafa-Hilmy                       ##
##          url: Chehab.me                                  ##
##      contact: apis@chehab.me                             ##
##                                                          ##
##############################################################

##############################################################
##                                                          ##
##  Usage:                                                  ##
##                                                          ##
##    -exa -f=arrivals -d=/dir/subdir                       ##
##    --export-xml-arrival --file=ar..ls --dir=/dir/subdir  ##
##    -fd=/dir/subdir/arrivals.json                         ##
##                                                          ##
##    -pj  | --print-json                                   ##
##    -pjd | --print-json-departure                         ##
##                                                          ##
##    --follow    -fw                                       ##
##    --verbose   -Vb                                       ##
##                                                          ##
##                                                          ##
##   --watch <sampling> <field=vaule>                       ##
##   --watch-sch <sampling> <field=vaule>                   ##
##   --watch-record                                         ##
##   ex: -exa --watch eta=05:35                             ##
##   ex: -exa --watch-sch                                   ##
##   [:sch: or any supplied fields ]                        ##
##                                                          ##
##    Rest: TBA                                             ##
##                                                          ##
##############################################################

import sys

# sys.path.append('/Users/chehab/Development/HECA/')

from HECADetails import *
from HECAlib import *

def HECACLIVersion():
    return 0.1

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

class HECA_CLI:
    
    
    operations = []
    operation  = None
    format     = None
    flight     = None
    fileName   = None
    exportDir  = None
    
        
    def cli_exec(self, args):
        
        if (len(args) > 1):
            
            if( args[1].lower() == '-v' or args[1].lower() == '--version' ):
                print "\nHECA/CAI FlightBoard (beta):"
                print "\tParser Version "+ str(HECAVersion() )
                print "\tCLI Version "+ str(HECACLIVersion()); print
                
            else:
                for i in range(1,len(args)):
                    if args[i].lower()[0:2] == "--":
                        self.printExportOptions(args[i].lower())
                    
                    elif args[i].lower()[0] == "-" and len(args[i].lower()) < 5:
                        self.printExportOptionsAbbreviated(args[i].lower())
                        
                        if self.watchOption(args[i]):
                            self.watchKeyValue(args[i])
                    
                    if self.operation:
                        print
                        print "Runing In Debug Mode.."
                        print "arglen: " + str(len(arg.lower())) +" arg( "+ str(1)+" / "+ str(len(args))+" )"
                        print "operation: " + str(self.operation)
                        print "format: " + str(self.format)
                        print "flight: " + str(self.flight)
                        print
                
        else:
            self.help()
        
    
    def printExportOptions(self, argu):
        print "HECA_CLI::printExportOptions: "+str(argu)
        # Get Operations.
        if argu[2:7] == "print":
            self.operations.append("PRINT")
        elif argu[2:8] == "export":
            self.operation.append("EXPORT")
        # Selected Format.
        if argu[8:11] == "xml" or argu[9:12] == "xml":
            self.format = "XML"
        elif argu[8:12] == "json" or argu[9:13] == "json":
            self.format = "JSON"
        # Selected Flight.
        if len(argu) > 10:
            if argu[14:21] == "arrival" or argu[13:20] == "arrival":
                self.flight = "ARRIVAL"
            elif argu[14:23] == "departure" or argu[13:22] == "departure":
                self.flight = "DEPARTURE"
        
    
    def watchOption(self, argu):
        print "HECA_CLI::watchOptions: "+str(argu)
        # Get Operations.
        if argu[2:7] == "watch":
            self.operation.append({"WATCH":None})
            
            for field in HECAParser.titles+["record","all","value"]:
                if argu[8:9+len(field)] == field:
                    self.operation[-1]["WATCH"]= field
                    
            return True
            
        else:
            return False
        
       
    def watchKeyValue(self, argu):
        print "HECA_CLI::watchOptions: "+str(argu)
        # Get Operations.
        if argu[2:7] == "watch":
            self.operation.append({"WATCH":None})
            
            for field in HECAParser.titles+["record","all","value"]:
                if argu[8:9+len(field)] == field:
                    self.operation[-1]["WATCH"]= field
                    
            return True
            
        else:
            return False
    
    def printExportOptionsAbbreviated(self, argu):
        print "HECA_CLI::printExportOptionsAbbreviated: "+str(argu)
        # Get Operations.
        if argu[1] == "e":
            self.operation = "EXPORT"
        elif argu[1] == "p":
            self.operation = "PRINT"
        # Selected Format.
        if argu[2] == "j":
            self.format = "JSON"
        elif argu[2] == "x":
            self.format = "XML"
        # Selected Flight.
        if len(argu) > 3:
            if argu[3] == "a":
                self.flight = "ARRIVAL"
            elif argu[3] == "d":
                self.flight = "DEPARTURE"
            
        
    @staticmethod
    def help():
        print #
        print "\nHECA/CAI FlightBoard (beta):"
        print "\tLib Version "+ str(HECAVersion() )
        print "\tCLI Version "+ str(HECACLIVersion())
        print #
        print "usage: heca <command><args> ... \n"
        print "commands: \n"
        print "       -v | --Version\tGet Current Versions.\n"
        print "       Export to File:\n"
        print "         -e<format>[<flight>] [-f<=name>] <dir>\n" 
        print "         --Export-<format>[-<flight>] [ --File<=name> ] <dir>\n"
        print "       Print to CLI:\n"
        print "         -p<format>[-<flight>]\n" 
        print "         --Export-<format>[-<flight>] \n"
        print "       <format>"
        print "          json: <j|json> [-ej] [--Export-JSON]\n"
        print "           xml: <x|xml> [-ex] [--Export-XML]\n"
        print "       <flight>"
        print "          departure: <d|departure> [-exd] [--Print-XML-Departure]\n"
        print "            arrival: <a|arrival> [-pja] [--Export-JSON-Arrival]\n"
    
    # help = Callable(help)

        