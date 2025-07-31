from streamlist as st
from pricing_model import black_scholes
st.set_page_config(page_title="Black-Scholes Option Pricer", layout="centered")
st.title("Black-Scholes Option Pricing Model")
S=st.number_input("Spot Price (S)", value=100.0)
K = st.number_input("Strike Price (K)", value=100.0)
T = st.number_input("Time to Maturity (T, in years)", value=1.0)
r = st.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.number_input("Volatility (σ)", value=0.2)
option_type = st.selectbox("Option Type", ("call", "put"))

# Compute price
if st.button("Calculate Option Price"):
    price = black_scholes(S, K, T, r, sigma, option_type)
    st.success(f"The {option_type} option price is: **{price:.2f}**")
