import streamlit as st
import pandas as pd
import plotly.express as px

#page_setup
st.set_page_config(page_title= "CPI Dashboard",
page_icon=":bar_chart:", layout="wide")

#Reading the  Rwanda_CPI sheet
Rwanda_CPI = pd.read_excel("data.xlsx",
sheet_name= "Rwanda_CPI",
skiprows=3, nrows= 167)

#converting and creating MonthYear column
Rwanda_CPI["Date"] = pd.to_datetime(Rwanda_CPI["Date"])
Rwanda_CPI['MonthYear'] = Rwanda_CPI['Date'].dt.strftime('%B %Y')

#reading the Urban_Rural sheet
Rural_Urban = pd.read_excel("data.xlsx",
sheet_name= "Urban_Rural", skiprows=3)

#converting and creating new MonthYear column
Rural_Urban["Date"] = pd.to_datetime(Rural_Urban["Date"])
Rural_Urban['MonthYear'] = Rural_Urban['Date'].dt.strftime('%B %Y')

#Reading the Rwanda_Basket_cat sheet
Basket_cat = pd.read_excel("data.xlsx", sheet_name="Rwanda_Basket_cat",
skiprows=3)

#Reading Rural_Urban Basket category
Rural_Urban_Basket = pd.read_excel("data.xlsx",sheet_name="Rural_Urban_Basket_Cat",
skiprows=3)




#sidebar controls
st.sidebar.header("Customize the Visualization")
st.sidebar.subheader("Select the date and the region to review the corresponding CPI")

#selectbox for date
default_monthyear = "November 2022"
selected_date = st.sidebar.selectbox("Date",
options= Rwanda_CPI["MonthYear"], index=Rwanda_CPI["MonthYear"].eq(default_monthyear).idxmax())

#selectbox for Region
selected_region = st.sidebar.selectbox("Region",
options= Rural_Urban["Region"].unique())

#date range date_input
From_date = st.sidebar.selectbox("Select 'Start_Date':", options= Rwanda_CPI["MonthYear"],
help = "Please select the start date of which you want to visualize")

To_date = st.sidebar.selectbox("Select 'End_Date'", options=Rwanda_CPI["MonthYear"],
index = 165,
help="Please select the end date of which you want to visualize")

#selectbox for basket items
Basket = st.sidebar.selectbox("Item",
options= Basket_cat["Basket_Cat"].unique())



#Filter for Viewing Overall Rwanda_CPI based on the selected date
Filter_date1 = Rwanda_CPI.query("MonthYear == @selected_date")

if Filter_date1.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

#Filter for Viewing Overall Rwanda_CPI based on the selected date and Region
Filter_region = Rural_Urban.query("MonthYear == @selected_date & Region == @selected_region")

if Filter_region.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()
#filter for Visualizing Rwanda CPI based on the selected date range
filtered_Rwanda_CPI = Rwanda_CPI[(Rwanda_CPI["Date"] >= pd.to_datetime(From_date)) & (Rwanda_CPI["Date"] <= pd.to_datetime(To_date))]

if filtered_Rwanda_CPI.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

#filter for visualizing rural or urban cpi based chosen region and date range
filtered_rural_urban = Rural_Urban[
    (Rural_Urban["Date"] >= pd.to_datetime(From_date)) &
    (Rural_Urban["Date"] <= pd.to_datetime(To_date)) &
    (Rural_Urban["Region"] == selected_region)]

if filtered_rural_urban.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

#Filter for visualising basket item CPI based on date and Region
filtered_Rwanda_CPI_Basket = Basket_cat[
(Basket_cat["Date"] >= pd.to_datetime(From_date)) &
(Basket_cat["Date"] <= pd.to_datetime(To_date)) &
(Basket_cat["Basket_Cat"] == Basket)]

if filtered_Rwanda_CPI_Basket.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

#Filter for Visualizing basket item CPI based on selected region, item, and date range
filtered_Rural_Urban_Basket = Rural_Urban_Basket[
(Rural_Urban_Basket["Date"] >= pd.to_datetime(From_date)) &
(Rural_Urban_Basket["Date"] <= pd.to_datetime(To_date)) &
(Rural_Urban_Basket["Basket_Cat"] == Basket) &
(Rural_Urban_Basket["Region"] == selected_region)]


# Check if the dataframe is empty:
if Filter_date1.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

#Dashboard title
st.title(":bar_chart: 2022 Rwanda CPI Visualization Dashboard")
st.markdown("####")

#Viewing the Overall CPI based on the selected date
cor1, cor2 = st.columns(2)

filtered_cpi = float(Filter_date1["CPI"])

with cor1:
    st.subheader(f"Rwanda CPI on {selected_date}")
    st.write(f'<h2 style="text-align:center;">  {filtered_cpi} </h2>',
    unsafe_allow_html = True)

with cor2:
    st.subheader(f"{selected_region} CPI on {selected_date} was:")
    st.write(f'<h2 style="text-align:center;"> {round(float(Filter_region["CPI"]), 2)} </h2>',
    unsafe_allow_html = True)
st.markdown("""----""")

st.header('2022 Rwanda CPI Chart presentation')
#line chart for rwanda cpi based on the selected date range
cor3, cor4 = st.columns(2)

with cor3:
    Rwanda_CPI_linechart = px.line(filtered_Rwanda_CPI, x= "Date", y="CPI", title="Rwanda CPI Line Chart" )
    #fig.show()
    st.plotly_chart(Rwanda_CPI_linechart)
with cor4:
    #line chart for Rural_Urban CPI
    Rural_Urban_linechart = px.bar(filtered_rural_urban, x="Date", y="CPI",
    title = f"{selected_region} CPI")

    # Center the chart on the page
    st.markdown(f'<div style="text-align:center">{Rural_Urban_linechart.to_html()}</div>',
    unsafe_allow_html=True)

    st.plotly_chart(Rural_Urban_linechart)
cor5, cor6 = st.columns(2)
with cor5:
    #chart for Rwanda CPI based on selected basket item and date range
    Basket_chart = px.bar(filtered_Rwanda_CPI_Basket, x="Date", y="CPI", title = f"{Basket} from Rwanda Basket" )
    st.plotly_chart(Basket_chart)
with cor6:
#Chart for rural or urban basket item based on region,date range and selected item
    rural_urban_basket_chart = px.line(filtered_Rural_Urban_Basket, x="Date", y="CPI", title = f"{Basket} from {selected_region} CPI" )
    st.plotly_chart(rural_urban_basket_chart)


# Center the chart on the page
    st.markdown(f'<div style="text-align:center">{Rural_Urban_linechart.to_html()}</div>',
    unsafe_allow_html=True)


#
