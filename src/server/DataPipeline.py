import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(root_dir))

from src.server.DataSource import DataSource
from src.server.DataIngestion.IngestionFactory import IngestionFactory
from src.server.APIHandler import APIHandler
import os

class DataPipeline:
    def __init__(self):
        datasets_dir = os.path.join(os.path.dirname(__file__), '../..', 'datasets')
        
        self.data_sources = [
            DataSource("json", os.path.join(datasets_dir, 'dataset1.json')),
            DataSource("csv", os.path.join(datasets_dir, 'dataset2.csv')),
            DataSource("pdf", os.path.join(datasets_dir, 'dataset3.pdf')),
            DataSource("pptx", os.path.join(datasets_dir, 'dataset4.pptx'))
        ]
        
        self.ingestors = []
        
        self.processed_data = {}
        
    def ingest_data(self):
        for source in self.data_sources:
            ingestor = IngestionFactory.create_ingestion(source.type)
            ingestor.load_data(source.file_path)
            self.ingestors.append(ingestor)
            
    def process_data(self):
        for ingestor in self.ingestors:
            processor = ingestor.create_processor()
            
            result = processor.process_data()
            
            data_type = processor.get_data_type()
            self.processed_data[data_type] = result

    def handle_api(self):
        json_data = self.processed_data.get('json')
        csv_data = self.processed_data.get('csv')
        pdf_data = self.processed_data.get('pdf')
        pptx_data = self.processed_data.get('pptx')
        api_handler = APIHandler(json_data, csv_data, pdf_data, pptx_data)
        api_handler.run()

    def run_pipeline(self):
        self.ingest_data()
        self.process_data()
        self.handle_api()

if __name__ == '__main__':
    pipeline = DataPipeline()
    pipeline.run_pipeline()