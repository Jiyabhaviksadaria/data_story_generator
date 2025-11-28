import plotly.express as px
import numpy as np

class Visualizer:
    """Creates all required visualizations"""

    @staticmethod
    def create_histogram(df, column):
        return px.histogram(
            df, x=column, nbins=30,
            title=f'Distribution of {column}',
            color_discrete_sequence=['#667eea']
        )

    @staticmethod
    def create_bar_chart(df, column):
        counts = df[column].value_counts().head(10)
        return px.bar(
            x=counts.index,
            y=counts.values,
            title=f"Top {column} Categories",
            labels={'x': column, 'y': 'Count'},
            color=counts.values,
            color_continuous_scale='Viridis'
        )

    @staticmethod
    def create_scatter_plot(df, x_col, y_col):
        return px.scatter(
            df, x=x_col, y=y_col,
            title=f"{y_col} vs {x_col}",
            trendline="ols",
            color_discrete_sequence=['#667eea']
        )

    @staticmethod
    def create_correlation_heatmap(df):
        numeric_cols = df.select_dtypes(include=[np.number])
        if numeric_cols.shape[1] < 2:
            return None

        corr = numeric_cols.corr()
        return px.imshow(
            corr,
            title="Correlation Heatmap",
            color_continuous_scale='RdBu'
        )
