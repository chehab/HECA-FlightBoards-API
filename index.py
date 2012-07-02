#!/usr/bin/python

# Import modules for CGI handling 
import sys, cgi

#enable deugging
import cgitb; cgitb.enable()

# Import modules for HECA/CAI flightdata parser
from HECA import HECAParser


# Create instance of GET request
get = cgi.FieldStorage()


### No Request render a html page.
if len(GET.keys()) == 0:
    with open( "hello.html" , 'r') as f:
        read_data = f.read()
    f.closed
    print "Content-type: text/html\r\n\r\n"
    print read_data
### Process Request 
else:
    returnType = None 
    flightData = None
    try:
        for ky in GET.keys():
        ### Get return Types ################################################
            if ky == 'json' and ( GET[ky].value == "1" or GET[ky].value == "true" ):
                returnType = "json"; continue
            if ky == "xml" and ( GET[ky].value == "1" or GET[ky].value == "true" ):
                returnType = "xml"; continue
            if ky == "type" and GET[ky].value == "json":
                returnType = "json"; continue
            if ky == "type" and GET[ky].value == "xml":
                returnType = "xml"; continue
        ### Get flight Types ################################################
            ### [ arrival | departure | all ] = [ true | 1 ] ###
            if ky == 'arrival' and ( GET[ky].value == "1" or GET[ky].value == "true" ):
                flightData = "arrival"; continue
            if ky == 'departure' and ( GET[ky].value == "1" or GET[ky].value == "true" ):
                flightData = "departure"; continue
            if ky == "both" and ( GET[ky].value == "1" or GET[ky].value == "true" ):
                flightData = "both"; continue
            #### flight= [ arrival | departure | all ] ###
            if ky == "flight":
                if GET[ky].value == "both":
                    flightData = "both"; continue
                if GET[ky].value == "arrival":
                    flightData = "arrival"; continue
                if GET[ky].value == "departure":
                    flightData = "departure"; continue
        ################################################### GET request ###
    except Exception as inst:
        print "Content-type: text/html\r\n\r\n"
        print "<h1>An Error was encountered <em>in the input pramiters</em></h1>"
        print type(inst)
        print inst.args
        print inst
    except:
        print "Content-type: text/html\r\n\r\n"
        print "<h1>An Error was encountered <em>in the input pramiters</em></h1>"
    
    #######################################################################################
    ### Returing Request ##################################################################
    try:
        CAI = HECAParser()
        ### Returing JSON #################################################################
        if returnType == "json":
            print "Content-type: application/json"; print
            if flightData == "both":
                print CAI.HECAGetAsJSON()
            elif flightData == "arrival":
                print CAI.HECAGetArrivalAsJSON()
            elif flightData == "departure":
                print CAI.HECAGetDepartureAsJSON()
        ### Returing XML ##################################################################
        if returnType == "xml":
            print "Content-type: application/xml"; print
            if flightData == "both":
                print CAI.HECAGetAsXML()
            elif flightData == "arrival":
                print CAI.HECAGetArrivalAsXML()
            elif flightData == "departure":
                print CAI.HECAGetDepartureAsXML()
    except:
        print "Content-type: text/html\r\n\r\n"
        print "<h1>An Error was encountered <em>while parsing</em></h1>"