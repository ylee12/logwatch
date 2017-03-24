# LogWatch

## Description
  This Python script is used to notify users that an exception had been generated from the application. It searches through a constantly changed log file and find any words that matches words from the provided list (see usage below), and send an email. This application keeps track of its last read location in the file, so subsequent execution of this application will continue from its last read location and so will not resend email to users for exeptions which were already read from the file.  

## Usage
python logwatch.py [options] 

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

  python logwatch.py -f /usr/local/bea/user_projects/domains/mtc/servers/App