'''
Created on Mar 30, 2015

@author: aavalosv

Last modification: Apr 18, 2016
@author: aavalos
'''

'''
API to handling updates and creating workpaths for SVN

'''

import subprocess
import re
import os
from stat import *
from time import sleep

def send_cmd(command, msg):
    '''
    Sends commands to the terminal

    Args:
        command(string): Command to be sent
        msg(string): Little message about the command sent

    Return:
        proc(string): output of command sent
    '''
    print('sendCmd: ' + msg)
    print(command)

    proc = ''
    try:
            proc = str(subprocess.check_output(command, universal_newlines=True, shell=True))
            return proc
    except subprocess.CalledProcessError as ex:
            return False, '{0}\n{1}'.format(proc, ex)
    except Exception, ex:
            return False, '{0}\n{1}'.format(proc, ex)

def svnChecker(destination, server):
    '''
    This function gets both revisions, local and source

    Args:
        destination(string): Address where it will be located the workpath
        server(string): SVN source

    Return:
        verS,verL(int): Revisions, local and SVN source
    '''
    svnLocal = send_cmd(r"svn info " + destination, "Checking version")
    print(svnLocal)
    resLcl = re.findall(r"Revision:\s\d+", svnLocal)

    svnServer = send_cmd("svn info " + server, "Checking version")
    print(svnServer)
    resSvr = re.findall(r"Revision:\s\d+", svnServer)

    print resLcl
    print resSvr

    verL = re.findall(r"\d+",resLcl[0])
    verS = re.findall(r"\d+",resSvr[0])

    verS = int(verS[0])
    verL = int(verL[0])
    
    return verS, verL

def svnUpdate(destination, server, version = None, user = "dcgciauto", password = "niaip64@"):
    '''
    Main function
    It checks if the workpath already exist in order to compare its revision with the source revision.
    Args:
        destination(string): Address where it will be located the workpath
        server(string): SVN source
        version(Optional[int]): Specify to update to a specific version

    Return:
        bool: True if successful, False otherwise.
    '''
    try:
            x = len(server)
            destination = destination.replace("/", "\\")

            if server[x-1] != '/':
                reXml = re.findall(r"\w+\.\w+$", server)
                server = server.replace(reXml[0], "")
                if not os.path.exists(destination):
                    print "Checking out"

                    if version is not None:
                        svnCheck = send_cmd(r"svn checkout -r" + str(version) + " " + server + " " + destination + " " + "--depth empty " + " --username=" + user + " --password=" + password, "Checking out to revision " + str(version))
                        print svnCheck
                        svnUp = send_cmd(r"svn up -r" + str(version) + " " + destination + "\\" + reXml[0] + " --username=" + user + " --password=" + password, "Updating")
                        return True

                    svnCheck = send_cmd(r"svn checkout " + server + " " + destination + " " + "--depth empty " + " --username=" + user + " --password=" + password, "Checking out")
                    print svnCheck
                    svnUp = send_cmd(r"svn up " + destination + "\\" + reXml[0] + " " + " --username=" + user + " --password=" + password, "Updating")
                    print svnUp
                    return True
                else:
                    verS, verL = svnChecker(destination,server)

                    if version is not None:
                        os.chmod(destination, S_IWRITE )
                        svnRm = send_cmd(r"rmdir " + destination + " /Q /S", "Deleting")
                        print svnRm
                        svnCheck = send_cmd(r"svn checkout -r" + str(version) + " " + server + " " + destination + " " + "--depth empty " + " --username=" + user + " --password=" + password, "Checking out to revision " + str(version))
                        print svnCheck
                        svnUp = send_cmd(r"svn up -r" + str(version) + " " + destination + "\\" + reXml[0] + " --username=" + user + " --password=" + password, "Updating")
                        return True

                    if (verS != verL):
                        os.chmod(destination, S_IWRITE )
                        svnRm = send_cmd(r"rmdir " + destination + " /Q /S", "Deleting")
                        print svnRm
                        svnCheck = send_cmd(r"svn checkout " + server + " " + destination + " " + "--depth empty " + " --username=" + user + " --password=" + password, "Checking out")
                        print svnCheck
                        svnUp = send_cmd(r"svn up " + destination + "\\" + reXml[0] + " --username=" + user + " --password=" + password, "Updating")
                        print svnUp
                        return True
                    else:
                        print "SVN Path up to date"
                        return True

            else:
                if not os.path.exists(destination):
                    print "Checking out"

                    if version is not None:
                        svnCheck = send_cmd(r"svn checkout -r" + str(version) + " " + server + " " + destination + " --username=" + user + " --password=" + password, "Checking out to revision " + str(version))
                        print svnCheck
                        return True

                    svnCheck = send_cmd(r"svn checkout " + server + " " + destination + " --username=" + user + " --password=" + password, "Checking out")
                    print svnCheck
                    return True
                else:
                    verS, verL = svnChecker(destination,server)

                    if version is not None:
                        svnR = send_cmd(r"svn revert -R " + destination + " --username=" + user + " --password=" + password, "Reverting Local Changes")
                        print svnR
                        svnUp = send_cmd(r"svn up -r" + str(version) + " " + destination + " --username=" + user + " --password=" + password, "Updating")
                        return True

                    if (verS != verL):
                        svnR = send_cmd(r"svn revert -R " + destination + " --username=" + user + " --password=" + password, "Reverting Local Changes")
                        print svnR
                        svnUp = send_cmd(r"svn up " + destination + " --username=" + user + " --password=" + password, "Updating")
                        return True
                    else:
                        print "SVN Path Up to date"
                        return True
    except Exception, ex:
        print "Error: " + str(ex)
        return False