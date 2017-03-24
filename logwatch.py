#!/usr/bin/env python2
"""Log files watcher for Python

Given a list of options through command line input, this program will 
search the keywords from the log file, and send an email to the 
users when any of these keywords are found.  

Usage: python logwatch.py [options] 

Options:
  (note: A space character separates each option)
  -f ..., --file_log=...  Full name of the log file for monitoring. 
                          Default is C:\\download\\AppServer-4.log.
  -k ..., --keyword=...   Search these keywords from the file. Multiple
                          keywords are separated with a comma. 
                          Default is exception.
  -u ..., --u_email=...   Send an alert email to these users' account.
                          Multiple kemails are separated with a comma.  
                          Default is ylee@mtc.ca.gov.
  -l ..., --line=...      Number of line to print for excerpt.
                          Default is 10              
  -m ..., --mail_host=... Use this to specify SMTP host name. 
                          Default is pp-ag1.abag.ca.gov.
  -p ..., --mail_port=... Use this to specify the port number for SMTP host. 
                          Default is 25.
  -o ..., --out_file=...  Temporary output file for email message. 
                          Default is logwatch.out.
  -h, --help              show this help
  
Examples:
  python logwatch.py --help (or -h)
  
  python logwatch.py -f c:\mytest.log -k exception,error,bad,trap -u ylee@abc.com,john@mtc.ca.gov,atti@abag.com
  
  python logwatch.py --file_log /usr/local/mytest.log --keyword exception,trap -u ylee@abc.org -p 52 --mail_host myhost.smtp.com -o mytest.out
  
  python logwatch.py -f c:\\download\\AppServer-3.log -k exception,sql,slave -l 8 -u ylee@abc.org -p 52 -m myhost.smtp.ca.gov -o mytest.out

  python logwatch.py -f /usr/local/bea/user_projects/domains/mtc/servers/AppServer-1/logs/AppServer-1.log -k exception,sql,slave -l 8 -u ylee@abc.com -p 25 -m pp-ag1.com -o mytest.out
"""

__author__ = "Yong Lee (ylee@mtc.ca.gov)"
__version__ = "2.5"  #this script is initially developed in

import sys, socket
import getopt
import re
import os
import smtplib





def usage():
    print __doc__

