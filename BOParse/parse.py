from ftplib import FTP
import ftplib
import sys
import os

import zipfile

import argparse
import json

import traceback

# pip install pysftp - required:
import pysftp

import time
# pip install progressbar2 - required:
import progressbar
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, AdaptiveETA, AbsoluteETA, AdaptiveTransferSpeed

import logging

#for asOfDate:
import re
import datetime


# test enviroment with valid credentials:
# vmcos7apache01.YourCompanyinc.com
# bouser
# back0ffice

#console parameters parsing:
argument_parser = argparse.ArgumentParser(description='Downloading \
and starting processing BO for specific FCM')
argument_parser.add_argument('FCMName_Arg',
type=str, help='valid FCM name required')

args = argument_parser.parse_args()

# checking FCM and validate JSON configuration:
with open('json_config.json', 'r') as cfg:
    try:
        FCM_Config_data = json.load(cfg)
        if args.FCMName_Arg not in FCM_Config_data:
            sys.exit(" ----- No such FCM in config file. Exiting. ----- ")
        else:
            # release memory
            cfg = None
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(" ----- Invalid configuration, see details above ----- ")

# determine variables:
FCMNameVariable = args.FCMName_Arg
logFileName=FCMNameVariable + '_log.txt'

# create FCM Directory if not exists:
os.makedirs(FCMNameVariable, exist_ok=True)
# making 'Files' directory, if not exists:
os.makedirs(os.path.join(FCMNameVariable, 'Files'), exist_ok=True)
# making 'Archive' directory, if not exists:
os.makedirs(os.path.join(FCMNameVariable, 'Archives'), exist_ok=True)

# redefinition FTP class with :
class MyFTP(FTP):
    """ 1. inheriting FTP class
        2. reinitialization of sanitize meth`od
        3. adding logging in our MyFTP class
    """

    def _init__(self, *args):
        super(MyFTP, self).__init__(*args)

    @staticmethod
    def logger():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s : %(levelname)s : %(name)s : %(message)s',
            filename=os.path.join(FCMNameVariable, logFileName), # FCMNameVariable + '/' + logFileName,
            filemode='w'
        )
        logger = logging.getLogger('FTP')
        return logger

    def sanitize(self, *args):
        logger = self.logger()
        response = FTP.sanitize(self, *args)
        logger.debug(response)
        return response

    def write(self, *args):
        logging.info(*args) # writing to _log file



# Logger #3:
# creating logger:
logger = logging.getLogger("") # Root instance logger
logger.setLevel(logging.INFO) # Debug level. Welcome to flood of logging :)

# creating handler:
loggerHandler = logging.FileHandler(os.path.join(FCMNameVariable, logFileName), 'w') # FCMNameVariable + '/' + logFileName
loggerHandler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s','%Y-%m-%d %H:%M:%S'))
loggerHandler.propagate = True # probably useless.

# adding handler to logger:
logger.addHandler(loggerHandler)


# creating SFTP logger:
# CMD output stream handler:
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)

# create stdout logger:
consoleLogger = logging.StreamHandler(sys.stdout)
consoleLogger.setLevel(logging.INFO)
consoleLogger.propagate = True
# adding handler to logger:
logger.addHandler(consoleLogger)



# printing parsed arg from CMD:
logging.info(args.FCMName_Arg)

#ConfigFTPIP = "undefined"
ConfigAsOfDateType = "undefined"

