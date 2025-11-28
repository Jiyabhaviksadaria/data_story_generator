
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Data Story Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""

    .stApp {
        background: linear-gradient(to bottom right, #f0f4ff, #faf5ff);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }

""", unsafe_allow_html=True)

class DataAnalyzer:
    """Handles all data analysis operations"""
    
    def __init__(self, df):
        self.df = df
        
    def get_basic_stats(self):
        """Get basic statistical information"""
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
        """Generate automated insights from the data"""
        insights = []
        stats = self.get_basic_stats()
        
        # Insight 1: Dataset overview
        insights.append({
            'title': '📊 Dataset Overview',
            'description': f"This dataset contains {stats['rows']:,} rows and {stats['columns']} columns. "
                          f"It has {len(stats['numeric_columns'])} numeric and {len(stats['categorical_columns'])} categorical features.",
            'type': 'overview'
        })
        
        # Insight 2: Numeric columns analysis
        if stats['numeric_columns']:
            for col in stats['numeric_columns'][:3]:
                if col in self.df.columns:
                    mean_val = self.df[col].mean()
                    std_val = self.df[col].std()
                    insights.append({
                        'title': f'📈 {col} Analysis',
                        'description': f"The average {col.lower()} is {mean_val:.2f} with a standard deviation of {std_val:.2f}. "
                                      f"Values range from {self.df[col].min():.2f} to {self.df[col].max():.2f}.",
                        'type': 'numeric',
                        'column': col,
                        'viz_type': 'histogram'
                    })
        
        # Insight 3: Categorical analysis
        if stats['categorical_columns']:
            cat_col = stats['categorical_columns'][0]
            top_categories = self.df[cat_col].value_counts().head(5)
            insights.append({
                'title': f'🏷️ {cat_col} Distribution',
                'description': f"The most common {cat_col.lower()} is '{top_categories.index[0]}' with {top_categories.iloc[0]} occurrences. "
                              f"There are {self.df[cat_col].nunique()} unique categories in total.",
                'type': 'categorical',
                'column': cat_col,
                'viz_type': 'bar'
            })
        
        # Insight 4: Data quality
        if stats['missing_values'] > 0:
            missing_pct = (stats['missing_values'] / (stats['rows'] * stats['columns'])) * 100
            insights.append({
                'title': '⚠️ Data Quality',
                'description': f"Found {stats['missing_values']} missing values ({missing_pct:.1f}% of total data). "
                              f"Consider handling these before further analysis.",
                'type': 'quality'
            })
        else:
            insights.append({
                'title': '✅ Data Quality',
                'description': "Great news! No missing values detected in the dataset. The data is complete and ready for analysis.",
                'type': 'quality'
            })
        
        # Insight 5: Correlations
        if len(stats['numeric_columns']) >= 2:
            corr_matrix = self.df[stats['numeric_columns']].corr()
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))
            
            if high_corr:
                col1, col2, corr_val = high_corr[0]
                insights.append({
                    'title': '🔗 Strong Correlation Found',
                    'description': f"{col1} and {col2} show a strong correlation of {corr_val:.2f}. "
                                  f"This suggests these variables are related and move together.",
                    'type': 'correlation',
                    'viz_type': 'scatter'
                })
        
        return insights

class Visualizer:
    """Handles all visualization creation"""
    
    @staticmethod
    def create_histogram(df, column):
        fig = px.histogram(df, x=column, nbins=30,
                          title=f'Distribution of {column}',
                          color_discrete_sequence=['#667eea'])
        fig.update_layout(showlegend=False)
        return fig
    
    @staticmethod
    def create_bar_chart(df, column):
        value_counts = df[column].value_counts().head(10)
        fig = px.bar(x=value_counts.index, y=value_counts.values,
                    title=f'Top 10 {column} Categories',
                    labels={'x': column, 'y': 'Count'},
                    color=value_counts.values,
                    color_continuous_scale='Viridis')
        return fig
    
    @staticmethod
    def create_scatter_plot(df, x_col, y_col):
        fig = px.scatter(df, x=x_col, y=y_col,
                        title=f'{y_col} vs {x_col}',
                        trendline="ols",
                        color_discrete_sequence=['#667eea'])
        return fig
    
    @staticmethod
    def create_correlation_heatmap(df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr,
                           title='Correlation Heatmap',
                           color_continuous_scale='RdBu',
                           aspect='auto')
            return fig
        return None

def main():
    # Header
    st.title("📊 Interactive Data Story Generator")
    st.markdown("Upload your dataset and get AI-powered insights with beautiful visualizations")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("---")
        st.header("📋 Instructions")
        st.markdown("""
        1. Upload your CSV file
        2. Explore automated insights
        3. View interactive visualizations
        4. Download the complete report
        """)
    
    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Read data
            df = pd.read_csv(uploaded_file)
            
            # Initialize
            analyzer = DataAnalyzer(df)
            visualizer = Visualizer()
            stats = analyzer.get_basic_stats()
            
            # Metrics
            st.markdown("### 📈 Dataset Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Rows", f"{stats['rows']:,}")
            with col2:
                st.metric("Columns", stats['columns'])
            with col3:
                st.metric("Numeric Features", len(stats['numeric_columns']))
            with col4:
                st.metric("Missing Values", stats['missing_values'])
            
            st.markdown("---")
            
            # Preview
            with st.expander("👀 Preview Data"):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Generate insights
            insights = analyzer.generate_insights()
            
            # Display story
            st.markdown("### 📖 Data Story")
            st.markdown(f"## Analysis Report - {datetime.now().strftime('%B %d, %Y')}")
            
            st.markdown("---")
            st.markdown("### 🔍 Key Insights")
            
            # Display insights
            for idx, insight in enumerate(insights, 1):
                st.markdown(f"#### {idx}. {insight['title']}")
                st.markdown(insight['description'])
                
                # Visualizations
                if insight['type'] == 'numeric' and 'column' in insight:
                    fig = visualizer.create_histogram(df, insight['column'])
                    st.plotly_chart(fig, use_container_width=True)
                
                elif insight['type'] == 'categorical' and 'column' in insight:
                    fig = visualizer.create_bar_chart(df, insight['column'])
                    st.plotly_chart(fig, use_container_width=True)
                
                elif insight['type'] == 'correlation':
                    fig = visualizer.create_correlation_heatmap(df)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
            
            # Additional visualizations
            st.markdown("### 📊 Custom Visualization")
            if len(stats['numeric_columns']) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X axis", stats['numeric_columns'])
                with col2:
                    y_col = st.selectbox("Y axis", stats['numeric_columns'])
                
                if x_col != y_col:
                    fig = visualizer.create_scatter_plot(df, x_col, y_col)
                    st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    else:
        st.markdown("""
        ### 🚀 Get Started
        
        Upload your CSV file to generate:
        - 📊 Automated exploratory data analysis
        - 🔍 AI-powered insights
        - 📈 Interactive visualizations
        - 📝 Data story
        """)

if __name__ == "__main__":
    main()