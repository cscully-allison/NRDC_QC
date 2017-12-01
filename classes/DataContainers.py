class DataBundle:

    def __init__(self, BundleProperty=None, DataStreams=None):
        self.BundleProperty = BundleProperty
        self.DataStreams = DataStreams

    def SetProperty(self, BundleProperty):
        self.BundleProperty = BundleProperty

    def GetProperty(self):
        return self.BundleProperty

    def SetDataStreams(self, DataStreams):
        self.DataStreams = DataStreams

    def AddDataStream(self, DataStream):
        self.DataStreams.append(DataStream)

    def GetDataStreams(self):
        return self.DataStreams


class DataStream:

    def __init__
