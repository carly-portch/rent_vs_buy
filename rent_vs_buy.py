import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_renting_cost(rent, rent_increase, years):
    costs = []
    total_cost = 0
    for year in range(1, years + 1):
        total_cost += rent * 12
        costs.append(total_cost)
        rent *= (1 + rent_increase / 100)  # Increase rent annually
    return costs

def calculate_buying_cost(home_price, down_payment, loan_term, mortgage_rate, property_tax, maintenance, appreciation, years):
    loan_amount = home_price - down_payment
    monthly_mortgage = np.pmt(mortgage_rate / 12 / 100, loan_term * 12, -loan_amount)
    costs = []
    total_cost = 0
    home_value = home_price
    
    for year in range(1, years + 1):
        total_cost += (monthly_mortgage * 12) + (property_tax * home_value) + (maintenance * home_value)
        costs.append(total_cost)
        home_value *= (1 + appreciation / 100)
    
    return costs

st.title("Rent vs Buy Calculator")

st.sidebar.header("Renting Details")
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=2000, step=100)
rent_increase = st.sidebar.slider("Annual Rent Increase (%)", 0.0, 10.0, 2.0)

st.sidebar.header("Buying Details")
home_price = st.sidebar.number_input("Home Price ($)", value=300000, step=10000)
down_payment = st.sidebar.number_input("Down Payment ($)", value=60000, step=1000)
loan_term = st.sidebar.slider("Loan Term (Years)", 10, 30, 30)
mortgage_rate = st.sidebar.slider("Mortgage Interest Rate (%)", 1.0, 10.0, 4.0)
property_tax = st.sidebar.slider("Annual Property Tax Rate (%)", 0.0, 3.0, 1.0) / 100
maintenance = st.sidebar.slider("Annual Maintenance Cost (%)", 0.0, 5.0, 1.0) / 100
appreciation = st.sidebar.slider("Annual Home Appreciation (%)", 0.0, 5.0, 3.0)

years = st.sidebar.slider("Comparison Duration (Years)", 1, 50, 30)

rent_costs = calculate_renting_cost(monthly_rent, rent_increase, years)
buy_costs = calculate_buying_cost(home_price, down_payment, loan_term, mortgage_rate, property_tax, maintenance, appreciation, years)

years_range = list(range(1, years + 1))

crossover_year = next((year for year in range(years) if buy_costs[year] < rent_costs[year]), None)

fig, ax = plt.subplots()
ax.plot(years_range, rent_costs, label="Total Renting Cost", linestyle="--", color="red")
ax.plot(years_range, buy_costs, label="Total Buying Cost", linestyle="-", color="blue")
if crossover_year:
    ax.axvline(x=crossover_year, linestyle="dotted", color="green", label=f"Crossover: Year {crossover_year}")
ax.set_xlabel("Years")
ax.set_ylabel("Total Cost ($)")
ax.set_title("Rent vs Buy Financial Comparison")
ax.legend()
st.pyplot(fig)

if crossover_year:
    st.subheader(f"Based on your inputs, buying becomes more cost-effective than renting after {crossover_year} years.")
else:
    st.subheader("Based on your inputs, renting remains more cost-effective over the entire period.")

st.markdown("""
**Disclaimer:** This analysis is based on assumptions about rent increases, property appreciation, and mortgage costs. Actual costs may vary. Consider additional factors such as personal circumstances, market conditions, and opportunity costs before making a decision.
""")
