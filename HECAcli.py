# -*- coding: UTF-8 -*-
#!/usr/bin/pyth

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
from HECA import *

def HECACLIVersion():
    return 0.1

class HECA_CLI:
    

    operation = None
    format    = None
    flight    = None
    
    def cli_exec():
        
        if (len(sys.argv) > 1):
            
            if( sys.argv[1] == '-v' or sys.argv[1] == '--Version' ):
                print "\nHECA/CAI FlightBoard (beta):"
                print "\tParser Version "+ str(HECAVersion() )
                print "\tCLI Version "+ str(HECACLIVersion()); print
                
            else:
                
                arguments = sys.argv[1].lower()
                
                if arguments[0:2] == "--":
                    printExportOprtions(arguments)
                
                elif arguments[0] == "-" and len(arguments) < 5:
                    printExportOprtionsAbbreviated(arguments)
                
                print
                print "Runing In Debug Mode.."
                print "arglen: " + str(len(arguments)) +" arg( "+str(1)+" / "+str(len(sys.argv))+" )"
                print "operation: " +str(operation)
                print "format: " + str(format)
                print "flight: " + str(flight)
                print
                
        else:
            self.help()
        
    
    def printExportOprtions(self, argu):
        print " $> printExportOprtions"
        # Get Operations.
        if argu[2:7] == "print":
            operation = "PRINT"
        elif argu[2:8] == "export":
            operation = "EXPORT"
        # Selected Format.
        if argu[8:11] == "xml" or argu[9:12] == "xml":
            format = "XML"
        elif argu[8:12] == "json" or argu[9:13] == "json":
            format = "JSON"
        # Selected Flight.
        if len(argu) > 10:
            if argu[14:21] == "arrival" or argu[13:20] == "arrival":
                flight = "ARRIVAL"
            elif argu[14:23] == "departure" or argu[13:22] == "departure":
                flight = "DEPARTURE"
        
    
    def printExportOprtionsAbbreviated(self, argu):
        # Get Operations.
        if argu[1] == "e":
            operation = "EXPORT"
        elif argu[1] == "p":
            operation = "PRINT"
        # Selected Format.
        if argu[2] == "j":
            format = "JSON"
        elif argu[2] == "x":
            format = "XML"
        # Selected Flight.
        if len(argu) > 3:
            if argu[3] == "a":
                flight = "ARRIVAL"
            elif argu[3] == "d":
                flight = "DEPARTURE"
            
        
    
    def help(self):
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
    

        