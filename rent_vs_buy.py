import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title of the app
st.title("Rent vs Buy Calculator")

# Input fields for rent vs buy calculations
rent_yearly = st.number_input("Annual Rent ($)", value=12000)
buy_home_price = st.number_input("Home Price ($)", value=300000)
down_payment = st.number_input("Down Payment ($)", value=60000)
mortgage_rate = st.number_input("Mortgage Rate (%)", value=4) / 100
loan_term_years = st.number_input("Mortgage Term (years)", value=30)
property_tax_rate = st.number_input("Property Tax Rate (%)", value=1) / 100
insurance_rate = st.number_input("Home Insurance Rate (%)", value=0.2) / 100
maintenance_rate = st.number_input("Maintenance Rate (%)", value=1) / 100

# Calculate the monthly mortgage payment
loan_amount = buy_home_price - down_payment
monthly_rate = mortgage_rate / 12
loan_term_months = loan_term_years * 12
monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -loan_term_months)

# Cumulative costs over time (30 years)
years = np.arange(1, 31)  # 30 years
rent_cost = rent_yearly * years  # cumulative rent costs
buy_cost = np.zeros_like(years)
buy_cost[0] = down_payment  # initial down payment
for i in range(1, len(years)):
    annual_buy_cost = (monthly_payment * 12) + (buy_home_price * property_tax_rate) + (buy_home_price * insurance_rate) + (buy_home_price * maintenance_rate)
    buy_cost[i] = buy_cost[i-1] + annual_buy_cost

# Calculate the crossover point
crossover_year = np.where(rent_cost >= buy_cost)[0][0]

# Display results
st.subheader("Results")
st.write(f"The crossover occurs in year {crossover_year}, with costs as follows:")
st.write(f"Rent cost at year {crossover_year}: ${rent_cost[crossover_year - 1]:,.2f}")
st.write(f"Buy cost at year {crossover_year}: ${buy_cost[crossover_year - 1]:,.2f}")

# Plot the graph
fig, ax = plt.subplots()
ax.plot(years, rent_cost, label='Rent Cost')
ax.plot(years, buy_cost, label='Buy Cost')
ax.axvline(x=crossover_year, color='r', linestyle='--', label=f'Crossover at Year {crossover_year}')
ax.set_xlabel('Years')
ax.set_ylabel('Cumulative Costs ($)')
ax.set_title('Rent vs Buy Cumulative Costs')
ax.legend()
ax.grid(True)

# Display the graph in Streamlit
st.pyplot(fig)
