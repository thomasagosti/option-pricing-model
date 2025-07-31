import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# === BLACK-SCHOLES FUNCTION ===
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

# === HEATMAP FUNCTION ===
def plot_heatmap(black_scholes_func, spot_range, vol_range, T, r, K):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, sigma in enumerate(vol_range):
        for j, S in enumerate(spot_range):
            call = black_scholes_func(S, K, T, r, sigma, option_type='call')
            put = black_scholes_func(S, K, T, r, sigma, option_type='put')
            call_prices[i, j] = call
            put_prices[i, j] = put

    fig_call, ax1 = plt.subplots()
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), ax=ax1, cmap="YlGnBu")
    ax1.set_title("Call Option Prices")
    ax1.set_xlabel("Spot Price")
    ax1.set_ylabel("Volatility")

    fig_put, ax2 = plt.subplots()
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), ax=ax2, cmap="YlOrBr")
    ax2.set_title("Put Option Prices")
    ax2.set_xlabel("Spot Price")
    ax2.set_ylabel("Volatility")

    return fig_call, fig_put

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === STYLING ===
st.markdown("""
<style>
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    width: auto;
    margin: 0 auto;
}
.metric-call {
    background-color: #90ee90;
    color: black;
    margin-right: 10px;
    border-radius: 10px;
}
.metric-put {
    background-color: #ffcccb;
    color: black;
    border-radius: 10px;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}
.metric-label {
    font-size: 1rem;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# === SIDEBAR INPUT ===
with st.sidebar:
    st.title("Black-Scholes Model Inputs")
    
    S = st.number_input("Current Asset Price (S)", value=100.0)
    K = st.number_input("Strike Price (K)", value=100.0)
    T = st.number_input("Time to Maturity (T, in years)", value=1.0)
    sigma = st.number_input("Volatility (σ)", value=0.2)
    r = st.number_input("Risk-Free Interest Rate (r)", value=0.05)

    st.markdown("---")
    st.subheader("Heatmap Range Parameters")
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=S*0.8, step=1.0)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=S*1.2, step=1.0)
    vol_min = st.slider('Min Volatility', min_value=0.01, max_value=1.0, value=sigma*0.5, step=0.01)
    vol_max = st.slider('Max Volatility', min_value=0.01, max_value=1.0, value=sigma*1.5, step=0.01)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

# === MAIN PAGE ===
st.title("Black-Scholes Option Pricing Model")

# Show inputs as a table
input_data = {
    "Spot Price (S)": [S],
    "Strike Price (K)": [K],
    "Time to Maturity (T)": [T],
    "Volatility (σ)": [sigma],
    "Interest Rate (r)": [r]
}
st.table(pd.DataFrame(input_data))

# Calculate prices
call_price = black_scholes(S, K, T, r, sigma, option_type='call')
put_price = black_scholes(S, K, T, r, sigma, option_type='put')

# Show outputs
col1, col2 = st.columns([1,1], gap="small")
with col1:
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Price</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Price</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# === HEATMAPS ===
st.markdown("")
st.title("Options Price - Interactive Heatmaps")

st.info("Explore how option prices change with different Spot Prices and Volatility levels while keeping Strike and Maturity fixed.")

fig_call, fig_put = plot_heatmap(black_scholes, spot_range, vol_range, T, r, K)

col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig_call)
with col2:
    st.pyplot(fig_put)