#case sensetive:
def main(FCMName):
    if(FCMName):
        try:
            logging.info(" ----- Opening configuration file ----- ")
            with open('json_config.json', 'r') as config_file_pipeline:
                FCM_Config_data = json.load(config_file_pipeline)

                #checking keys in configuration:
                try:
                    logging.info(" ----- Checking FCM configuration ----- ")

                    if FCMName in FCM_Config_data:

                        if ('File_list' not in FCM_Config_data[FCMName]) or ('FTP' not in FCM_Config_data[FCMName]) or ('AsOfDate' not in FCM_Config_data[FCMName]):
                            logging.info(' ----- Not all required parameters was given from configuration! ----- ')
                            logging.info(' ----- Please check sections: File_list, FTP, AsOfDate  ----- ')
                            sys.exit("Not full configuration. Exiting.")
                        # FCM_Config_data[FCMName]['FTP']['FTP_IP']
                        # FCM_Config_data[FCMName]['FTP']['FTP_login']
                        # FCM_Config_data[FCMName]['FTP']['FTP_password']
                        else:

                            #read FCM configuration and initialize all variables:
                            global ConfigFTPIP
                            ConfigFTPIP = FCM_Config_data[FCMName]['FTP']['FTP_IP']


                            if 'FTP_folder' in FCM_Config_data[FCMName]['FTP']:
                                FTPFolderPath=FCM_Config_data[FCMName]['FTP']['FTP_folder']
                            else:
                                FTPFolderPath=""

                            # create list of arguments, based on configuration:
                            global ConfigAsOfDateType
                            global ConfigAsOfDateMask
                            global ConfigAsOfDateBeginOfString
                            global ConfigAsOfDateOutMask

                            try:
                                ConfigAsOfDateType = FCM_Config_data[FCMName]['AsOfDate']['Type']
                            except:
                                pass

                            try:
                                ConfigAsOfDateMask = FCM_Config_data[FCMName]['AsOfDate']['Mask']
                            except:
                                logging.info(" ----- WARNING! AsOfDateMask not defined ----- hh")
                                pass

                            try:
                                ConfigAsOfDateBeginOfString = FCM_Config_data[FCMName]['AsOfDate']['BeginOfString']
                            except:
                                pass

                            try:
                                ConfigAsOfDateOutMask = FCM_Config_data[FCMName]['AsOfDate']['OutMask']
                            except:
                                pass

                            arguments = [FCM_Config_data[FCMName]['FTP']['FTP_IP'],
                                                     FCM_Config_data[FCMName]['FTP']['FTP_login'],
                                                     FCM_Config_data[FCMName]['FTP']['FTP_password'],
                                                     FTPFolderPath,
                                                     FCM_Config_data[FCMName]['File_list'],
                                                     ConfigAsOfDateType]


                            # if 'Type' in FCM_Config_data[FCMName]['AsOfDate']:
                            #     if FCM_Config_data[FCMName]['AsOfDate']['Type'] == '2':
                            #         logging.info(' ----------------------------------------------------------------------------------------------------------------------------- TYPE = 2 ----------')
                            #         arguments.extend(FCM_Config_data[FCMName]['AsOfDate']['Type'])
                            #     else:
                            #         arguments.extend('0')
                            #     #other if's about asOfDate Types:
                            # else:
                            #     logging.info(' ----- Type of AsOfDate not found ----- ')
                            #     sys.exit("Check AsOfDate configuration")


                            # checking if we should use SFTP instead of FTP:
                            if(FCM_Config_data[FCMName]['FTP']['FTP_mode'] == 'SFTP'):
                                logging.info(' ----- SFTP flag Detected ----- ')
                                # call download from SFTP function:
                                try:
                                    logging.info(" ----- Starting connection to SFTP: ----- ")
                                    getFilesFromSFTP(*arguments)
                                    logging.info(" ----- SFTP connection closed ----- ")
                                except KeyError:
                                    print(traceback.format_exc())
                            else:
                                #call download from FTP function:
                                try:
                                    logging.info(" ----- Starting connection to FTP: ----- ")
                                    getFilesFromFTP(*arguments)
                                    logging.info(" ----- FTP connection closed ----- ")
                                except KeyError:
                                    print(traceback.format_exc())

                            #AsOfDate should be here:

                            try:
                                commandToRun = "GMI.exe " + FCMName + " -d 2016/11/28"
                                os.chdir(FCMName)
                                logging.info(" ----- Running command: " + commandToRun + " in " + os.getcwd())
                                runExternalProcess(commandToRun)
                            except Exception as e:
                                logging.info(e)

                    else:
                        logging.info(" ----- No such FCM in configuration! ----- ")



                except KeyError:
                    logging.info(" ----- Configuration Key error: Wrong KEY was set. \
                    Or no such FCM in configuration. Or configuration incorrect ----- ")
                    print (traceback.format_exc())

        except ValueError as e:
            print(e)
        except KeyError:
            logging.info (" ----- No such FCM was found in Configuration. \
            Incorrect FCMName was passed as parameter ----- ")

    else:
        logging.info(" ----- FCMName parameter parser error ----- ")



