import streamlit as st  # web development
import datetime
# from subs.data_loader import load_data, process_data_for_analysis , process_uploaded_file, convert_time , process_time_resolution_and_duplicates , display_column_statistics
# from subs.visualisation import visualize_missing_values , visualize_data_by_date_range , visualise_time_series_data
import black 

# You need to instal both Pyomo and glpk package before running the code 

from pyomo.environ import *
import numpy as np
import math
import pandas   as pd
from pandas import Series, DataFrame
from subs.data_processing import time_series_plot, plot_cumulative_distribution
from subs.optimisation_engine import opt_engine , solver_opt
from subs.initialisation import GenCo_reading , demand_reading , RES_reading , not_supplied_energy
st.set_page_config(
    page_title="Capacity Expansion Model",
    page_icon="🏭",
)
st.image("./images/header.png")

st.title("A Basic Power System Capacity Expansion Model")
st.markdown("Created by Saeed Misaghian")
st.markdown("📧 Contact me: [sam.misaqian@gmail.com](mailto:sam.misaqian@gmail.com)")
st.markdown("🔗 [GitHub](https://github.com/SaM-92)")
st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/saeed-misaghian/)")

st.markdown("📕 This model and associated data are taken from [this repos](https://github.com/Power-Systems-Optimization-Course/power-systems-optimization/blob/master/Notebooks/03-Basic-Capacity-Expansion.ipynb)")

st.markdown("### 🏭 Generators Input Data")


# Ask the user whether they want to upload a CSV file or use the editable table
input_genco = st.radio('How do you want to input the data?', ('Use Editable Table','Upload CSV File' ))

generators,FixedCost,VarCost,generators_names = GenCo_reading(input_genco)

number_of_generators = generators.shape[0]



st.markdown("### 📊 Demand Input Data")
# Ask the user whether they want to use the default values or upload their own data
input_demand = st.radio('Do you want to use the default values for year long load data or upload your own data?', ('Use Default Values', 'Upload My Own Data'))

demand , demand_column = demand_reading(input_demand)



st.markdown("### 🍃🌍☀️ Renewables Capacity Factors")

input_RES = st.radio('Do you want to use the default values for year long renewables data or upload your own data?', ('Use Default Values', 'Upload My Own Data'))

RES, RES_wind, RES_solar = RES_reading(input_RES)

st.markdown("### 💡 Penalty for non-served energy ($/MWh)")

NSECost = not_supplied_energy()




st.markdown("### ⚙️ Optimisation Engine")
if st.button('Run the Model'):
    time_series_plot(demand,'Demand')
    plot_cumulative_distribution(demand)
    
    opt_model = opt_engine(generators,FixedCost,VarCost,generators_names,demand,demand_column,RES, RES_wind, RES_solar,NSECost) 
    solver_opt(opt_model)

st.markdown("### 🤖 OpenAI ")

