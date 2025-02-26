from flask import Flask, jsonify

class APIHandler:
    def __init__(self, json_data, csv_data, pdf_data, pptx_data):
        self.json_data = json_data
        self.csv_data = csv_data
        self.pdf_data = pdf_data
        self.pptx_data = pptx_data
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/api/data', methods=['GET'])
        def get_data():
            return jsonify({"json_data": self.json_data['json_data'], "csv_data": self.csv_data, "pdf_data": self.pdf_data, "pptx_data": self.pptx_data})
        
        @self.app.route('/api/data/<file_type>', methods=['GET'])
        def get_data_by_type(file_type):
            if file_type == 'json':
                return self.json_data
            elif file_type == 'csv':
                return jsonify({"csv_data": self.csv_data})
            elif file_type == 'pdf':
                return jsonify({"pdf_data": self.pdf_data})
            elif file_type == 'pptx':
                return jsonify({"pptx_data": self.pptx_data})
            else:
                return jsonify({"error": "Invalid file type"}), 404

    def run(self):
        """Run the Flask app."""
        self.app.run(debug=True)