import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Climate & Health Dashboard", layout="wide")

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'processed')
RESULTS_DIR = os.path.join(PROJECT_DIR, 'results')

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'integrated_data_1990_2019.csv'))
    corr_df = pd.read_csv(os.path.join(RESULTS_DIR, 'climate_mortality_correlations.csv'))
    return df, corr_df

df, corr_df = load_data()

st.title("🌍 Climate Impact on Public Health (1990-2019)")
st.markdown("Analysis of climate variables and mortality rates across 49 countries")

st.sidebar.header("Filters")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df['Country/Territory'].unique()),
    default=['Germany', 'United States', 'China', 'Brazil']
)

year_range = st.sidebar.slider(
    "Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(1990, 2019)
)

filtered_df = df[
    (df['Country/Territory'].isin(selected_countries)) &
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1])
]

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Climate Trends", "Mortality Analysis", "Correlations"])

with tab1:
    st.header("Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Countries", df['Country/Territory'].nunique())
    with col2:
        st.metric("Years", f"{df['Year'].min()}-{df['Year'].max()}")
    with col3:
        st.metric("Total Records", len(df))
    with col4:
        st.metric("Variables", len(df.columns))
    
    st.subheader("Sample Data")
    st.dataframe(filtered_df.head(10))

with tab2:
    st.header("Climate Trends")
    
    climate_var = st.selectbox(
        "Select Climate Variable",
        ['Temperature_C', 'Precipitation_mm', 'Surface_Pressure_Pa', 'Wind_Speed_ms']
    )
    
    fig = px.line(
        filtered_df,
        x='Year',
        y=climate_var,
        color='Country/Territory',
        title=f'{climate_var} Evolution Over Time'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Temperature Distribution by Country")
    fig2 = px.box(
        filtered_df,
        x='Country/Territory',
        y='Temperature_C',
        title='Temperature Distribution'
    )
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Mortality Analysis")
    
    rate_cols = [col for col in df.columns if col.endswith('_Rate_per_100k')]
    
    selected_cause = st.selectbox(
        "Select Cause of Death",
        [col.replace('_Rate_per_100k', '') for col in rate_cols]
    )
    
    rate_col = f'{selected_cause}_Rate_per_100k'
    
    fig = px.line(
        filtered_df,
        x='Year',
        y=rate_col,
        color='Country/Territory',
        title=f'{selected_cause} - Death Rate per 100k'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(f"Average {selected_cause} Rate by Country")
    avg_by_country = filtered_df.groupby('Country/Territory')[rate_col].mean().sort_values(ascending=False)
    
    fig2 = px.bar(
        x=avg_by_country.index,
        y=avg_by_country.values,
        labels={'x': 'Country', 'y': 'Average Rate per 100k'},
        title=f'Average {selected_cause} Rate by Country'
    )
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.header("Climate-Mortality Correlations")
    
    top_n = st.slider("Number of top correlations to display", 10, 50, 20)
    
    corr_type = st.radio("Correlation Type", ["Strongest (Absolute)", "Positive", "Negative"])
    
    if corr_type == "Strongest (Absolute)":
        top_corr = corr_df.nlargest(top_n, 'Correlation', keep='all')
    elif corr_type == "Positive":
        top_corr = corr_df.nlargest(top_n, 'Correlation')
    else:
        top_corr = corr_df.nsmallest(top_n, 'Correlation')
    
    fig = px.bar(
        top_corr,
        x='Correlation',
        y=[f"{row['Cause'][:25]} vs {row['Climate_Variable']}" for _, row in top_corr.iterrows()],
        orientation='h',
        title=f'Top {top_n} Climate-Mortality Correlations ({corr_type})',
        color='Correlation',
        color_continuous_scale='RdBu_r'
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Correlation Heatmap - Top Causes")
    top_causes = corr_df.groupby('Cause')['Correlation'].apply(lambda x: x.abs().max()).nlargest(10).index
    
    heatmap_data = corr_df[corr_df['Cause'].isin(top_causes)].pivot(
        index='Cause',
        columns='Climate_Variable',
        values='Correlation'
    )
    
    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Climate Variable", y="Cause of Death", color="Correlation"),
        color_continuous_scale='RdBu_r',
        aspect="auto"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard created with Streamlit")