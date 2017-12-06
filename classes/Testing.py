class Tester:
    def __init__(self, TestParameters = None, DataStream = None):
        self.Datastream = DataStream
        self.TestConfiguration = TestConfiguration



class Test:

    __metaclass__ = ABCMeta

    def __init__(self, TestID = ""):
        self.id = TestID

    @abstractmethod
    def RunTest():
        return False

class MissingValueTest(Test):
    def __init__(self, TestID = ""):
        self.id = TestID

    def RunTest(MasurementPair):
        #variables
        First = MeasurementPair[0]
        Second = MeasurementPair[1]

        #Compare zeorth measurement timestamp against 1st
        # If they are greater than 10mins apart create measuremt,
        # Flag and eject



class OutOfBoundsTest(Test):
    def __init__(self, TestID = "", UpperBound = 0, LowerBound = 0):
        self.id = TestID
        self.Max = UpperBound
        self.Min = LowerBound

    def RunTest(Measurement):
        if Measurement.Value > self.Max:
            Measurement.SetFlag(1)
            return Measurement

        elif Measurement.Value < self.Min:
            Measurement.SetFlag(1)
            return Measurement

        else:
            return Measurement


class RepeatValueTest(Test):
    def __init__(self, TestID = "", NumDataPoints=0):
        self.id = TestID
        self.NumDataPoints = NumDataPoints

    def GetTestRequiredDataPoints():
        return self.NumDataPoints

    def RunTest(MeasurementsList):
        if len(MeasurementsList) != self.NumDataPoints:
            raise ValueError

        #test the first element against all subsequent elements
        #if equivalent keep going elsewise kick out as unflagged
        for Measurement in MeasurementsList:
            if MeasurementsList[0].Value != Measurement.Value:
                return Measurements

        Measurement[0].SetFlag(2)
        return Measurement[0]