# define function, which works with SFTP:
def getFilesFromSFTP(SFTP_IP,
                     SFTP_Login,
                     SFTP_Password,
                     SFTP_Folder,
                     file_list,
                     asOfDateType):
    # define additional parameters:
    cnopts = pysftp.CnOpts()
    # disable host key checking:
    cnopts.hostkeys = None
    with pysftp.Connection(SFTP_IP, username=SFTP_Login, password=SFTP_Password,
                           cnopts=cnopts) as sftp:
        # output current directory:
        logging.info(' ----- Current directory: ' + sftp.pwd + ' ----- ')
        for dirAttributes in sftp.listdir_attr():
            logging.info(dirAttributes)
        # if folder param not empty and destination folder exists - change working directory:
        try:
            if SFTP_Folder != "":
                # check if directory exists, and then change working directory:
                if sftp.exists(SFTP_Folder):
                    logging.info(' ----- Changing working directory to: ' + SFTP_Folder + ' ----- ')
                    sftp.chdir(SFTP_Folder)
                    logging.info(' ----- Current directory: ' + sftp.pwd + ' ----- ')
                    for dirAttributes in sftp.listdir_attr():
                        logging.info(dirAttributes)
        except KeyError as e:
            print(e)

        #asOfDateType - checking the directory for files under mask:
        if asOfDateType == 'FromFileNameOnFTP':
            #global ConfigFTPIP
            #validFileList=[]
            validFileList = {}
            logging.info(asOfDateType)
            for fileNamesOnFTP in sftp.listdir():
                logging.info(fileNamesOnFTP)
                for file in file_list:
                    DateValidationResult = ValidateDateFromString(fileNamesOnFTP, ConfigAsOfDateBeginOfString,
                                                              ConfigAsOfDateMask, ConfigAsOfDateOutMask)
                    # checking names of files on FTP with the filename mask and date mask from configuration:
                    if file in fileNamesOnFTP and DateValidationResult is not False:
                        logging.info("+++yes")
                        ##validFileList.append(fileNamesOnFTP)
                        #validFileList.extend(DateValidationResult)
                        #generating array of 'filename':'valid date'
                        validFileList[fileNamesOnFTP]=DateValidationResult
                        #ValidProcess = ValidateDateFromString(fileNamesOnFTP,"TRUE","%Y%m%d")
                        logging.info(type(DateValidationResult))
                        #logging.info(ValidProcess)
                    #else:
                        #logging.info("---no")
            logging.info(validFileList)
            #logging.info(max(validFileList))
            filesDatesList = []
            for ValidPairs in validFileList:
                logging.info(ValidPairs) # filename
                logging.info(validFileList[ValidPairs]) #filedate
                filesDatesList.append(validFileList[ValidPairs])


                LastDate = datetime.datetime.strptime(validFileList[ValidPairs], ConfigAsOfDateOutMask).date()

                LastDate = max(validFileList[ValidPairs])
                logging.info(LastDate)
                #datetime.datetime.da

            logging.info(filesDatesList)
            logging.info(max(filesDatesList))

            logging.info(validFileList[max(filesDatesList)])

            # ValidateDateFromString ?

            #ValidateDateFromString()

        #file_list = validFileList



        try:
            if file_list:
                for fileName in file_list:
                    try:
                        if sftp.exists(fileName):
                            filepathVariable = os.path.join(FCMNameVariable, 'Files', fileName)
                            logging.info(' ----- Starting download file ' + fileName+ ' to local path: ' + filepathVariable + ' ----- ')
                            #progress bar inserting:
                            sftp.get(fileName,localpath=filepathVariable,callback=printProgressBar)
                            logging.info(' ----- File ' + fileName + ' downloaded to ' + filepathVariable +  ' ----- ')
                            # unzipping:
                            if (zipfile.is_zipfile(filepathVariable)):
                                logging.info(' ----- Extracting ' + filepathVariable + ' ----- ')
                                unZipFiles(filepathVariable, os.path.join(FCMNameVariable, 'Files'))
                            else:
                                logging.info(' ----- ' + filepathVariable + ' is not a valid ZIP-file, skipping ----- ')
                        else:
                            logging.info(' ----- WARNING! No such file on FTP: ' + fileName + ' ----- ')
                            # this warning should be emailed to GWOPS.
                            # but script will continue to working.
                    except:
                        print(traceback.format_exc())
            else:
                logging.info('----- WARNING! File list in configuration is empty!')
        except KeyError as e:
            print(e)


#bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)

def printProgressBar(param1, param2):
    widgets = ['Downloading progress: ', Percentage(), ' ', Bar(), ETA(), ' ', FileTransferSpeed()]
    bar = progressbar.ProgressBar(max_value=param2,widgets=widgets)
    bar.update(param1)

