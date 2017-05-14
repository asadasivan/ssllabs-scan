#!/usr/bin/env python
'''
@Author: Arunkumar Sadasivan
Reference: ssllabsscanner project (author Jonathan C Trull). 
'''
import argparse
import requests
import time
from UtilityPartner import readURLListFile,getUniqueURLList,dynamicPrinter

'''
@params:
publish : set to "off" if assessment results should not be published on the public results boards
startNew : if set to "on" then cached assessment results are ignored
fromCache : if on will deliver cached assessment reports
all : done - full information will be returned only if the assessment is complete (status is READY or ERROR).
ignoreMismatch : proceed with assessments even when server certificate doesn't match the assessment hostname
'''
# Defaults:
API = "https://api.ssllabs.com/api/v2/"
baseOutputFileName = "SSLTestResults"
baseOutputFileExt = "txt"
baseURLlistFileName = "hostURL"
baseURLlistFileExt = "info"
fileDir = "." # modify this paramter to specify the input file. Output file will be created under the same directory. 


# This is a helper method that takes the path to the relevant API call and the user-defined payload and requests the data/server test from Qualys SSL Labs. Returns JSON formatted data
def requestAPI(path, payload={}):
    url = API + path   
    try:
        response = requests.get(url, params=payload)
    except requests.exceptions.RequestException as e:
        print "Exception Occured", e
        pass
        #sys.exit(1)
    if response is None:
        results = "[Error] Failed to establish a connection: Nodename nor server name provided not known"
    else:
        results = response.json()
    return results

def resultsFromCache(host, publish = "off", startNew = "off", fromCache = "on", all = "done"):
    path = "analyze"
    payload = {'host': host, 'publish': publish, 'startNew': startNew, 'fromCache': fromCache, 'all': all}
    results = requestAPI(path, payload)
    return results

def runSSLLabsScan(host, publish = "off", startNew = "on", all = "done", ignoreMismatch = "on"):
    path = "analyze"
    payload = {'host': host, 'publish': publish, 'startNew': startNew, 'all': all, 'ignoreMismatch': ignoreMismatch}
    results = requestAPI(path, payload)
    payload.pop('startNew') 
    while results['status'] != 'READY' and results['status'] != 'ERROR':
        print("Scan in progress, please wait for the results.")
        time.sleep(30)
        results = requestAPI(path, payload)     
    return results
    
  
def getGradefromSSLlabs(results):
    try:
        grade = results['endpoints'][0]['grade']
        return grade
    except Exception, e:
        print "Exception Occured", e
        pass
        return "grade error"
   

def getProtocolList(results):
    SSLv2 = SSLv3 = TLS1_0 = TLS1_1 = TLS1_2 = "No"
    protocolList = [ ]
    #print results['endpoints'][0]['details']['protocols']
    try:
        for protocol in results['endpoints'][0]['details']['protocols']:
            if "SSL" in protocol['name'] and protocol['version']=="2.0":
                SSLv2 = "Yes"
                break
    except Exception, e:
        print "Exception Occured", e
        SSLv2 = "Error" 
        pass
    protocolList.append("SSLv2:" + SSLv2 )
          
    try:
        for protocol in results['endpoints'][0]['details']['protocols']:
            if "SSL" in protocol['name'] and protocol['version']=="3.0":
                SSLv3 = "Yes"
                break 
    except Exception, e:
        print "Exception Occured", e
        SSLv3 = "Error" 
        pass  
    protocolList.append("SSLv3:" + SSLv3) 
    
    try:
        for protocol in results['endpoints'][0]['details']['protocols']:
            if "TLS" in protocol['name'] and protocol['version']=="1.0":
                TLS1_0 = "Yes"
                break
    except Exception, e:
        print e
        TLS1_0 = "Error" 
        pass 
    protocolList.append("TLS1.0:" + TLS1_0)
        
    try:
        for protocol in results['endpoints'][0]['details']['protocols']:
            if "TLS" in protocol['name'] and protocol['version']=="1.1":
                TLS1_1 = "Yes"
                break
    except Exception, e:
        print "Exception Occured", e
        TLS1_1 = "Error" 
        pass
    protocolList.append("TLS1.1:" + TLS1_1) 
                    
    try:
        for protocol in results['endpoints'][0]['details']['protocols']:
            if "TLS" in protocol['name'] and protocol['version']=="1.2":
                TLS1_2 = "Yes"
                break
    except Exception, e:
        print "Exception Occured", e
        TLS1_2 = "Error" 
        pass
    protocolList.append("TLS1.2:" + TLS1_2) 
    
    return str(protocolList) # convert to string

   
