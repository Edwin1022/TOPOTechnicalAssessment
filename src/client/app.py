import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(root_dir))

from src.server.DataPipeline import DataPipeline
from src.server.Visualization.VisualizationFactory import VisualizationFactory
import streamlit as st
import matplotlib.pyplot as plt

class DataVisualizationDashboard:
    def __init__(self):
        st.set_page_config(
            page_title="Data Visualization",
            page_icon="📊",
            layout="wide"
        )
        self.pipeline = self.initialize_pipeline()
        self.viz_options = ["JSON Data Visualizations", "CSV Data Visualizations", "PDF Data Visualizations", "PPTX Data Visualizations"]

    @st.cache_resource
    def initialize_pipeline(_self):
        pipeline = DataPipeline()
        pipeline.ingest_data()
        pipeline.process_data()
        return pipeline

    def render_sidebar(self):
        st.sidebar.header("Controls")
        self.viz_selection = st.sidebar.selectbox("Select Visualization", self.viz_options)
        st.sidebar.markdown("---")
        st.sidebar.subheader("About")
        st.sidebar.info(
            "This dashboard displays visualizations from the data pipeline. "
            "Select different visualization options from the sidebar."
        )
    
    def render_json_visualizations(self):
        json_data = self.pipeline.processed_data.get('json')
        visualization = VisualizationFactory.create_visualization('json', json_data)

        st.header("JSON Data Visualizations")

        plt.figure(figsize=(10, 6))
        fig1, fig2 = visualization.plot()

        st.pyplot(fig1)
        st.pyplot(fig2)

    def render_csv_visualizations(self):
        csv_data = self.pipeline.processed_data.get('csv')
        visualization = VisualizationFactory.create_visualization('csv', csv_data)

        st.header("CSV Data Visualizations")
        
        plt.figure(figsize=(10, 6))
        fig1, fig2, fig3 = visualization.plot()
        
        st.pyplot(fig1)
        st.pyplot(fig2)
        st.pyplot(fig3)

    def render_pdf_visualizations(self):
        pdf_data = self.pipeline.processed_data.get('pdf')
        visualization = VisualizationFactory.create_visualization('pdf', pdf_data)

        st.header("PDF Data Visualizations")
        
        plt.figure(figsize=(10, 6))
        fig1, fig2 = visualization.plot()
        
        st.pyplot(fig1)
        st.pyplot(fig2)
    
    def render_pptx_visualizations(self):
        pptx_data = self.pipeline.processed_data.get('pptx')
        visualization = VisualizationFactory.create_visualization('pptx', pptx_data)

        st.header("PPTX Data Visualizations")
        
        plt.figure(figsize=(10, 6))
        fig1, fig2, fig3 = visualization.plot()
        
        st.pyplot(fig1)
        st.pyplot(fig2)
        st.pyplot(fig3)

    def render_dashboard(self):
        st.title("Data Visualization Dashboard 📊")

        with st.spinner("Loading data pipeline..."):
            self.pipeline = self.initialize_pipeline()

        self.render_sidebar()

        if 'json' in self.pipeline.processed_data and 'csv' in self.pipeline.processed_data and 'pdf' in self.pipeline.processed_data and 'pptx' in self.pipeline.processed_data:
            if self.viz_selection == "JSON Data Visualizations":
                self.render_json_visualizations()
            elif self.viz_selection == "CSV Data Visualizations":
                self.render_csv_visualizations()
            elif self.viz_selection == "PDF Data Visualizations":
                self.render_pdf_visualizations()
            elif self.viz_selection == "PPTX Data Visualizations":
                self.render_pptx_visualizations()
        else:
            st.warning("Required data not available. Please check if the data pipeline has processed 'json', 'csv', 'pdf' and 'pptx' data.")

if __name__ == "__main__":
    dashboard = DataVisualizationDashboard()
    dashboard.render_dashboard()