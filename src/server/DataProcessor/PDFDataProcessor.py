from .DataProcessor import DataProcessor

class PDFDataProcessor(DataProcessor):
    def __init__(self, pdf_data):
        super().__init__(pdf_data)
        self.pdf_data = pdf_data

    def process_data(self):
        self.pdf_data['Quarter'] = self.pdf_data['Year'].astype(str) + '_' + self.pdf_data['Quarter']
        self.pdf_data.drop('Year', axis="columns", inplace=True)
        self.pdf_data['Revenue (in $)'] = self.pdf_data['Revenue (in $)'].str.replace(',', '').astype(float)
        return self.pdf_data.to_dict(orient='records')
    
    def get_data_type(self):
        return 'pdf'