# Data Processing and Visualization Pipeline

## Overview
This project is a data processing and visualization pipeline designed to handle multiple data formats (JSON, CSV, PDF, PPTX). The pipeline ingests data from various sources, processes it, and provides visualizations through a Streamlit dashboard. Additionally, it exposes an API using Flask to access the processed data in JSON format.

### Key Components
- **Data Ingestion**: Handles loading data from different file formats.
- **Data Processing**: Processes the ingested data into a uniform structure.
- **Visualization**: Generates visualizations for the processed data.
- **API Handler**: Provides endpoints to access the processed data.

## Setup Instructions

### Prerequisites
- Git
- Visual Studio Code
- Python 3.8 or higher
- `pip` (Python package installer)

### Installation
1. **Clone the repository**:
   Open your terminal (Git Bash is recommended)
   ```bash
   git clone https://github.com/Edwin1022/TOPOTechnicalAssessment.git
   cd TOPOTechnicalAssessment
   code .

2. **Create and activate a virtual environment**:
   - Before installing dependencies, set up a virtual environment to isolate the project’s packages.
   - Run these commands in your terminal (from the TOPOTechnicalAssessment directory):
      - On Windows (using Git Bash or Command Prompt):
        ```bash
         python -m venv venv
         source venv/Scripts/activate  # For Git Bash
         # OR
         venv\Scripts\activate  # For Command Prompt
        ```
      - On macOS/Linux:
        ```bash
         python3 -m venv venv
         source venv/bin/activate
   
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Ensure you have a `requirements.txt` file with dependencies like:
   ```text
   streamlit
   flask
   pandas
   matplotlib
   seaborn
   tabula-py
   python-pptx
   pytest
   pytest-mock

### Running the Application
1. **Run the data pipe and access the API**:
   ```bash
   python src/server/DataProcessing.py
   ```
   This processes the data and runs the Flask server.
   The API will be available at http://127.0.0.1:5000/api/data. (You are recommended to use Postman to test out the API.)

2. **Access the Streamlit dashboard**:
   ```bash
   streamlit run src/client/app.py

## Testing Instructions

1. **Execute unit tests and integration tests for DataProcessing.py**:
   ```bash
   pytest tests/server/TestDataProcessing.py -v

2. **Execute unit tests and integration tests for IngestionFactory.py**:
   ```bash
   pytest tests/server/DataIngestion/TestIngestionFactory.py -v

3. **Execute unit tests and integration tests for VisualizationFactory.py**:
   ```bash
   pytest tests/server/Visualization/TestVisualizationFactory.py -v

## Assumptions or Challenges

### Assumptions
- The datasets are located in the datasets/ directory relative to the project root.
- The data formats are consistent and follow the expected structure (e.g., JSON with nested company/employee data, CSV with specific columns).

## Challenges:
Challenges
- Handling different data formats and ensuring consistent processing across them.
- Managing dependencies and ensuring compatibility across libraries like pandas, matplotlib, and seaborn.
- Designing a flexible and extensible architecture to accommodate future data formats and processing requirements.
