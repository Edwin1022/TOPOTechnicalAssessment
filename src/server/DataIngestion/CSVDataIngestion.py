from .DataIngestion import DataIngestion
from ..DataProcessor.CSVDataProcessor import CSVDataProcessor
import pandas as pd

class CSVDataIngestion(DataIngestion):
    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)

    def create_processor(self):
        return CSVDataProcessor(self.data)