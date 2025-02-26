from .Visualization import Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class PPTXDataVisualization(Visualization):
    def __init__(self, pptx_data):
        super().__init__(pptx_data)
        self.pptx_data = pptx_data

    def plot(self):
        fig1 = self.plot_annual_summary()
        fig2 = self.plot_quarterly_metrics()
        fig3 = self.plot_revenue_distribution()
        return fig1, fig2, fig3
    
    def plot_annual_summary(self):
        key_highlights = self.pptx_data["FitPro: Annual Summary 2023"]["Key Highlights"]

        df = pd.DataFrame(list(key_highlights.items()), columns=["Metric", "Value"])

        fig, ax = plt.subplots(figsize=(8, 2))

        ax.axis("off")

        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc="center",
            loc="center"
        )

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)

        ax.set_title("FitPro: Annual Summary 2023 - Key Highlights", fontsize=14, pad=20)

        return fig
    
    def plot_quarterly_metrics(self):
        data = self.pptx_data["Quarterly Metrics"]
        df = pd.DataFrame(data).T.reset_index()
        df.rename(columns={"index": "Quarter"}, inplace=True)

        fig, axes = plt.subplots(3, 1, figsize=(13, 15))

        fig.subplots_adjust(hspace=0.5)

        # Plot Avg Duration (Minutes)
        sns.lineplot(x="Quarter", y="Avg Duration (Minutes)", data=df, ax=axes[0], marker="o", color="blue")
        axes[0].set_title("Average Duration (Minutes) by Quarter", fontsize=14)
        axes[0].set_ylabel("Avg Duration (Minutes)", fontsize=12)

        # Plot Memberships Sold
        sns.lineplot(x="Quarter", y="Memberships Sold", data=df, ax=axes[1], marker="o", color="green")
        axes[1].set_title("Memberships Sold by Quarter", fontsize=14)
        axes[1].set_ylabel("Memberships Sold", fontsize=12)

        # Plot Revenue
        sns.lineplot(x="Quarter", y="Revenue", data=df, ax=axes[2], marker="o", color="red")
        axes[2].set_title("Revenue by Quarter", fontsize=14)
        axes[2].set_ylabel("Revenue ($)", fontsize=12)

        return fig
    
    def plot_revenue_distribution(self):
        revenue_distribution = self.pptx_data["Revenue Breakdown by Activity"]["Revenue Distribution"]

        df = pd.DataFrame(list(revenue_distribution.items()), columns=["Activity", "Revenue Percentage"])

        fig, ax = plt.subplots(figsize=(6, 6))
        
        ax.pie(
            df["Revenue Percentage"],
            labels=df["Activity"],
            autopct="%1.1f%%",
            startangle=140,
            colors=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
        )

        ax.set_title("Revenue Breakdown by Activity", fontsize=10)

        return fig