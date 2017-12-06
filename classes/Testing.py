from abc import ABCMeta, abstractmethod


class Tester:

    def __init__(self, TestParameters = None, DataStream = None):
        self.DataStream = DataStream
        self.TestParameters = TestParameters
        self.Tests = []
        self.TestedDataPoints = []

        self.Tests = self.ConstructTests(TestParameters)



    def RunTests(self):
        #variabales
        PossibleRepeatValues = []

        for Ndx, Measurement in enumerate(self.DataStream.Measurements):

            for Test in self.Tests:
                if Test.id == "OBT":
                    Tested = Test.RunTest(Measurement)
                    #if Tested.Flag != None:


                elif Test.id == "RVT":
                    NumDataPoints = Test.GetTestRequiredDataPoints()
                    if Ndx >= NumDataPoints:
                        PossibleRepeatValues = self.DataStream.Measurements[ Ndx-NumDataPoints : Ndx ]
                        PossibleRepeatValues.append( Measurement )
                        Tested = Test.RunTest( PossibleRepeatValues )

                elif Test.id == "MVT":
                    if Ndx >= 2:

    def ConstructTests(self, TestParams):
        #variabales
        Tests = []

        Tests.append( MissingValueTest() )

        for TestInfo in TestParams:
            if TestInfo["Type"] == "Bounds":
                Tests.append( OutOfBoundsTest( "OBT" , TestInfo["Max"], TestInfo["Min"] ) )
            elif TestInfo["Type"] == "Repeat Value":
                Tests.append( RepeatValueTest( "RVT" , TestInfo["RepeatThreshold"] ) )

        return Tests


class Test:

    __metaclass__ = ABCMeta

    def __init__(self, TestID = ""):
        self.id = TestID

    @abstractmethod
    def RunTest():
        return False



class MissingValueTest(Test):
    def __init__(self, TestID = "MVT"):
        self.id = TestID

    def RunTest(self, MasurementPair):
        #variables
        First = MeasurementPair[0]
        Second = MeasurementPair[1]

        #Compare zeorth measurement timestamp against 1st
        # If they are greater than 10mins apart create measuremt,
        # Flag and eject



class OutOfBoundsTest(Test):
    def __init__(self, TestID = "OBT", UpperBound = 0, LowerBound = 0):
        self.id = TestID
        self.Max = float(UpperBound)
        self.Min = float(LowerBound)

    def RunTest(self, Measurement):
        if Measurement.Value > self.Max:
            Measurement.setFlag(2)
            return Measurement

        elif Measurement.Value < self.Min:
            Measurement.setFlag(2)
            return Measurement

        else:
            return Measurement


class RepeatValueTest(Test):
    def __init__(self, TestID = "RVT", NumDataPoints=0):
        self.id = TestID
        self.NumDataPoints = int(NumDataPoints)

    #returns the number of datapoints required to
    #run the repeat value test includes the
    #datapoint to be measured
    def GetTestRequiredDataPoints(self):
        return self.NumDataPoints - 1

    def RunTest(self, MeasurementsList):

        if len(MeasurementsList) != self.NumDataPoints:
            raise ValueError

        TestedMeasurement = MeasurementsList[ self.NumDataPoints-1 ]
        MeasurementsList = MeasurementsList[:-1]

        #test the first element against all subsequent elements
        #if equivalent keep going elsewise kick out as unflagged
        for Measurement in MeasurementsList:
            if TestedMeasurement.Value != Measurement.Value:
                return TestedMeasurement

        TestedMeasurement.setFlag(1)
        return TestedMeasurement
