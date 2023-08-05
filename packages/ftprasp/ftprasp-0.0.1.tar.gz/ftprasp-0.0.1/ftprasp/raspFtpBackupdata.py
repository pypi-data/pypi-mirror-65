import os
import os.path
from ftplib import FTP
from dateutil import parser
import fnmatch
import time
import reconnecting_ftp
from datetime import datetime

print('Start Backup Process.......................................................................')

class ftprasp:

    def __init__(self, hostname, user, password, port, mainRaspberry, mainExternalhd):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.port = port
        self.mainRasp = mainRaspberry
        self.mainExternalhd = mainExternalhd
        self.copyright = "Copyright (c) Kanutsanun Bouking"

        print(self.copyright)

        '''mainRaspberry = Mainpath to backup data on Raspberry Pi sd card
        mainExternalhd = Mainpath to backup data on External Hardisk which is connected to Raspberry Pi
        dirFTP = Data directory(actually is folder name) on FTP server
        dirLOCAL = Foldername on backup directory'''

    def __str__(self):
        return "Login to: {}\nuser: {}\nport: {}".format(self.hostname, self.user, self.port)
    
    def process_Raspberry(self, dirFTP, dirLOCAL):

        print('Start backup to Raspberry Pi............................................................')
        localpath = self.mainRasp+'/'+dirLOCAL+'/'
        localfiles = os.listdir(localpath)
        #print(localfiles)

        with reconnecting_ftp.Client(self.hostname, self.port, self.user, self.password) as ftp:
            ftp.cwd(dirFTP)
            FTPcurrentDir = ftp.pwd()
            FTPfiles = ftp.mlsd(FTPcurrentDir) #list files in ftp path
            # print(FTPcurrentDir)

            for i in FTPfiles:
                FTPfileName = i[0]
                ftpMtime = parser.parse(i[1]['modify'])

                if not os.path.exists(self.mainRasp+'/'+dirLOCAL+'/'+ FTPfileName):
                    print ('Downloading to Raspberry pi %s - Modified %s' %(FTPfileName, ftpMtime))
                    ftp.retrbinary('RETR %s'%(FTPcurrentDir+'/'+FTPfileName), open(self.mainRasp+'/'+dirLOCAL+'/'+FTPfileName, 'wb').write)
                    time.sleep(10)
                else:
                    print('%s Already in LOCAL - Checking modified' %FTPfileName)
                    for localname in localfiles:

                        if fnmatch.fnmatch(localname, FTPfileName) is True:
                            localMtime = datetime.strptime(time.ctime(os.path.getmtime(localpath+localname)), '%a %b %d %H:%M:%S %Y')
                            #=======Checking modified data, Time is UTC=======
                            # print('FTP:   %-5s %s %s %s' %(' ', FTPfileName, ftpMtime, type(ftpMtime)))
                            # print('Local: %-5s %s %s %s' %(' ', localname, localMtime, type(localMtime)))
                        
                            if ftpMtime > localMtime:
                                print('FTP data was modified...Sending %s to Local backup' %FTPfileName)
                                ftp.retrbinary('RETR %s'%(FTPcurrentDir+'/'+FTPfileName), open(self.mainRasp+'/'+dirLOCAL+'/'+FTPfileName, 'wb').write)
                                time.sleep(5)
                            else:
                                print('%s Data on FTP server was not modified' %FTPfileName)


        print('Raspberry pi is checking back to FTP server............................................................')
        localpath = self.mainRasp+'/'+dirLOCAL+'/'
        localfiles = os.listdir(localpath)
        # print(localfiles, type(localfiles))

        with reconnecting_ftp.Client(self.hostname, self.port, self.user, self.password) as ftp:
            ftp.cwd(dirFTP)
            FTPcurrentDir = ftp.pwd()
            FTPfiles = ftp.mlsd(FTPcurrentDir) #list files in ftp path
            listFtp_FileName = []
            for file in FTPfiles:
                FTPfileName = file[0]
                listFtp_FileName.append(FTPfileName)
            # print(listFtp_FileName, type(listFtp_FileName))
        diff = list(set(localfiles) - set(listFtp_FileName))
        print("%s is not appear on FTP server" %diff)
        if diff != []:
            for file in diff:
                os.remove(self.mainRasp+'/'+dirLOCAL+'/'+file)
                print("{} was removed from Raspberry Pi".format(file))
        else:
            print("Nothings change")

    def process_ExternalHd(self, dirFTP, dirLOCAL):

        print('Start backup to ExternalHd.......................................................................................')
        localpath = self.mainExternalhd+'/'+dirLOCAL+'/'
        localfiles = os.listdir(localpath)

        with reconnecting_ftp.Client(self.hostname, self.port, self.user, self.password) as ftp:
            ftp.cwd(dirFTP)
            FTPcurrentDir = ftp.pwd()
            FTPfiles = ftp.mlsd(FTPcurrentDir) #list files in ftp path

            for i in FTPfiles:
                FTPfileName = i[0]
                ftpMtime = parser.parse(i[1]['modify'])

                if not os.path.exists(self.mainExternalhd+'/'+dirLOCAL+'/'+ FTPfileName):
                    print ('Downloading to ExternalHd %s - Modified %s' %(FTPfileName, ftpMtime))
                    ftp.retrbinary('RETR %s'%(FTPcurrentDir+'/'+FTPfileName), open(self.mainExternalhd+'/'+dirLOCAL+'/'+FTPfileName, 'wb').write)
                    time.sleep(5)
                else:
                    print('%s Already in LOCAL - Checking modified' %FTPfileName)
                    for localname in localfiles:

                        if fnmatch.fnmatch(localname, FTPfileName) is True:
                            localMtime = datetime.strptime(time.ctime(os.path.getmtime(localpath+localname)), '%a %b %d %H:%M:%S %Y')
                            #=======Checking modified data, Time is UTC=======
                            # print('FTP:   %-5s %s %s %s' %(' ', FTPfileName, ftpMtime, type(ftpMtime)))
                            # print('Local: %-5s %s %s %s' %(' ', localname, localMtime, type(localMtime)))
                        
                            if ftpMtime > localMtime:
                                print('FTP data was modified...Sending %s to Local backup' %FTPfileName)
                                ftp.retrbinary('RETR %s'%(FTPcurrentDir+'/'+FTPfileName), open(self.mainExternalhd+'/'+dirLOCAL+'/'+FTPfileName, 'wb').write)
                                time.sleep(5)
                            else:
                                print('%s Data on FTP server was not modified' %FTPfileName)

        print('ExternalHd is checking back to FTP server.............................................................................')
        localpath = self.mainExternalhd+'/'+dirLOCAL+'/'
        localfiles = os.listdir(localpath)
        # print(localfiles, type(localfiles))

        with reconnecting_ftp.Client(self.hostname, self.port, self.user, self.password) as ftp:
            ftp.cwd(dirFTP)
            FTPcurrentDir = ftp.pwd()
            FTPfiles = ftp.mlsd(FTPcurrentDir) #list files in ftp path
            listFtp_FileName = []
            for file in FTPfiles:
                FTPfileName = file[0]
                listFtp_FileName.append(FTPfileName)
            # print(listFtp_FileName, type(listFtp_FileName))
        diff = list(set(localfiles) - set(listFtp_FileName))
        print("%s is not appear on FTP server" %diff)
        if diff != []:
            for file in diff:
                os.remove(self.mainExternalhd+'/'+dirLOCAL+'/'+file)
                print("{} was removed from ExternalHd".format(file))
        else:
            print("Nothings change")

  
              
if __name__=='__main__':
    
    obj = ftprasp(hostname='', user='', password='', port=21, mainRaspberry="", mainExternalhd="")
    print(obj)
    obj.process_Raspberry(dirFTP='', dirLOCAL='')
    obj.process_ExternalHd(dirFTP='', dirLOCAL='')