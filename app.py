import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import random


st.set_page_config(
    page_title="BMW Sales Dashboard (2010-2024)",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stPlotlyChart {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    
    try:
        df = pd.read_csv("BMW sales data (2010-2024) (1).csv")
    except FileNotFoundError:
        st.error("CSV file not found. Please ensure 'BMW sales data (2010-2024) (1).csv' is in the same directory.")
        st.stop()
    

    df = df.dropna(how='all')
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    

    if "Country" not in df.columns:
        countries = [
            "United States", "Germany", "United Kingdom", "India",
            "China", "Japan", "France", "Canada", "Australia", "Brazil"
        ]
        random.seed(42) 
        df["Country"] = [random.choice(countries) for _ in range(len(df))]
    
    return df

df = load_data()


st.title("🚗 BMW Sales Dashboard (2010-2024)")
st.markdown("---")


st.sidebar.header("🔍 Filters")


year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)


countries = ["All"] + sorted(df["Country"].unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", countries)


if "Model" in df.columns:
    models = ["All"] + sorted(df["Model"].unique().tolist())
    selected_model = st.sidebar.selectbox("Select Model", models)
else:
    selected_model = "All"


filtered_df = df[
    (df["Year"] >= year_range[0]) & 
    (df["Year"] <= year_range[1])
]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

if selected_model != "All" and "Model" in df.columns:
    filtered_df = filtered_df[filtered_df["Model"] == selected_model]


st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df["Sales_Volume"].sum()
    st.metric("Total Sales Volume", f"{total_sales:,.0f}")

with col2:
    if "Price_USD" in filtered_df.columns:
        avg_price = filtered_df["Price_USD"].mean()
        st.metric("Average Price (USD)", f"${avg_price:,.0f}")
    else:
        st.metric("Average Price (USD)", "N/A")

with col3:
    if "Model" in filtered_df.columns:
        total_models = filtered_df["Model"].nunique()
        st.metric("Total Models", total_models)
    else:
        st.metric("Total Models", "N/A")

with col4:
    total_countries = filtered_df["Country"].nunique()
    st.metric("Countries", total_countries)

st.markdown("---")


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Sales Trends", 
    "🏆 Top Models", 
    "🌍 Geographic Analysis", 
    "🔍 Correlations",
    "📋 Data Explorer"
])


with tab1:
    st.subheader("BMW Global Sales Over Time")
    
    sales_by_year = filtered_df.groupby("Year")["Sales_Volume"].sum().reset_index()
    fig1 = px.line(
        sales_by_year,
        x="Year",
        y="Sales_Volume",
        title="Sales Volume Trend",
        markers=True,
        color_discrete_sequence=["#1f77b4"]
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)
    
  
    if "Price_USD" in filtered_df.columns:
        st.subheader("Average Price Trend by Country")
        avg_price_country = filtered_df.groupby(["Year", "Country"])["Price_USD"].mean().reset_index()
        fig2 = px.line(
            avg_price_country,
            x="Year",
            y="Price_USD",
            color="Country",
            title="Average BMW Price Trend"
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)


with tab2:
    if "Model" in filtered_df.columns:
        st.subheader("Top 10 Best-Selling BMW Models")
        
        model_sales = filtered_df.groupby("Model")["Sales_Volume"].sum().reset_index()
        model_sales = model_sales.sort_values(by="Sales_Volume", ascending=False).head(10)
        
        fig3 = px.bar(
            model_sales,
            x="Model",
            y="Sales_Volume",
            title="Top 10 Models by Sales Volume",
            color="Sales_Volume",
            color_continuous_scale="Blues"
        )
        fig3.update_layout(height=500)
        st.plotly_chart(fig3, use_container_width=True)
        

        col1, col2 = st.columns(2)
        
        with col1:
            if "Fuel_Type" in filtered_df.columns:
                st.subheader("Sales by Fuel Type")
                fuel_sales = filtered_df.groupby("Fuel_Type")["Sales_Volume"].sum().reset_index()
                fig4 = px.pie(
                    fuel_sales,
                    names="Fuel_Type",
                    values="Sales_Volume",
                    title="Sales Distribution by Fuel Type"
                )
                st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            if "Transmission" in filtered_df.columns:
                st.subheader("Sales by Transmission")
                trans_sales = filtered_df.groupby("Transmission")["Sales_Volume"].sum().reset_index()
                fig5 = px.pie(
                    trans_sales,
                    names="Transmission",
                    values="Sales_Volume",
                    title="Sales Distribution by Transmission"
                )
                st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Model information not available in the dataset.")


with tab3:
    st.subheader("BMW Sales Distribution by Country")
    

    country_sales = filtered_df.groupby("Country", as_index=False)["Sales_Volume"].sum()
    
    def get_iso(country):
        try:
            return pycountry.countries.lookup(country).alpha_3
        except:
            return None
    
    country_sales["iso_alpha"] = country_sales["Country"].apply(get_iso)
    country_sales = country_sales.dropna(subset=["iso_alpha"])
    

    fig6 = px.choropleth(
        country_sales,
        locations="iso_alpha",
        color="Sales_Volume",
        hover_name="Country",
        color_continuous_scale="Blues",
        title="Global Sales Distribution"
    )
    fig6.update_layout(height=500)
    st.plotly_chart(fig6, use_container_width=True)
    

    st.subheader("Market Share by Country")
    fig7 = px.pie(
        country_sales,
        names="Country",
        values="Sales_Volume",
        title="BMW Market Share by Country"
    )
    fig7.update_layout(height=500)
    st.plotly_chart(fig7, use_container_width=True)


with tab4:
    st.subheader("Correlation Matrix of Numeric Features")
    
    numeric_cols = filtered_df.select_dtypes(include=["int64", "float64"]).corr()
    fig8 = px.imshow(
        numeric_cols,
        text_auto=True,
        color_continuous_scale="Blues",
        title="Feature Correlations"
    )
    fig8.update_layout(height=600)
    st.plotly_chart(fig8, use_container_width=True)
    

    col1, col2 = st.columns(2)
    
    with col1:
        if "Price_USD" in filtered_df.columns:
            st.subheader("Price vs Sales Volume")
            fig9 = px.scatter(
                filtered_df.sample(min(1000, len(filtered_df))),
                x="Price_USD",
                y="Sales_Volume",
                color="Model" if "Model" in filtered_df.columns else None,
                title="Price vs Sales Volume"
            )
            st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        if "Engine_Size_L" in filtered_df.columns and "Price_USD" in filtered_df.columns:
            st.subheader("Engine Size vs Price")
            fig10 = px.scatter(
                filtered_df.sample(min(1000, len(filtered_df))), 
                x="Engine_Size_L",
                y="Price_USD",
                color="Fuel_Type" if "Fuel_Type" in filtered_df.columns else None,
                title="Engine Size vs Price"
            )
            st.plotly_chart(fig10, use_container_width=True)

with tab5:
    st.subheader("Explore the Dataset")
    
 
    st.write("**Summary Statistics:**")
    st.dataframe(filtered_df.describe(), use_container_width=True)
    
    st.write("**Raw Data:**")
    st.dataframe(filtered_df, use_container_width=True)
    

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='bmw_sales_filtered.csv',
        mime='text/csv',
    )


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>BMW Sales Dashboard | Data Analysis | 2010-2024</p>
    </div>
    """,
    unsafe_allow_html=True
)
