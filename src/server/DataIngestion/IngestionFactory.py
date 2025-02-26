from .JSONDataIngestion import JSONDataIngestion
from .CSVDataIngestion import CSVDataIngestion
from .PDFDataIngestion import PDFDataIngestion
from .PPTXDataIngestion import PPTXDataIngestion

class IngestionFactory:
    _ingestion_classes = {
        "json": JSONDataIngestion,
        "csv": CSVDataIngestion,
        "pdf": PDFDataIngestion,
        "pptx": PPTXDataIngestion
    }
    
    @classmethod
    def create_ingestion(cls, data_type):
        if data_type not in cls._ingestion_classes:
            raise ValueError(f"Unsupported data type: {data_type}")
            
        return cls._ingestion_classes[data_type]()