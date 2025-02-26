from .JSONDataVisualization import JSONDataVisualization
from .CSVDataVisualization import CSVDataVisualization
from .PDFDataVisualization import PDFDataVisualization
from .PPTXDataVisualization import PPTXDataVisualization

class VisualizationFactory:
    @staticmethod
    def create_visualization(data_type: str, data):
        if data_type.lower() == 'json':
            return JSONDataVisualization(data)
        elif data_type.lower() == 'csv':
            return CSVDataVisualization(data)
        elif data_type.lower() == 'pdf':
            return PDFDataVisualization(data)
        elif data_type.lower() == 'pptx':
            return PPTXDataVisualization(data)
        else:
            raise ValueError(f"Unsupported data type: {data_type}. Supported types are 'json', 'csv', 'pdf' and 'pptx'.")