#this global variable is defined especially for ftplib stupid library to make progressbar possible feature:
amount_of_bytes_downloaded=0

def FTPFileHandlerWithProgressBar(block, filehandler, file_size):
    global amount_of_bytes_downloaded
    #write to file:
    writtendata = filehandler.write(block)
    amount_of_bytes_downloaded = amount_of_bytes_downloaded + writtendata
    bar = progressbar.ProgressBar(max_value=file_size)
    bar.update(amount_of_bytes_downloaded)





# define fucntion, which works with FTP:
def getFilesFromFTP(FTP_IP,
                        FTP_Login,
                        FTP_Password,
                        FTP_Folder,
                        file_list):

    #handle exceptions:
    try:
        logging.info(" ----- Connecting to:" + FTP_IP + " under " + FTP_Login + " user ----- ")
        ftp = MyFTP(FTP_IP,user=FTP_Login, passwd=FTP_Password) #MyFTP instead of FTP
        # set_debuglevel(N), where N - 0 or 1 or 2 - different levels of logging info.
        ftp.set_debuglevel(0)
        logging.info(" ----- Current directory: ----- ")
        ftp.retrlines('LIST', ftp.write)
        #check fot FTP_Folder parameter, if was set in configuration or not:
        if (FTP_Folder != ""):
            logging.info(' ----- Go to ' + FTP_Folder + ' directory ----- ')
            try:
                #using depricated nlst method, but it works fine.
                #checking if folder exists on FTP server:
                if (FTP_Folder in ftp.nlst()):
                    #ftp.cwd('/' + FTP_Folder)
                    ftp.cwd(os.path.basename(FTP_Folder))
                    #ftp.cwd(FTP_Folder)
                    logging.info(' ----- Current directory: ' + FTP_Folder + ' ----- ')
                    ftp.retrlines('LIST', ftp.write)
                else:
                    logging.info(' ----- No such directroy on FTP: ' + FTP_Folder + ' ----- ')
                    sys.exit('Wrong directory name. Exiting')
            except ValueError as e:
                print(e)

        try:
            if file_list:
                for file_to_download in file_list:
                    try:
                        if (file_to_download in ftp.nlst()):
                            filepathVariable = os.path.join(FCMNameVariable, 'Files', file_to_download)
                            logging.info(" ----- downloading " + file_to_download + " file ----- ")
                            file_size=ftp.size(file_to_download)
                            filehandler = open(filepathVariable, 'wb')
                            global amount_of_bytes_downloaded
                            amount_of_bytes_downloaded = 0

                            ftp.retrbinary('RETR ' + file_to_download,
                                           callback=lambda block: FTPFileHandlerWithProgressBar(block, filehandler, file_size))
                            filehandler.close()

                            logging.info(" -----  downloading file " + file_to_download + " completed ----- ")
                            #unzipping:
                            if (zipfile.is_zipfile(filepathVariable)):
                                logging.info(' ----- Extracting ' + filepathVariable + ' ----- ')
                                unZipFiles(filepathVariable, os.path.join(FCMNameVariable, 'Files'))
                            else:
                                logging.info(' ----- ' + filepathVariable + ' is not a valid ZIP-file, skipping ----- ')
                        else:
                            logging.info(' ----- WARNING! No such file on FTP: ' + file_to_download + ' ----- ')
                            # this warning should be emailed to GWOPS.
                            # but script will continue to working.
                    except:
                        print(traceback.format_exc())
            else:
                logging.info('----- WARNING! File list in configuration is empty!')
                sys.exit('No file list given. Exiting')
        except:
            print(traceback.format_exc())

    except ftplib.all_errors as e:
        print(e)

def unZipFiles(zipFileName, pathToUnzip):
    try:
        with zipfile.ZipFile(zipFileName, 'r') as openArchive:
            # get file list in archive
            #logging.info(openArchive.namelist())
            # go through file list:
            for ArchivedFile in openArchive.namelist():
                # #get file name
                data = openArchive.read(ArchivedFile)
                filename = os.path.basename(ArchivedFile)
                # skip directories
                if not filename:
                    continue
                else:
                    os.makedirs(pathToUnzip, exist_ok=True)
                    with open(os.path.join(pathToUnzip,filename), 'wb') as saveToFile:
                        saveToFile.write(data)

        logging.info(' ----- renaming original archive to ' + zipFileName + ' _extracted.zip ----- ')
        try:
            os.rename(zipFileName, zipFileName + '_extracted.zip')
            logging.info(' ----- Successfully renamed  ----- ')
        except Exception as e:
            # this alarm should be emailed to GWOPS:
            logging.info(e)
            logging.info(' ----- Warning! Failed to rename ZIP file ' + zipFileName + ' ----- ')
    except Exception as e:
        logging.info(' ----- Failed to extract ZIP file ' + zipFileName + ' with reason: ' + ' ----- ')
        logging.info(e)


