'''
Created on Apr 15, 2015

@author: aavalosv

Last modification: Apr 15, 2016
@author: aavalosv
'''

from coverage import Coverage
from svnUpdater import svnUpdate, send_cmd
import os
from stat import *


'''
Testing script for svnUpdater
'''

cov = Coverage()
cov.start()

server = "https://shvssvn01.sh.intel.com/dcsg_repos/svn_degci_infra/degci_infra/configuration/"
server2 = "https://shvssvn01.sh.intel.com/dcsg_repos/svn_degci_infra/degci_infra/global_gdc.xml"
destination1 = r"C:\temp\Workpath"
destination2 = r"C:\temp\SvnFile"
destination3 = r"C:\temp\WorkpathRev"
destination4 = r"C:\temp\SvnFileRev"

#TC1 Create a Workpath
print "Create workpath"
if svnUpdate(destination1,server):
		print "It works!!"
else:
		print "Not yet"
#TC2 Workpath up to date
print "Workpath already updated"		
if svnUpdate(destination1,server):
		print "It works!!"
else:
		print "Not yet"
#TC3 Update workpath to a specific version
print "Update workpath to a specific version"
if svnUpdate(destination1,server, version = 1445):
		print "It works!!"
else:
		print "Not yet"
#TC4 Update workpath
print "Update Workpath"
if svnUpdate(destination1,server):
		print "It works!!"
else:
		print "Not yet"
#TC5 Create workpath for a file
print "Create workpath for a file"
if svnUpdate(destination2,server2):
		print "It works!!"
else:
		print "Not yet"
#TC6 File already up to date		
print "File already updated"
if svnUpdate(destination2,server2):
		print "It works!!"
else:
		print "Not yet"
#TC7 Update file to specific revision
print "Update file to a specific revision"
if svnUpdate(destination2,server2, version = 11):
		print "It works!!"
else:
		print "Not yet"
#TC8 Update file
print "Update file"
if svnUpdate(destination2,server2):
		print "It works!!"
else:
		print "Not yet"
#TC9
print "Create workpath for specific revision for a file"
if svnUpdate(destination3,server2, version = 10):
		print "It works!!"
else:
		print "Not yet"
#TC10
print "Create workpath for specific version"
if svnUpdate(destination4,server, version = 1445):
		print "It works!!"
else:
		print "Not yet"
#TC11
print "Error SVN source"
if svnUpdate(destination1,r"file:///C:/Users/error"):
		print "It works!!"
else:
		print "Not yet"

# TC12

send_cmd(IOError,"Error")

# TC13

send_cmd(ValueError, "Error")

# TC14
x = {1:3,2:"s",3:"2"}
send_cmd(x, "Error")

# TC15
send_cmd("svn info https://error.m", "Checks")

#Clean up
os.chmod(destination1, S_IWRITE )
send_cmd(r"rmdir " + destination1 + " /Q /S", "Deleting")
os.chmod(destination2, S_IWRITE )
send_cmd(r"rmdir " + destination2 + " /Q /S", "Deleting")
os.chmod(destination3, S_IWRITE )
send_cmd(r"rmdir " + destination3 + " /Q /S", "Deleting")
os.chmod(destination4, S_IWRITE )
send_cmd(r"rmdir " + destination4 + " /Q /S", "Deleting")

cov.stop()
cov.html_report(directory='covhtml')