def getCipherSuitesfromResults(results):
    cipherSuitesList = [ ]
    try:
        for suite in results['endpoints'][0]['details']['suites']['list']:
            cipherSuitesList.append(suite['name'] + ": " + str(suite['cipherStrength']))
        return str(cipherSuitesList) # convert to string 
    except Exception, e:
        print "Exception Occured", e
        pass
        return "ciphersuite list error"

     
def initiate_SSLlabsTest(URLList_File, protocol, cipherList):
    resultList = [ ]
    cipherSuites = protocolList = "null"
    fileList = readURLListFile(URLList_File)
    uniqueURLList = getUniqueURLList(fileList) 
    URLListsize = len(uniqueURLList) 
    currentURLNum = 1    
    for URL in uniqueURLList:
        output = "[Testing] %d of %d URL" % (currentURLNum,URLListsize) + "\n"
        dynamicPrinter(output)
        URL = URL.strip() # remove \n
        # initiate Qualys SSL labs test 
        results = runSSLLabsScan(URL)   
        if "Error" in results:
            # Unable to establish a connection
            resultList.append(URL + ";" + "Connection Error" + ";" + "Connection Error" + ";" + "Connection Error" + "\n")
        else:
            if(protocol):
                protocolList = getProtocolList(results)
            else:
                protocolList = "skip"  # Test not performed  
            if(cipherList):
                cipherSuites = getCipherSuitesfromResults(results)  
            else:
                cipherSuites = "skip" # Test not performed  
            grade = getGradefromSSLlabs(results)
            resultList.append(URL + ";" + grade + ";" + protocolList + ";" + cipherSuites + "\n")   
        currentURLNum += 1     
    return resultList  

def gethostURLFile():
    fileName = fileDir + "/" + baseURLlistFileName + "." + baseURLlistFileExt
    return fileName
    
def getSSLTestresultsFile():
    timeStr = time.strftime("%Y%m%d-%H%M%S")  
    fileName = fileDir + "/" + baseOutputFileName + "_" + timeStr + "." + baseOutputFileExt
    return fileName

def writeResultstoFile(resultList, outputFile):
    with open(outputFile, 'w+') as fileHandler:
        if resultList != None:
            for result in resultList:
                fileHandler.write(result)  
                
    
   
###############################################################################
# Main
###############################################################################
def main(args):
    cipherList = args.cipher
    protocol = args.protocol
    hostURLFile = args.urlfile
    resultsFile = args.outputfile
    if not hostURLFile:
        hostURLFile = gethostURLFile() 
    resultList =  initiate_SSLlabsTest(hostURLFile, protocol, cipherList) 
    if not resultsFile:
        resultsFile = getSSLTestresultsFile() 
    writeResultstoFile(resultList, resultsFile)
    
if __name__ == "__main__":
    def help_formatter(prog):
        r"Widen the text that is printed when the app is invoked with --help"
        args = dict(max_help_position=60, width=120)
        return argparse.HelpFormatter(prog, **args)

    parser = argparse.ArgumentParser(formatter_class=help_formatter)
    parser.add_argument("-f", "--urlfile", type=str, default=None,
                        required=False,
                        help="File that contains list of URLs or IP address.")
    parser.add_argument("-p", "--protocol", default=False, action="store_true", 
                        required=False,
                        help="Test for SSL or TLS Protocols supported")
    parser.add_argument("-c", "--cipher", default=False, action="store_true", 
                        required=False,
                        help="Test for Ciphers supported")
    parser.add_argument("-o", "--outputfile", type=str, default=None,
                        required=False,
                        help="File that contains the result of the test")
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        pass    
