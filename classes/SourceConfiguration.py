import sys
from Configuration import Configuration
import xmltodict


class SourceConfiguration(Configuration):
    #constructor
    def __init__(self, SourceFile=None):
        #variables
        xml = ""
        CachedFilePath = "{}.cached".format(SourceFile)

        self.SourceFile = SourceFile

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

            except Exception, e:
                print("Unexpected error:", e)
                print("Configuration object failed to fully instantiate.")
                print("If this was a file I/O error please consider changing the path to the configuaration file.")


    def GetSourceInfo(self):
        return self.SourceMetaData


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
        return False
