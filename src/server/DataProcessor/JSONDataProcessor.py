from .DataProcessor import DataProcessor
import pandas as pd

class JSONDataProcessor(DataProcessor):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.json_data = json_data

    def process_data(self):
        companies_df = pd.json_normalize(
            self.json_data['companies'],
            meta=[
                'id', 'name', 'industry', 'revenue', 'location'
            ],
            errors='ignore'
        )

        employees_df = pd.json_normalize(
            self.json_data['companies'],
            record_path='employees',
            meta=[
            ['id'],
            ['name']
            ],
            meta_prefix='company_',
            errors='ignore'
        )

        performance_data = []
        for company in self.json_data['companies']:
            company_id = company['id']
            for quarter, data in company['performance'].items():
                performance_data.append({
                'company_id': company_id,
                'quarter': quarter,
                'revenue': data['revenue'],
                'profit_margin': data['profit_margin']
        })
        performance_df = pd.DataFrame(performance_data)

        companies_df = self.clean_companies_df(companies_df)
        employees_df = self.clean_employees_df(employees_df)
        performance_df = self.clean_performance_df(performance_df)

        return self.jsonify(companies_df, employees_df, performance_df)

    def clean_companies_df(self, companies_df):
        companies_df.drop(columns=['employees', 'performance.2023_Q1.revenue', 'performance.2023_Q1.profit_margin', 'performance.2023_Q2.revenue', 'performance.2023_Q2.profit_margin'], axis='columns', inplace=True)

        companies_df['revenue'] = companies_df['revenue'].fillna(companies_df['revenue'].median())

        companies_df = companies_df.rename(columns={
            'id': 'Company_Id',
            'name': 'Company_Name',
            'industry': 'Industry',
            'revenue': 'Revenue',
            'location': 'Location'
        })

        return companies_df

    def clean_employees_df(self, employees_df):
        employees_df['hired_date'] = pd.to_datetime(employees_df['hired_date'])
        median_date = employees_df['hired_date'].median()
        employees_df['hired_date'] = employees_df['hired_date'].fillna(median_date)

        employees_df = employees_df.rename(columns={
            'id': 'Employee_Id',
            'name': 'Employee_Name',
            'role': 'Role',
            'cashmoneh': 'Cash_Money',
            'hired_date': 'Hired_Date',
            'company_id': 'Company_Id',
            'company_name': 'Company_Name'
        })

        return employees_df

    def clean_performance_df(self, performance_df):
        performance_df['revenue (in $)'] = performance_df['revenue'].fillna(performance_df['revenue'].median())

        performance_df = performance_df[['quarter', 'revenue (in $)', 'profit_margin', 'company_id']]

        performance_df = performance_df.rename(columns={
            'quarter': 'Quarter',
            'revenue (in $)': 'Revenue (in $)',
            'profit_margin': 'Profit_Margin',
            'company_id': 'Company_Id'
        })

        return performance_df

    def jsonify(self, companies_df, employees_df, performance_df):
        companies_data = []

        for index, company_row in companies_df.iterrows():
            company_dict = company_row.to_dict()

            employees_data = employees_df[employees_df['Company_Id'] == company_dict['Company_Id']].to_dict('records')
                
            for employee in employees_data:
                del employee['Company_Id'] 
                
            company_dict['Employees'] = employees_data

            performance_data = performance_df[performance_df['Company_Id'] == company_dict['Company_Id']].to_dict('records')
            company_dict['Performance'] = performance_data

            companies_data.append(company_dict)

        final_json = {'json_data': companies_data}

        return final_json
    
    def get_data_type(self):
        return 'json'