import pytest
import os
from unittest.mock import Mock, patch

from src.server.DataProcessing import DataProcessing

@pytest.fixture
def mock_data_source():
    return Mock(file_path="test/path/data.json", type="json")

@pytest.fixture
def mock_ingestor():
    mock = Mock()
    mock.load_data.return_value = None
    mock.create_processor.return_value = Mock(
        process_data=lambda: {"test": "data"},
        get_data_type=lambda: "json"
    )
    return mock

@pytest.fixture
def mock_api_handler():
    return Mock(run=lambda: None)

@pytest.fixture
def data_pipeline(tmp_path):
    datasets_dir = tmp_path / "datasets"
    datasets_dir.mkdir()
    
    (datasets_dir / "dataset1.json").touch()
    (datasets_dir / "dataset2.csv").touch()
    (datasets_dir / "dataset3.pdf").touch()
    (datasets_dir / "dataset4.pptx").touch()
    
    return DataProcessing()

# Unit Tests
class TestDataProcessing:
    def test_init(self, tmp_path):
        pipeline = DataProcessing()
        assert len(pipeline.data_sources) == 4
        assert pipeline.processed_data == {}
        assert pipeline.ingestors == []

    @patch('src.server.DataProcessing.IngestionFactory')
    def test_ingest_data(self, mock_factory, data_pipeline, mock_ingestor):
        mock_factory.create_ingestion.return_value = mock_ingestor
        data_pipeline.ingest_data()
        
        assert len(data_pipeline.ingestors) == 4
        assert mock_ingestor.load_data.called
        assert mock_factory.create_ingestion.call_count == 4

    def test_process_data(self, data_pipeline, mock_ingestor):
        data_pipeline.ingestors = [mock_ingestor]
        data_pipeline.process_data()
        
        assert "json" in data_pipeline.processed_data
        assert data_pipeline.processed_data["json"] == {"test": "data"}
        assert mock_ingestor.create_processor.called

    @patch('src.server.DataProcessing.APIHandler')
    def test_handle_api(self, mock_api_handler_class, data_pipeline):
        mock_handler_instance = mock_api_handler_class.return_value
        data_pipeline.processed_data = {
            "json": {"data": "json"},
            "csv": {"data": "csv"},
            "pdf": {"data": "pdf"},
            "pptx": {"data": "pptx"}
        }
        
        data_pipeline.handle_api()
        
        mock_api_handler_class.assert_called_once_with(
            {"data": "json"},
            {"data": "csv"},
            {"data": "pdf"},
            {"data": "pptx"}
        )
        assert mock_handler_instance.run.called

# Integration Tests
class TestDataProcessingIntegration:
    @patch('src.server.DataProcessing.IngestionFactory')
    @patch('src.server.DataProcessing.APIHandler')
    def test_run_pipeline(self, mock_api_handler_class, mock_factory, data_pipeline):
        mock_ingestor = Mock()
        mock_processor = Mock()
        mock_processor.process_data.return_value = {"test": "data"}
        mock_processor.get_data_type.return_value = "json"

        mock_ingestor.create_processor.return_value = mock_processor
        mock_factory.create_ingestion.return_value = mock_ingestor
        
        mock_handler = Mock()
        mock_handler.run.return_value = None
        mock_api_handler_class.return_value = mock_handler

        data_pipeline.run_pipeline()

        assert len(data_pipeline.ingestors) == 4
        assert "json" in data_pipeline.processed_data
        assert mock_ingestor.load_data.call_count == 4
        assert mock_ingestor.create_processor.call_count == 4
        assert mock_processor.process_data.call_count == 4
        assert mock_handler.run.called

    def test_data_source_paths(self, data_pipeline):
        for source in data_pipeline.data_sources:
            assert os.path.exists(source.file_path)
            assert source.type in ["json", "csv", "pdf", "pptx"]

if __name__ == '__main__':
    pytest.main([__file__])