def main(argv):
    
    #set up default values
    file_log = "C:\\download\\AppServer-4.log"
    keywords = "exception"
    u_emails = "ylee@abc.com"
    e_line = 10 
    mail_host = "pp-ag1.abc.com"
    mail_port = 25
    out_file = "logwatch.out"
    dataFileName = 'logwatch.dat'
    
    #print "argv = %s\n" % argv
    
    try:
        opts, args = getopt.getopt(argv, "hk:u:l:m:p:f:o:d:", 
                                   ["help", "keyword=", "u_email=", "line=", "mail_host=", "mail_port=", "file_log=", "out_file=", "data_file"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-k", "--keyword"):
            keywords = arg
        elif opt in ("-u", "--u_email"):
            u_emails = arg
        elif opt in ("-l", "--line"):
            e_line = int (arg)
        elif opt in ("-m", "--mail_host"):
            mail_host = arg
        elif opt in ("-p", "--mail_port"):
            mail_port = int (arg)
        elif opt in ("-f", "--file_log"):
            file_log = arg
        elif opt in ("-o", "--out_file"):
            out_file = arg
        elif opt in ("-d", "--data_file"):
            dataFileName = arg
    
    #source = ";".join(args)
    #print "args = %s\n" % source
    print "keyword = %s\n u_email = %s\n u_line = %d\n mail_host = %s\n mail_port = %d\n file_log = %s\n out_file = %s\n" % (keywords, u_emails, e_line, mail_host, mail_port, file_log, out_file)       
    
    # f.seek(0, 2) # seek to the end of the file
    # f.tell()   # tell the position (size) of the file
    
    #read information recorded from last time file scan ...
    try:
        ftemp = open (dataFileName, 'r')
        line = ftemp.readline()
        (lineNumberStr, finputLastFileSizeStr) = line.split(',')
        lineNumber = int (lineNumberStr)
        finputLastFileSize = int (finputLastFileSizeStr)
        
    #except IOError:
    except:
        # data file does not exist. Use default value
        lineNumber = 0
        finputLastFileSize = 0  
        #print "Error encounter:", sys.exc_info()[0]
        #raise
    else:
        print "Closing file %s.\n" % dataFileName
        ftemp.close() 
    
    
    
    try:
        # open a file for writing
        foutput = open (out_file, "w")
        
        try:
            
            
            finput = open (file_log, "r")
            Continue = True
            (inFilePath, inFileName) = os.path.split(file_log)
            
            #get the current size of the file
            finput.seek(0, 2) # seek to the end of the file
            finputFileSize = finput.tell()   # tell the position (size) of the file 
            if finputLastFileSize <= finputFileSize :
                #continue to read the file from last point
                finput.seek(finputLastFileSize, 0)
            else:
                #read from the beginning
                finput.seek(0, 0)
                lineNumber = 0             
            
            
            try:
               while Continue:
                   line = finput.readline()
                   if len (line) == 0:
                       break
                   #process line
                   #print line 
                   lineNumber += 1
                   if isKeywordsInLine(line, keywords):
                       title = "\n\nA searched word is found in line %d from file %s. The following is an excerpt ...\n" % (lineNumber, inFileName)
                       foutput.write (title)
                       foutput.write (line)
                       #read the next X lines from the file
                       eLineCnter = 1
                       while (eLineCnter < e_line):
                           line = finput.readline()
                           if len (line) == 0:
                               Continue = False
                               break
                           
                           #process line
                           #print line 
                           lineNumber += 1
                           foutput.write (line)
                           eLineCnter += 1
               
               # get the file size 
               finput.seek(0, 2) # seek to the end of the file
               finputFileSize = finput.tell()   # tell the position (size) of the file   
             
            finally:
                finput.close()
                
        except IOError:
            print "Error in reading file %s.\n" % file_log
            os._exit(99)
            
    except IOError:
        print "Error in opening file %s.\n" % out_file   
        os._exit(99)
    else:
        print "Closing file %s.\n" % out_file
        foutput.close()
    
    #record input file information for next time use
    try:
        ftemp = open (dataFileName, 'w')
        ftemp.write ("%d,%d" % (lineNumber, finputFileSize))
    
    except IOError:
        print "Error in writing to file %s.\n" % dataFileName   
        os._exit(99)
    else:
        print "Closing file %s.\n" % dataFileName
        ftemp.close() 
        
    #send email 
    #open  
    try:
        ftemp = open (out_file, 'r')
        
        #read an entire file into a string
        email_body = ftemp.read()  
  
        # if the string is not empty, then send an email
        if len(email_body) > 0:
            # get the name of the local machine
            hostname = socket.gethostname()
            from_email = "root_" + hostname + "@mtc.ca.gov"
            emailList = u_emails.split (',')
            sendMessageWithSMTP(mail_host, from_email, emailList, email_body, file_log, mail_port)
            
      
    except IOError:
        print "Error in reading file %s.\n" % out_file   
        os._exit(99)
    else:
        print "Closing file %s after reading.\n" % out_file
        ftemp.close() 
    
    
    
    
       
def sendMessageWithSMTP(mail_server, from_addr, to_addr, email_body, log_file_name, mail_server_port = 25 ):
    """Send a email message using SMTP protocol.
    """
    
    subject_header = 'An exception found in %s' % log_file_name
    headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (from_addr, ", ".join(to_addr), subject_header)
    email_message = headers + email_body   
        
    try:
        s = smtplib.SMTP(mail_server, mail_server_port)
        s.sendmail(from_addr, to_addr, email_message)
        print 'An email is successfully sent to %s' % ", ".join(to_addr)
        s.quit()
    except:
        print "Error in sending email message...."
        print "Error encounter:", sys.exc_info()[0]
        os._exit(99)
    
     


def isKeywordsInLine(line, kwords):
    """Check to see if the line match any of the keywords.
    """
    found = False
     
    kwList = kwords.split (',')
    for keyword in kwList:
        #print "****keyword is %s." % keyword
        r1 = re.compile (keyword, re.IGNORECASE)
        if r1.search(line):
            print line
            found = True
            break 
      
    return found
    
    

if __name__ == "__main__":
    main(sys.argv[1:])
