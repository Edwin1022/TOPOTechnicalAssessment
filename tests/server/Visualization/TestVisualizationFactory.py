# tests/server/test_visualization_factory.py
import pytest
from unittest.mock import Mock, patch
import pandas as pd
from src.server.Visualization.VisualizationFactory import VisualizationFactory
from src.server.Visualization.JSONDataVisualization import JSONDataVisualization
from src.server.Visualization.CSVDataVisualization import CSVDataVisualization
from src.server.Visualization.PDFDataVisualization import PDFDataVisualization
from src.server.Visualization.PPTXDataVisualization import PPTXDataVisualization

# Fixtures
@pytest.fixture
def mock_json_data():
    return {
        "json_data": [
            {
                "Company_Id": 1,
                "Company_Name": "Comp1",
                "Employees": [{"Role": "Dev", "Cash_Money": 100, "Company_Name": "Comp1"}]
            }
        ]
    }

@pytest.fixture
def mock_csv_data():
    return pd.DataFrame({"Membership_Type": ["A"], "Revenue (in $)": [100], "Location": ["Loc1"], "Activity": ["Act1"]})

@pytest.fixture
def mock_pdf_data():
    return pd.DataFrame({"Quarter": ["Q1"], "Revenue (in $)": [100], "Memberships Sold": [50]})

@pytest.fixture
def mock_pptx_data():
    return {
        "FitPro: Annual Summary 2023": {"Key Highlights": {"Rev": 100}},
        "Quarterly Metrics": {"Q1": {"Avg Duration (Minutes)": 30, "Memberships Sold": 50, "Revenue": 100}},
        "Revenue Breakdown by Activity": {"Revenue Distribution": {"Act1": 50}}
    }

# Unit Tests
class TestVisualizationFactoryUnit:
    def test_create_json_visualization(self, mock_json_data):
        viz = VisualizationFactory.create_visualization('json', mock_json_data)
        assert isinstance(viz, JSONDataVisualization)
        assert viz.companies_df.shape[0] == 1
        assert viz.employees_df.shape[0] == 1

    def test_create_csv_visualization(self, mock_csv_data):
        viz = VisualizationFactory.create_visualization('csv', mock_csv_data)
        assert isinstance(viz, CSVDataVisualization)
        assert viz.csv_data.equals(mock_csv_data)

    def test_create_pdf_visualization(self, mock_pdf_data):
        viz = VisualizationFactory.create_visualization('pdf', mock_pdf_data)
        assert isinstance(viz, PDFDataVisualization)
        assert viz.pdf_data.equals(mock_pdf_data)

    def test_create_pptx_visualization(self, mock_pptx_data):
        viz = VisualizationFactory.create_visualization('pptx', mock_pptx_data)
        assert isinstance(viz, PPTXDataVisualization)
        assert viz.pptx_data == mock_pptx_data

    def test_create_visualization_invalid_type(self):
        with pytest.raises(ValueError) as exc_info:
            VisualizationFactory.create_visualization('xml', None)
        assert str(exc_info.value) == "Unsupported data type: xml. Supported types are 'json', 'csv', 'pdf' and 'pptx'."

    @pytest.mark.parametrize("data_type,expected_class", [
        ("JSON", JSONDataVisualization),
        ("csv", CSVDataVisualization),
        ("PDF", PDFDataVisualization),
        ("pptx", PPTXDataVisualization)
    ])
    def test_case_insensitivity(self, data_type, expected_class, mock_json_data):
        viz = VisualizationFactory.create_visualization(data_type, mock_json_data)
        assert isinstance(viz, expected_class)

# Integration Tests
class TestVisualizationFactoryIntegration:
    @patch('matplotlib.pyplot.subplots')
    def test_csv_visualization_plots(self, mock_subplots, mock_csv_data):
        mock_fig = Mock()
        mock_ax = Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        viz = VisualizationFactory.create_visualization('csv', mock_csv_data)
        fig1, fig2, fig3 = viz.plot()
        
        assert fig1 == mock_fig
        assert fig2 == mock_fig
        assert fig3 == mock_fig
        assert mock_subplots.call_count == 3

if __name__ == '__main__':
    pytest.main([__file__])