from abc import ABCMeta, abstractmethod
import sys
import xmltodict


class Configuration:
    __metaclass__ = ABCMeta

    def __init__(self, SourceFile = None):
        self.SourceFile = SourceFile

    @abstractmethod
    def CheckForChanges(self):
        return False

    @abstractmethod
    def Update(self):
        return False




class SourceConfiguration(Configuration):
    #constructor
    def __init__(self, SourceFile=None):
        #variables
        xml = ""
        CachedFilePath = "{}.cached".format(SourceFile)
        self.SourceFile = SourceFile
        self.SourceMetaData = None

        #Only try to fetch configuration information
        # if a file source was given
        if SourceFile != None:
            try:
                with open(SourceFile) as CFile:
                    xml = CFile.read()
                    self.SourceMetaData = xmltodict.parse(xml)

                # Write cached file out for later comparision
                WFile = open(CachedFilePath, 'w+')
                WFile.write(xml)

            except Exception as e:
                print("Unexpected error:", e)
                print("Configuration object failed to fully instantiate.")
                print("If this was a file I/O error please consider changing the path to the configuaration file.")



    def GetSourceInfo(self):
        return self.SourceMetaData

    '''
    Checks for changes in the configuration file by comparing against
    a cached version of the configuration file.
    True = There has been changes
    False = There has been no changes
    '''
    def CheckForChanges(self):
        #replace with a speedy hash comparision function
        with open(self.SourceFile) as AFile:
            with open(self.SourceFile + ".cached") as BFile:
                if AFile.read() != BFile.read():
                    return True
                return False


    def UpdateFilePath(self, SourceFile):
        self.SourceFile = SourceFile



    def Update(self):
        #variables
        xml = ""
        CachedFilePath = "{}.cached".format(self.SourceFile)


        #Only try to fetch configuration information
        # if a file source was given
        if self.SourceFile != None:
                with open(SourceFile) as CFile:
                    xml = CFile.read()
                    self.SourceMetaData = xmltodict.parse(xml)

                # Write cached file out for later comparision
                WFile = open(CachedFilePath, 'w+')
                WFile.write(xml)
