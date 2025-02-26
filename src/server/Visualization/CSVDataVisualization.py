from .Visualization import Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class CSVDataVisualization(Visualization):
    def __init__(self, csv_data):
        super().__init__(csv_data)
        self.csv_data = pd.DataFrame(csv_data)

    def plot(self):
        fig1 = self.plot_average_revenue_by_membership_type()
        fig2 = self.plot_total_revenue_by_location()
        fig3 = self.plot_total_revenue_by_activity()
        return fig1, fig2, fig3
    
    def plot_average_revenue_by_membership_type(self):
        revenue_by_membership_type = self.csv_data.groupby("Membership_Type")["Revenue (in $)"].mean().reset_index()

        fig, ax = plt.subplots(figsize=(13, 6))
        sns.barplot(x='Membership_Type', y='Revenue (in $)', data=revenue_by_membership_type, ci=None)
        ax.set_title('Average Revenue by Membership Type')
        ax.set_xlabel('Membership Type')
        ax.set_ylabel('Average Revenue (in $)')
        return fig
    
    def plot_total_revenue_by_location(self):
        revenue_by_location = self.csv_data.groupby("Location")["Revenue (in $)"].sum().reset_index()

        fig, ax = plt.subplots(figsize=(13, 6))
        sns.barplot(x='Location', y='Revenue (in $)', data=revenue_by_location, ci=None)
        ax.set_title('Total Revenue by Location')
        ax.set_xlabel('Location')
        ax.set_ylabel('Total Revenue (in $)')
        return fig
    
    def plot_total_revenue_by_activity(self):
        revenue_by_activity = self.csv_data.groupby("Activity")["Revenue (in $)"].sum().reset_index()

        fig, ax = plt.subplots(figsize=(13, 6))
        sns.barplot(x='Activity', y='Revenue (in $)', data=revenue_by_activity, ci=None)
        ax.set_title('Total Revenue by Activity')
        ax.set_xlabel('Activity')
        ax.set_ylabel('Total Revenue (in $)')
        return fig