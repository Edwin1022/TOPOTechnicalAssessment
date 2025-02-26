from .DataIngestion import DataIngestion
from ..DataProcessor.PDFDataProcessor import PDFDataProcessor
import tabula

class PDFDataIngestion(DataIngestion):
    def load_data(self, file_path):
        tables = tabula.read_pdf(file_path, pages='all')
        self.data = tables[0]

    def create_processor(self):
        return PDFDataProcessor(self.data)