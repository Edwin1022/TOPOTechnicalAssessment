from .Visualization import Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class JSONDataVisualization(Visualization):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.json_data = json_data

        companies_list = self.json_data["json_data"]

        self.companies_df = pd.json_normalize(companies_list, sep="_", 
                                        meta=["Company_Id", "Company_Name", "Industry", "Location", "Revenue"])

        employees_data = []
        for company in companies_list:
            for employee in company["Employees"]:
                employee["Company_Id"] = company["Company_Id"]
                employees_data.append(employee)

        self.employees_df = pd.DataFrame(employees_data)

    def plot(self):
        pass
    
    def plot_salary_distribution_by_company(self, companies_df, employees_df, company_filter=None):
        filtered_employees = employees_df.copy()
        
        if company_filter:
            company_ids = companies_df[companies_df['Company_Name'] == company_filter]['Company_Id'].tolist()
            filtered_employees = filtered_employees[filtered_employees['Company_Id'].isin(company_ids)]
        
        fig, ax = plt.subplots(figsize=(13, 6))

        sns.boxplot(x='Company_Name', y='Cash_Money', data=filtered_employees)
        ax.set_title('Salary Distribution by Company')
        ax.set_xlabel('Company')
        ax.set_ylabel('Salary (in $)')
        ax.tick_params(axis='x', rotation=45)

        return fig
    
    def plot_roles_by_average_salary(self, employees_df, sort_order=True, top_n=10):
        filtered_employees = employees_df.copy()
        
        filtered_employees = filtered_employees.sort_values(by='Cash_Money')

        fig, ax = plt.subplots(figsize=(13, 9))

        role_salary = filtered_employees.groupby('Role')['Cash_Money'].mean().reset_index()
        role_salary = role_salary.sort_values('Cash_Money', ascending=sort_order).head(top_n)
        
        sns.barplot(x='Cash_Money', y='Role', data=role_salary)
        ax.set_title('Top N Roles by Average Salary')
        ax.set_xlabel('Average Salary (in $)')
        ax.set_ylabel('Role')

        return fig