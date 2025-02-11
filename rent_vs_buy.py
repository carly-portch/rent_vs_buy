import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt

def calculate_rent_cost(monthly_rent, annual_rent_increase, years, investment_return):
    rent_costs = []
    total_rent_paid = 0
    for year in range(years):
        total_rent_paid += monthly_rent * 12
        rent_costs.append(total_rent_paid)
        monthly_rent *= (1 + annual_rent_increase / 100)
    return rent_costs

def calculate_buying_cost(home_price, down_payment, loan_term, mortgage_rate,
                          property_tax, insurance, maintenance, hoa, appreciation,
                          selling_costs, years):
    loan_amount = home_price - down_payment
    monthly_mortgage = npf.pmt(mortgage_rate / 12 / 100, loan_term * 12, -loan_amount)
    home_value = home_price
    total_costs = 0
    buy_costs = []
    
    for year in range(years):
        total_costs += (monthly_mortgage * 12 + property_tax * home_value / 100 + insurance + maintenance * home_price / 100 + hoa)
        home_value *= (1 + appreciation / 100)
        buy_costs.append(total_costs)
    
    selling_proceeds = home_value * (1 - selling_costs / 100)
    net_buying_cost = total_costs - (selling_proceeds - loan_amount)
    return buy_costs, net_buying_cost

st.title("Rent vs Buy Calculator")

st.sidebar.header("Renting Details")
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=2000)
annual_rent_increase = st.sidebar.number_input("Annual Rent Increase (%)", value=3)
investment_return = st.sidebar.number_input("Investment Return on Savings (%)", value=5)

st.sidebar.header("Buying Details")
home_price = st.sidebar.number_input("Home Price ($)", value=400000)
down_payment = st.sidebar.number_input("Down Payment ($)", value=80000)
mortgage_rate = st.sidebar.number_input("Mortgage Interest Rate (%)", value=6)
loan_term = st.sidebar.slider("Loan Term (Years)", 10, 30, 30)
property_tax = st.sidebar.number_input("Property Tax (% of Home Price)", value=1.2)
insurance = st.sidebar.number_input("Annual Home Insurance ($)", value=1200)
maintenance = st.sidebar.number_input("Annual Maintenance (% of Home Price)", value=1)
hoa = st.sidebar.number_input("Monthly HOA Fees ($)", value=0)
appreciation = st.sidebar.number_input("Annual Home Appreciation (%)", value=3)
selling_costs = st.sidebar.number_input("Selling Costs (% of Home Price)", value=6)

years = st.sidebar.slider("Years Staying in Home", 1, 30, 10)

rent_costs = calculate_rent_cost(monthly_rent, annual_rent_increase, years, investment_return)
buy_costs, net_buying_cost = calculate_buying_cost(home_price, down_payment, loan_term, mortgage_rate,
                                                   property_tax, insurance, maintenance, hoa,
                                                   appreciation, selling_costs, years)

fig, ax = plt.subplots()
ax.plot(range(1, years+1), rent_costs, label="Total Rent Cost", linestyle="--", marker="o")
ax.plot(range(1, years+1), buy_costs, label="Total Buying Cost", linestyle="-", marker="s")
ax.set_xlabel("Years")
ax.set_ylabel("Total Cost ($)")
ax.set_title("Rent vs Buy Financial Comparison")
ax.legend()
st.pyplot(fig)

if rent_costs[-1] < net_buying_cost:
    st.subheader("Renting is financially better over this period.")
else:
    st.subheader("Buying is financially better over this period.")
