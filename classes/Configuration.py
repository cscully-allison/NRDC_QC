import sys
import copy

from xml.dom.minidom import parseString, Document
from abc import ABCMeta, abstractmethod

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
        self.XMLString = ""

        #Only try to fetch configuration information
        # if a file source was given
        if SourceFile != None:
            try:
                with open(SourceFile) as CFile:
                    xml = CFile.read()
                    self.SourceMetaData = parseString(xml)
                    self.XMLString = xml

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
                    self.SourceMetaData = parseString(xml)

                # Write cached file out for later comparision
                WFile = open(CachedFilePath, 'w+')
                WFile.write(xml)

class TestConfiguration(Configuration):

        def __init__(self, SourceFile=None):
            #member variabales
            self.SourceFile = SourceFile
            self.SourceMetaData = None
            self.TestParameters = {}
            self.XMLString = ""

            #variables
            xml = ""
            CachedFilePath = "{}.cached".format(SourceFile)


            #Only try to fetch configuration information
            # if a file source was given
            if SourceFile != None:
                try:
                    with open(SourceFile) as CFile:
                        xml = CFile.read()
                        self.SourceMetaData = parseString(xml)
                        self.XMLString = xml

                    # Write cached file out for later comparision
                    WFile = open(CachedFilePath, 'w+')
                    WFile.write(xml)

                except Exception as e:
                    print("Unexpected error:", e)
                    print("Configuration object failed to fully instantiate.")
                    print("If this was a file I/O error please consider changing the path to the configuaration file.")

                self.TestParameters = self.ExtractTestParams(self.SourceMetaData)


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


        '''
            Write changes to existing test parameters as passed up from the user interface web site.
            Also write out new tests to our xml file with this function (maybe that should be a different function?).
        '''

        def WriteChanges(self, NewTestParams):
            #A temp test param object will be needed to store and write out new test params
            #WriteTP = copy.deepcopy(self.TestParameters);

            #NewTestParams is an object with one key which is the dsID
            #we can also push up multiple new or modified tests at the same time
            #with this interface
            #for key in NewTestParams:
            #    if(WriteTP):
            #        for ndx, test in enumerate(WriteTP[key]):
            #            if (test['Type'] == NewTestParams[key]['Type']):
            #                WriteTP[key][ndx] = NewTestParams[key]
            #    else:
            #        return

            #write out changes to source xml file
            #with open(self.SourceFile, 'w+') as FP:

            for key in NewTestParams:
                self.UpdateXML(key, NewTestParams[key])


            with open(self.SourceFile, 'w+') as fp:
                fp.write(self.SourceMetaData.toxml());


        def Update(self):
            #variables
            xml = ""
            CachedFilePath = "{}.cached".format(self.SourceFile)


            #Only try to fetch configuration information
            # if a file source was given
            if self.SourceFile != None:
                    with open(self.SourceFile) as CFile:
                        xml = CFile.read()
                        self.SourceMetaData = parseString(xml)

                    # Write cached file out for later comparision
                    WFile = open(CachedFilePath, 'w+')
                    WFile.write(xml)
                    WFile.close()


        """ Helper Functions """

        """
        Extracts and organizes test Parameters from the XML
        into the configuration object

        Returns: A dictionary which maps a datastream id to
                List of tests
        """
        def ExtractTestParams(self, TestXML):
            #variables
            DataStreams = None
            Tests = None
            TestHolder = {}
            AssociatedTests = []
            TestBundle = {}
            TestBundles = []

            #code
            DataStreams = TestXML.getElementsByTagName("DataStream")

            for Stream in DataStreams:
                StreamID = self.GetInnerXML(Stream.getElementsByTagName("Stream"))
                Tests = Stream.getElementsByTagName("Test")

                #append tests into this test bundle object
                #using a temporary dictionary load data
                #THIS CAN BE PUSHED OUT INTO A FUNCTION
                for Test in Tests:
                    TestHolder["Type"] = self.GetInnerXML(Test.getElementsByTagName("Type"))

                    if TestHolder["Type"] == "Bounds":
                        TestHolder["Max"] = self.GetInnerXML(Test.getElementsByTagName("Max"))
                        TestHolder["Min"] = self.GetInnerXML(Test.getElementsByTagName("Min"))

                    elif TestHolder["Type"] == "Repeat Value":
                        TestHolder["RepeatThreshold"] = self.GetInnerXML(Test.getElementsByTagName("RepeatThreshold"))

                    AssociatedTests.append(TestHolder)

                    TestHolder = {}

                TestBundle[StreamID] = AssociatedTests

                #TestBundles.append(TestBundle)

                #reset our temporary holders
                AssociatedTests = []
                #TestBundle = {}

            return TestBundle

        #Updates the XML from SourceMetaData with a singular bundle of new test parameters
        def UpdateXML(self, ModifiedDsID, NewTestParams):
            StreamExists = False
            TestExists = False
            DataStreams = self.SourceMetaData.getElementsByTagName("DataStream")

            modifiedTest = NewTestParams

            for Stream in DataStreams:
                StreamID = self.GetInnerXML(Stream.getElementsByTagName("Stream"))
                if(StreamID == ModifiedDsID):
                    StreamExists = True
                    Tests = Stream.getElementsByTagName("Test")

                    for Test in Tests:
                        if( NewTestParams["Type"] == self.GetInnerXML(Test.getElementsByTagName("Type")) ):
                            TestExists = True

                            for Param in NewTestParams:
                                if(Param != "Type"):
                                    Test.getElementsByTagName(Param)[0].firstChild.nodeValue = NewTestParams[Param]


            if not TestExists:
                NewTestNode = self.CreateTest(NewTestParams)

                #append new test to existing stream


            if not StreamExists:
                Stream = self.CreateStream(NewTestNode, ModifiedDsID)

                print(Stream)

                #we have to modify the data source config file here as well
                self.AddStreamToDataSourceConfig(ModifiedDsID)


        #---------HARDCODED TO BE REPLACED WITH A BETTER ARITECTURAL DESIGN-------
        def AddStreamToDataSourceConfig(self, dsID):
            ConfigDOM = None
            NewNode = None
            TestedDataStreams = None

            with open("../config/datasource.config") as CFile:
                xml = CFile.read()
                ConfigDOM = parseString(xml)

            NewNode = ConfigDOM.createElement("Stream")
            NewNode.appendChild(ConfigDOM.createTextNode(dsID))

            TestedDataStreams = ConfigDOM.getElementsByTagName("TestedDataStreams")[0]
            TestedDataStreams.appendChild(NewNode)

            print( ConfigDOM.toxml() )


        def CreateTest(self, NewTestParams):
            #create a node called test
            NewTest = self.SourceMetaData.createElement("Test")

            #create text node each paramter and append to test
            for parameter in NewTestParams:
                TempParam = self.SourceMetaData.createElement(parameter)
                TempParam.appendChild( self.SourceMetaData.createTextNode(NewTestParams[parameter]) )
                NewTest.appendChild(TempParam)

            return NewTest

        def CreateStream(self, NewTestNode, DsID):
            NewStream = self.SourceMetaData.createElement("DataStream")

            StreamIDNode = self.SourceMetaData.createElement("Stream")
            StreamIDNode.appendChild( self.SourceMetaData.createTextNode(DsID) )

            NewStream.appendChild(StreamIDNode)
            NewStream.appendChild(NewTestNode)

            return NewStream


        def GetInnerXML(self, node):
            return node[0].firstChild.nodeValue
