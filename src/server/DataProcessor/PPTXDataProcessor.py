from .DataProcessor import DataProcessor
import re

class PPTXDataProcessor(DataProcessor):
    def __init__(self, pptx_data):
        super().__init__(pptx_data)
        self.pptx_data = pptx_data

    def process_data(self):
        # Collect all text
        combined_text = self.collect_all_text(self.pptx_data)
        
        # Extract basic data
        data = self.extract_basic_data(combined_text)
        
        # Extract quarterly metrics
        data["Quarterly Metrics"] = self.extract_quarterly_metrics(self.pptx_data)
        
        return data

    REGEX_PATTERNS = {
        "total_revenue": r"Total Revenue:?\s*\$?([0-9,.]+)",
        "total_memberships": r"Total Memberships Sold:?\s*([0-9,.]+)",
        "top_location": r"Top Location:?\s*(\w+)",
        "gym_revenue": r"Gym:?\s*([0-9,.]+)%?",
        "pool_revenue": r"Pool:?\s*([0-9,.]+)%?",
        "tennis_revenue": r"Tennis Court:?\s*([0-9,.]+)%?",
        "training_revenue": r"Personal Training:?\s*([0-9,.]+)%?"
    }
    
    def extract_text_value(self, text, pattern, remove_percent=False):
        match = re.search(pattern, text)
        if match:
            value = match.group(1).strip()
            if remove_percent:
                value = value.replace("%", "")
            value = value.replace(",", "")
            return float(value) if value.replace(".", "").isdigit() else value
        return None

    def collect_all_text(self, presentation):
        all_text = []
        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    all_text.append(shape.text.strip())
        return "\n".join(all_text)

    def extract_basic_data(self, combined_text):
        data = {
            "FitPro: Annual Summary 2023": {
                "Key Highlights": {
                    "Total Revenue (in $)": None,
                    "Total Memberships Sold": None,
                    "Top Location": None,
                }
            },
            "Revenue Breakdown by Activity": {
                "Revenue Distribution": {
                    "Gym": None,
                    "Pool": None,
                    "Tennis Court": None,
                    "Personal Training": None
                }
            }
        }
        
        # Extract main metrics using global patterns
        data["FitPro: Annual Summary 2023"]["Key Highlights"]["Total Revenue (in $)"] = self.extract_text_value(combined_text, self.REGEX_PATTERNS["total_revenue"])
        data["FitPro: Annual Summary 2023"]["Key Highlights"]["Total Memberships Sold"] = int(self.extract_text_value(combined_text, self.REGEX_PATTERNS["total_memberships"]))
        data["FitPro: Annual Summary 2023"]["Key Highlights"]["Top Location"] = self.extract_text_value(combined_text, self.REGEX_PATTERNS["top_location"])
        
        # Extract revenue breakdown using global patterns
        data["Revenue Breakdown by Activity"]["Revenue Distribution"]["Gym"] = self.extract_text_value(combined_text, self.REGEX_PATTERNS["gym_revenue"], True)
        data["Revenue Breakdown by Activity"]["Revenue Distribution"]["Pool"] = self.extract_text_value(combined_text, self.REGEX_PATTERNS["pool_revenue"], True)
        data["Revenue Breakdown by Activity"]["Revenue Distribution"]["Tennis Court"] = self.extract_text_value(combined_text, self.REGEX_PATTERNS["tennis_revenue"], True)
        data["Revenue Breakdown by Activity"]["Revenue Distribution"]["Personal Training"] = self.extract_text_value(combined_text, self.REGEX_PATTERNS["training_revenue"], True)
        
        return data
    
    def extract_quarterly_metrics(self, presentation):
        quarterly_metrics = {
            "Q1": {
                "Revenue": None,
                "Memberships Sold": None,
                "Avg Duration (Minutes)": None
            },
            "Q2": {
                "Revenue": None,
                "Memberships Sold": None,
                "Avg Duration (Minutes)": None
            },
            "Q3": {
                "Revenue": None,
                "Memberships Sold": None,
                "Avg Duration (Minutes)": None
            },
            "Q4": {
                "Revenue": None,
                "Memberships Sold": None,
                "Avg Duration (Minutes)": None
            }
        }
        
        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, 'table') and shape.has_table:
                    table = shape.table
                    
                    # Check if this table has "Quarter" in the first column header
                    if table.cell(0, 0).text.strip() == "Quarter":
                        # Iterate through rows (skipping header)
                        for row_idx in range(1, len(table.rows)):
                            quarter = table.cell(row_idx, 0).text.strip()
                            
                            if quarter in quarterly_metrics:
                                # Revenue is in column 1
                                revenue = table.cell(row_idx, 1).text.strip().replace(",", "")
                                
                                # Memberships sold is in column 2
                                memberships = table.cell(row_idx, 2).text.strip()
                                
                                # Average duration is in column 3
                                avg_duration = table.cell(row_idx, 3).text.strip()
                                
                                # Update the data dictionary
                                quarterly_metrics[quarter]["Revenue"] = float(revenue)
                                quarterly_metrics[quarter]["Memberships Sold"] = int(memberships)
                                quarterly_metrics[quarter]["Avg Duration (Minutes)"] = int(avg_duration)
        
        return quarterly_metrics
    
    def get_data_type(self):
        return 'pptx'