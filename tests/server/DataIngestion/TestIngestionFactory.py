import pytest
from unittest.mock import Mock, patch, mock_open
from src.server.DataIngestion.IngestionFactory import IngestionFactory
from src.server.DataIngestion.JSONDataIngestion import JSONDataIngestion
from src.server.DataIngestion.CSVDataIngestion import CSVDataIngestion
from src.server.DataIngestion.PPTXDataIngestion import PPTXDataIngestion
from src.server.DataIngestion.PDFDataIngestion import PDFDataIngestion

# Fixtures
@pytest.fixture
def mock_json_data():
    return '{"key": "value"}'

@pytest.fixture
def mock_csv_data():
    return "col1,col2\nval1,val2"

@pytest.fixture
def mock_pptx_data():
    return Mock()

@pytest.fixture
def mock_pdf_data():
    return Mock()

# Unit Tests
class TestIngestionFactoryUnit:
    @patch('src.server.DataIngestion.IngestionFactory.IngestionFactory._ingestion_classes', new_callable=dict)
    def test_create_ingestion_valid_types(self, mock_classes):
        mock_classes.update({
            "json": Mock(return_value="json_instance"),
            "csv": Mock(return_value="csv_instance"),
            "pdf": Mock(return_value="pdf_instance"),
            "pptx": Mock(return_value="pptx_instance")
        })

        assert IngestionFactory.create_ingestion("json") == "json_instance"
        assert IngestionFactory.create_ingestion("csv") == "csv_instance"
        assert IngestionFactory.create_ingestion("pdf") == "pdf_instance"
        assert IngestionFactory.create_ingestion("pptx") == "pptx_instance"

    def test_create_ingestion_invalid_type(self):
        with pytest.raises(ValueError) as exc_info:
            IngestionFactory.create_ingestion("xml")
        assert str(exc_info.value) == "Unsupported data type: xml"

    @patch('src.server.DataIngestion.JSONDataIngestion.json')
    def test_json_ingestion(self, mock_json, tmp_path):
        mock_json.load.return_value = {"key": "value"}
        file_path = tmp_path / "test.json"
        file_path.write_text('{"key": "value"}')
        
        ingestor = IngestionFactory.create_ingestion("json")
        assert isinstance(ingestor, JSONDataIngestion)
        
        ingestor.load_data(str(file_path))
        assert ingestor.data == {"key": "value"}
        
        processor = ingestor.create_processor()
        assert processor.__class__.__name__ == "JSONDataProcessor"
        assert processor.data == {"key": "value"}

    @patch('src.server.DataIngestion.CSVDataIngestion.pd')
    def test_csv_ingestion(self, mock_pandas, tmp_path):
        mock_df = Mock()
        mock_pandas.read_csv.return_value = mock_df
        file_path = tmp_path / "test.csv"
        file_path.write_text("col1,col2\nval1,val2")
        
        ingestor = IngestionFactory.create_ingestion("csv")
        assert isinstance(ingestor, CSVDataIngestion)
        
        ingestor.load_data(str(file_path))
        assert ingestor.data == mock_df
        
        processor = ingestor.create_processor()
        assert processor.__class__.__name__ == "CSVDataProcessor"
        assert processor.data == mock_df

    @patch('src.server.DataIngestion.PPTXDataIngestion.Presentation')
    def test_pptx_ingestion(self, mock_presentation, tmp_path):
        mock_pres = Mock()
        mock_presentation.return_value = mock_pres
        file_path = tmp_path / "test.pptx"
        file_path.touch()
        
        ingestor = IngestionFactory.create_ingestion("pptx")
        assert isinstance(ingestor, PPTXDataIngestion)
        
        ingestor.load_data(str(file_path))
        assert ingestor.data == mock_pres
        
        processor = ingestor.create_processor()
        assert processor.__class__.__name__ == "PPTXDataProcessor"
        assert processor.data == mock_pres

    @patch('src.server.DataIngestion.PDFDataIngestion.tabula')
    def test_pdf_ingestion(self, mock_tabula, tmp_path):
        mock_table = Mock()
        mock_tabula.read_pdf.return_value = [mock_table]
        file_path = tmp_path / "test.pdf"
        file_path.touch()
        
        ingestor = IngestionFactory.create_ingestion("pdf")
        assert isinstance(ingestor, PDFDataIngestion)
        
        ingestor.load_data(str(file_path))
        assert ingestor.data == mock_table
        
        processor = ingestor.create_processor()
        assert processor.__class__.__name__ == "PDFDataProcessor"
        assert processor.data == mock_table

# Integration Tests
class TestIngestionFactoryIntegration:
    @pytest.mark.parametrize("data_type, class_type", [
        ("json", JSONDataIngestion),
        ("csv", CSVDataIngestion),
        ("pdf", PDFDataIngestion),
        ("pptx", PPTXDataIngestion)
    ])
    def test_create_ingestor_type(self, data_type, class_type):
        ingestor = IngestionFactory.create_ingestion(data_type)
        assert isinstance(ingestor, class_type)
        assert hasattr(ingestor, 'load_data')
        assert hasattr(ingestor, 'create_processor')

if __name__ == '__main__':
    pytest.main([__file__])