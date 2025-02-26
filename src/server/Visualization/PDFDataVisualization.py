from .Visualization import Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class PDFDataVisualization(Visualization):
    def __init__(self, pdf_data):
        super().__init__(pdf_data)
        self.pdf_data = pd.DataFrame(pdf_data)

    def plot(self):
        fig1 = self.plot_quarterly_revenue()
        fig2 = self.plot_quarterly_membership_sold()
        return fig1, fig2
    
    def plot_quarterly_revenue(self):
        fig, ax = plt.subplots(figsize=(13, 6))
        sns.lineplot(x='Quarter', y='Revenue (in $)', data=self.pdf_data, ax=ax)
        ax.set_title('Quarterly Revenue Over Years')
        ax.set_xlabel('Quarter')
        ax.set_ylabel('Revenue (in $)')
        return fig

    def plot_quarterly_membership_sold(self):
        fig, ax = plt.subplots(figsize=(13, 6))
        sns.lineplot(x='Quarter', y='Memberships Sold', data=self.pdf_data, ax=ax)
        ax.set_title('Quarterly Memberships Sold Over Years')
        ax.set_xlabel('Quarter')
        ax.set_ylabel('Memberships Sold')
        return fig