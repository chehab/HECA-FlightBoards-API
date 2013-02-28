#!/usr/bin/python
# -*- coding: UTF-8 -*-
# export PYTHONIOENCODING=utf-8

# Import modules 
import os, sys
import Queue
import threading
# Import modules for CGI deugging
import cgi, cgitb; cgitb.enable()

#Importing HECA/CAI flightdata parser
from HECAlib import HECAParser

#Importing HECA Themeing
from HECAtheme import HECATheme

# Create instance of GET request
GET = cgi.FieldStorage()

# http status code
statusCode = "400"

def HECAUpdateCache():
    CAI_debug = HECAParser()
    CAI_debug.HECAUpdateCache()
    # respondpage = HECATheme()
    # respondpage.alert("info","HECA Cache Updated",mode_msg)
    # print respondpage.echo()
#end:HECAUpdateCache

def mimetype(mt="html"):
    if mt == "json":
        print "Content-type: application/json"#; print
    if mt == "xml":
        print "Content-type: application/xml"
    if mt == "javascript":
        print "Content-type: text/javascript"
    if mt == "html":
        print "Content-type: text/html"#; print
    print "Content-Encoding: UTF8"; print


### No Request render a html page.
if len(GET.keys()) == 0:
   respondpage = HECATheme()
   print respondpage.echo()
### Process Request 
else:
    returnType    = None
    flightData    = None
    json_callback = None
    loadfromcache = False
    #try:
    for ky in GET.keys():
        
        value_lower = GET.getvalue(ky).lower()
        keyword = str(ky).lower()
        
    
    ### format=flight ################################################
    
        if keyword == 'json':
            returnType = "json"
            if value_lower == "arrival":
                flightData = "arrival"; continue
            elif value_lower == "departure":
                flightData = "departure"; continue
            elif value_lower == "both" or value_lower == "all":
                flightData = "both"; continue
        
        ################################################
        
        if keyword == 'xml':
            returnType = "xml"
            if value_lower == "arrival":
                flightData = "arrival"; continue
            elif value_lower == "departure":
                flightData = "departure"; continue
            elif value_lower == "both" or value_lower == "all":
                flightData = "both"; continue
        
    
    ### flight=format ################################################
    
        if keyword == 'arrival':
            flightData = "arrival"
            if value_lower == "json":
                returnType = "json"; continue
            elif value_lower == "xml":
                returnType = "xml"; continue
        
        ################################################
        
        if keyword == 'departure':
            flightData = "departure"
            if value_lower == "json":
                returnType = "json"; continue
            elif value_lower == "xml":
                returnType = "xml"; continue
        
    
    ### JSON: callback ################################################
    
        if keyword == 'callback':
            json_callback = value_lower; continue
    
    ### Test Mode: load from cache ####################################
    
        if keyword == 'cache':
            kyValue = GET.getvalue(ky)
            if kyValue == "1" or kyValue == "true" or kyValue == "force":
                loadfromcache = True; continue
    
    ### debugig: check=function|var ###################################
    
        if keyword == 'exec':
            
            kyValue = GET.getvalue(ky)
            mode_msg = "Maintenance Mode"
            respondpage = HECATheme()
            
            if kyValue == "HECAisCacheAvailable":
                CAI_debug = HECAParser()
                respond_msg = "Is Cache Available = "
                if CAI_debug.HECAisCacheAvailable():
                    respond_msg += "True"
                    respondpage.alert("success",respond_msg, mode_msg)
                else:
                    respond_msg += "False"
                    respondpage.alert("error",respond_msg, mode_msg)
                print respondpage.echo()
            
            if kyValue == "HECAisCacheAvailable|arrival":
                CAI_debug = HECAParser()
                respond_msg = "Is Cache Available for Arrivals = "
                if CAI_debug.HECAisCacheAvailable( CAI_debug.HECAHeading.Arrival ):
                    respond_msg += "True"
                    respondpage.alert("success",respond_msg,mode_msg)
                else:
                    respond_msg += "False"
                    respondpage.alert("error",respond_msg,mode_msg)
                print respondpage.echo()
            
            if kyValue == "HECAisCacheAvailable|departure":
                CAI_debug = HECAParser()
                respond_msg = "Is Cache Available for Departure = "
                if CAI_debug.HECAisCacheAvailable( CAI_debug.HECAHeading.Departure ):
                    respond_msg += "True"
                    respondpage.alert("success",respond_msg,mode_msg)
                else:
                    respond_msg += "False"
                    respondpage.alert("error",respond_msg,mode_msg)
                print respondpage.echo()
            
            if kyValue == "HECAUpdateCache":

                update_q = Queue.Queue()
                t = threading.Thread(target=HECAUpdateCache)
                t.daemon = True
                t.start()

                reload_url = ""
                for char in str( os.environ['SERVER_NAME'] + os.environ['REQUEST_URI'] ):
                    if char != "?":
                        reload_url += char
                    else:
                        reload_url += "?exec=CacheUpdating"
                        break

                respondpage = HECATheme()
                respondpage.pageRefresh(60,reload_url)
                respondpage.alert("info","HECA Updating Cache. <small>Page Will ReFresh in 60 secands.</small>",mode_msg)
                print respondpage.echo()
            
            if kyValue == "CacheUpdating":
                reload_url = ""
                for char in str( os.environ['SERVER_NAME'] + os.environ['REQUEST_URI'] ):
                    if char != "?":
                        reload_url += char
                    else:
                        reload_url += "?exec=CacheUpdating"
                        break

                respondpage = HECATheme()

                if CAI_debug.HECAisCacheAvailable():
                    respondpage.alert("info","HECA Cache Has Been Updated.",mode_msg)
                else:
                    respondpage.pageRefresh(60,reload_url)
                    respondpage.alert("info","HECA Updating Cache. <small>Page Will ReFresh in 60 secands.</small>",mode_msg)
                
                print respondpage.echo()
                exit()

            # if kyValue == "HECAGetUpdatedFlights|arrival|json":
            #     CAI_debug = HECAParser()
            #     if CAI_debug.HECAisCacheAvailable( CAI_debug.HECAHeading.Departure ):
            #         mimetype("json")
            #         CAI_debug.HECAGetUpdatedFlights( CAI_debug.HECAHeading.Arrival )
            #         print CAI_debug.HECAGetArrivalAsJSON()
            #     else:
            #         mimetype("json")
            #         print '{"Cach is Outdated":-1}'
            
        
        ################################################### GET request ###
    #except Exception as inst:
        #TODO
    #except:
        #TODO
    
    
    #######################################################################################
    ### Returing Request ##################################################################
    
    #try:
    CAI = HECAParser()
    
    ### Returing JSON #################################################################
    
    if returnType == "json":
    
        respond = ""
        if flightData == "both":
            respond = CAI.HECAGetAsJSON(loadfromcache)
        elif flightData == "arrival":
            respond = CAI.HECAGetArrivalAsJSON(loadfromcache)
        elif flightData == "departure":
            respond = CAI.HECAGetDepartureAsJSON(loadfromcache)
        
        if json_callback:
            mimetype("javascript")
            respond = json_callback + "(" + respond + ")"
        else:
            mimetype("json")
        
        print respond
    
    ### Returing XML ##################################################################
    
    if returnType == "xml":
        mimetype("xml")
        if flightData == "both":
            print CAI.HECAGetAsXML()
        elif flightData == "arrival":
            print CAI.HECAGetArrivalAsXML()
        elif flightData == "departure":
            print CAI.HECAGetDepartureAsXML()
    
   # except:
       #TODO
