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
##    -exa -f=arrivals /dir/subdir                          ##
##    --export-xml-arrival --file=arrivals /dir/subdir      ##
##                                                          ##
##    -pj  | --print-json                                   ##
##    -pjd | --print-json-departure                         ##
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

operation = None
format    = None
flight    = None
fileName  = None
exportDir = None

  

def main():
    
     
    
    if (len(sys.argv) > 1):
        
        if( sys.argv[1] == '-v' or sys.argv[1] == '--Version' ):
            print "\nHECA/CAI FlightBoard (beta):"
            print "\tParser Version "+ str(HECAVersion() )
            print "\tCLI Version "+ str(HECACLIVersion()); print
            
        else:
            
            operation = None
            format    = None
            flight    = None
            fileName  = None
            exportDir = None
            
            arguments = sys.argv[1].lower()
            
            if arguments[0:1] == "--":
                # Get Operations.
                if arguments[2:7] == "print":
                    operation = "p"
                elif arguments[2:8] == "export":
                    operation = "e"
                # Selected Format.
                if arguments[8:11] == "xml" or arguments[9:12] == "xml":
                    format = "x"
                elif arguments[8:12] == "json" or arguments[9:13] == "json":
                    format = "j"
                # Selected Flight.
                if len(arguments) > 10:
                    if arguments[14:21] == "arrival" or arguments[13:20] == "arrival":
                        flight = "a"
                    elif arguments[14:23] == "departure" or arguments[13:22] == "departure":
                        flight = "d"
            elif len(arguments) < 5:
                # Get Operations.
                if arguments[1] == "e":
                    operation = "e"
                elif arguments[1] == "p":
                    operation = "p"
                # Selected Format.
                if arguments[2] == "j":
                    format = "j"
                elif arguments[2] == "x":
                    format = "x"
                # Selected Flight.
                if len(arguments) > 3:
                    if arguments[3] == "a":
                        flight = "a"
                    elif arguments[3] == "d":
                        flight = "d"
            # else:
            #     help()
            #     exit()

                
            print "Runing In Debug Mode.."
            print "operation: "+str(operation)
            print "format: "+ str(format)
            print "flight: "+ str(flight)
            print "arglen: "+ str(len(arguments))
            
    else:
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

    
    
    
    
if __name__ == '__main__':
    
    main()