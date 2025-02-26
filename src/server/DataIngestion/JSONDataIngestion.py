from .DataIngestion import DataIngestion
from ..DataProcessor.JSONDataProcessor import JSONDataProcessor
import json

class JSONDataIngestion(DataIngestion):
    def load_data(self, file_path):
        with open(file_path, 'r') as f:
            self.data = json.load(f)
    
    def create_processor(self):
        return JSONDataProcessor(self.data)