def runExternalProcess(stringToRunProcess):
    import subprocess
    returnCodesDict = {1: 'std::exception caught, see log message for more details.',
                       2: 'Unknown exception caught.  Further investigation is needed.',
                       4: 'Account parse not successful, see Generic Parser Ops guide for details',
                       8: 'Currency parse not successful, see Generic Parser Ops guide for details',
                       12: 'Account and Currency parse not successful',
                       }
    try:
        external_process = subprocess.run(
            #"GMI.exe Penson -d 2016/11/28",
            stringToRunProcess,
            shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=True  # works as #external_process.check_returncode()
        )

        if external_process.returncode == 0:
            logging.info('Successful parsed')

    except subprocess.CalledProcessError as e:
        logging.info(e)
        if e.returncode in returnCodesDict:
            logging.info(returnCodesDict.get(e.returncode))
        else:
            logging.info('Unknown return code')






#AsOfDate-related functions:
def ReadAsOfDateFromStatementFiles(fileName,lineNumber):
    #if lineNumber == 'AUTO':
    with open(fileName) as filepipeline:
        for stringnum, filepipeline in enumerate(filepipeline, 1):
            if lineNumber == 'AUTO' and stringnum < 10:
                print("searching for asOfDate value in line# " + str(stringnum) + ", " + filepipeline)
                snippedString = ReadAsOfDateFromString(filepipeline)
                print("Validating AsOfDate from string")
                validDateFlag = ValidateDateFromString(snippedString) ###############################################
                if validDateFlag != False:
                    print(validDateFlag + " - Date is valid")
                    return validDateFlag
                    #raise StopIteration
                    #return
                    #print(lineNumber)
                else:
                    print("NO AS OF DATE FOUND")
            else:
                if stringnum == lineNumber:
                    print("searching for asOfDate value in line# " + str(stringnum) + ", " + filepipeline)
                    snippedString = ReadAsOfDateFromString(filepipeline)
                    validDateFlag = ValidateDateFromString(snippedString) ###############################################
                    if validDateFlag != False:
                        print(validDateFlag + " - Date is valid")
                        return validDateFlag
                    #else:
                        #print("NO AS OF DATE FOUND")

def ReadAsOfDateFromString(stringValue):
    print("Removing extra symbols from string")
    snippedString = re.sub("[^0-9]", "", stringValue)
    print(snippedString)
    return snippedString
    #print(snippedString[0:4])
    #preferred mask is: YYYY MM DD



def ValidateDateFromString(dateString, beginOfStringFlag, dateMask, dateOutMask):
    #dateMask = 'YYYYMMDD'
    #datetime.datetime(year=2017, month=12, day=10)
    #dateString=int(dateString)
    try:
        if(beginOfStringFlag == 'FALSE'):
            #.date() method in the end is removing datetime from the string
            #validDate = datetime.datetime.strptime(dateString[-8:], '%Y%m%d')
            validDate = datetime.datetime.strptime(dateString[-8:], dateMask).date()
        else:
            #validDate = datetime.datetime.strptime(dateString[:8], '%Y%m%d')
            validDate = datetime.datetime.strptime(dateString[:8], dateMask).date()

        logging.info(validDate)
        logging.info(type(validDate))
        asOfDateValue = validDate.strftime(dateOutMask)
        logging.info(asOfDateValue)
        return asOfDateValue
    except Exception as e:
        #print(e)
        return False

def DetectLastFilesOnFTP(filelist):
    try:
        logging.info("DetectLastFilesOnFTP")
    except Exception as e:
        print(e)
        return False



# STARTING PYTHON:
if __name__ == "__main__":
    main(FCMNameVariable)



# ERROR-LIST:
# [Errno 11004] getaddrinfo failed - Hostname didn't resolved or doesn't exists [Not valid host-name]
# 530 Login incorrect.
# 550 Failed to open file. - no permission, maybe file doesn't exist OR there is folder with such name (not a file!)
# 550 Could not get file size. - probably wrong name of file or it's not a file!

