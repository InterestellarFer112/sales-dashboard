import streamlit as st
import pandas as pd
import numpy as np

#Page Data
YEAR = 2023
cities = ["Tokyo", "Yokohama", "Osaka"]
data = pd.read_csv("store_Sales_2022-2023.csv")



#Page Title
st.set_page_config(page_title="Sales Dashboard", page_icon="⛪")
st.title("Sales Dashboard")


#data
@st.cache_data
def updatefunction(data):
    # st.dataframe(data)
    data["date_of_sale"] = pd.to_datetime(data["date_of_sale"])
    data["month"] = data["date_of_sale"].dt.month #se extrae el mes
    data["year"] = data["date_of_sale"].dt.year #se extrae el año
    
    return data


data = updatefunction(data)
st.dataframe(data)
city_renuves =(
    data.groupby(["city","year"])["sales_amount"]
    .sum()
    .unstack()
    .assign(change=lambda x:x.pct_change(axis=1)[YEAR]*1000)
    )


left_col, mid_col,_right_col = st.columns(3)

with left_col:
    st.metric(
        label=cities[0],
        value=f"${city_renuves.loc[cities[0],YEAR]:,.2f}",
        delta=f"${city_renuves.loc[cities[0],'change']:.2f}. vs Last Year"
    )
with mid_col:
    st.metric(
        label=cities[1],
        value=f"${city_renuves.loc[cities[1],YEAR]:,.2f}",
        delta=f"${city_renuves.loc[cities[1],'change']:.2f}. vs Last Year"
    )
with _right_col:
    st.metric(
        label=cities[2],
        value=f"${city_renuves.loc[cities[2],YEAR]:,.2f}",
        delta=f"${city_renuves.loc[cities[2],'change']:.2f}. vs Last Year"
    )


select_cities = st.selectbox("Select a Citie", cities)
show_previous_year = st.toggle("Show previous Year")
if show_previous_year:

    visualization_year = YEAR -1
else:
    visualization_year = YEAR

st.write(f"sales Year {visualization_year}")



tab_month, tab_category = st.tabs(["Monthly Analysis", "Category Analysis"])


with tab_month:
    st.write("filter and display Monthly Analysis")
    filtered_data = (
    data.query("city == @select_cities & year == @visualization_year")
    .groupby("month", dropna=False, as_index=False)
    .agg({"sales_amount": "sum"})
)

         
    
st.bar_chart(data=filtered_data[["month", "sales_amount"]].set_index("month"))



with tab_category:
        st.write("filter and display category Analysis")
        
        filtered_data = (
        data.query("city == @select_cities & year == @visualization_year")
        .groupby("product_category", dropna=False, as_index=False)
        .agg({"sales_amount": "sum"})
)

st.bar_chart(data=filtered_data.set_index("product_category"))



