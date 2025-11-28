import numpy as np
import pandas as pd

class DataAnalyzer:
    """Handles all data analysis operations"""

    def __init__(self, df):
        self.df = df

    def get_basic_stats(self):
        """Compute core statistics of the dataset."""
        stats = {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'numeric_columns': self.df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': self.df.select_dtypes(include=['object']).columns.tolist(),
            'missing_values': self.df.isnull().sum().sum(),
            'duplicate_rows': self.df.duplicated().sum()
        }
        return stats

    def generate_insights(self):
        """Generate automated rule-based insights for storytelling."""
        insights = []
        stats = self.get_basic_stats()

        # Insight 1: Dataset Overview
        insights.append({
            'title': '📊 Dataset Overview',
            'description': (
                f"The dataset contains **{stats['rows']:,} rows** and **{stats['columns']} columns**. "
                f"It includes **{len(stats['numeric_columns'])} numeric** and **{len(stats['categorical_columns'])} categorical features**."
            ),
            'type': 'overview'
        })

        # Insight 2: Numeric Columns Summary
        for col in stats['numeric_columns'][:3]:  # limit to first 3
            mean_val = self.df[col].mean()
            std_val = self.df[col].std()
            insights.append({
                'title': f'📈 {col} Analysis',
                'description': (
                    f"Average {col.lower()}: **{mean_val:.2f}**, Standard deviation: **{std_val:.2f}**.\n"
                    f"Range: **{self.df[col].min():.2f}** to **{self.df[col].max():.2f}**."
                ),
                'type': 'numeric',
                'column': col,
                'viz_type': 'histogram'
            })

        # Insight 3: Categorical Distribution
        if stats['categorical_columns']:
            cat = stats['categorical_columns'][0]
            counts = self.df[cat].value_counts()
            insights.append({
                'title': f'🏷️ {cat} Distribution',
                'description': (
                    f"The most frequent **{cat}** value is **'{counts.index[0]}'** "
                    f"with **{counts.iloc[0]} occurrences**.\n"
                    f"Total unique categories: **{self.df[cat].nunique()}**."
                ),
                'type': 'categorical',
                'column': cat,
                'viz_type': 'bar'
            })

        # Insight 4: Data Quality
        if stats['missing_values'] > 0:
            missing_pct = (stats['missing_values'] / (stats['rows'] * stats['columns'])) * 100
            insights.append({
                'title': '⚠️ Missing Data',
                'description': (
                    f"The dataset contains **{stats['missing_values']} missing values** "
                    f"({missing_pct:.2f}% of total).\n"
                    f"Consider cleaning or imputing missing values."
                ),
                'type': 'quality'
            })
        else:
            insights.append({
                'title': '✅ Data Quality Check',
                'description': "No missing values detected. The dataset is clean.",
                'type': 'quality'
            })

        # Insight 5: Correlation
        if len(stats['numeric_columns']) >= 2:
            corr_matrix = self.df[stats['numeric_columns']].corr()
            strong_corr = [
                (c1, c2, corr_matrix.loc[c1, c2])
                for c1 in corr_matrix.columns
                for c2 in corr_matrix.columns
                if c1 != c2 and abs(corr_matrix.loc[c1, c2]) > 0.7
            ]
            if strong_corr:
                col1, col2, corr = strong_corr[0]
                insights.append({
                    'title': '🔗 Strong Correlation Detected',
                    'description': (
                        f"**{col1}** and **{col2}** have a high correlation of **{corr:.2f}**.\n"
                        f"This means changes in one variable strongly relate to changes in the other."
                    ),
                    'type': 'correlation',
                    'viz_type': 'scatter',
                    'column_x': col1,
                    'column_y': col2
                })

        return insights
