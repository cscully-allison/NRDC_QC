import sys
from Configuration import Configuration
import xmltodict


class SourceConfiguration(Configuration):
    def __init__(self, SourceFile=None):
        #variables
        xml = ""

        self.SourceFile = SourceFile

        try:
            with open(SourceFile) as CFile:
                xml = CFile.read()
                self.SourceMetaData = xmltodict.parse(xml)

            WFile = open("." + SourceFile + ".cached", 'w+')
            WFile.write(xml)

        except Exception, e:
            print("Unexpected error:", e)
            print("Configuration object failed to fully instantiate.")
            print("If this was a file I/O error please consider changing the path to the configuaration file.")

    def GetSourceInfo():
        return self.SourceMetaData

    def CheckForChanges():
        return False

    def Update():
        return False
