from .DataProcessor import DataProcessor
import pandas as pd

class CSVDataProcessor(DataProcessor):
    def __init__(self, csv_data):
        super().__init__(csv_data)
        self.csv_data = csv_data

    def process_data(self):
        self.csv_data['Date'] = pd.to_datetime(self.csv_data['Date'])
        self.csv_data = self.csv_data.rename(columns={
            'Revenue': 'Revenue (in $)'
        })
        return self.csv_data.to_dict(orient='records')
    
    def get_data_type(self):
        return 'csv'