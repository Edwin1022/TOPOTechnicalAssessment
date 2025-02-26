from .DataIngestion import DataIngestion
from ..DataProcessor.PPTXDataProcessor import PPTXDataProcessor
from pptx import Presentation

class PPTXDataIngestion(DataIngestion):
    def load_data(self, file_path):
        self.data = Presentation(file_path)

    def create_processor(self):
        return PPTXDataProcessor(self.data)