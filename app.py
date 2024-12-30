import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set Streamlit app title
st.title("Crypto Portfolio Tracker")

# Instructions
st.write("""
### Enter your wallet address to fetch holdings and view real-time data.
Supported networks: Ethereum (ERC-20 tokens).
""")

# Input Wallet Address
wallet_address = st.text_input("Wallet Address (Ethereum)")


# CoinGecko API for fetching prices
def fetch_token_prices(tokens):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(tokens), "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    return response.json()


# Function to fetch holdings using Etherscan API
def fetch_eth_holdings(wallet, etherscan_api_key):
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": "4ZYT4JJ9Y57FKN96RMVMXAMQPNQK7JH3DR",
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "1":
        return data["result"]
    else:
        st.error("Failed to fetch holdings. Please check the wallet address.")
        return []


# Display portfolio
if st.button("Fetch Holdings"):
    if wallet_address:
        etherscan_api_key = "YOUR_ETHERSCAN_API_KEY"  # Replace with your Etherscan API key

        st.write(f"Fetching holdings for wallet: `{wallet_address}`")

        # Fetch token transactions
        transactions = fetch_eth_holdings(wallet_address, etherscan_api_key)

        if transactions:
            # Process holdings
            holdings = {}
            for tx in transactions:
                token_name = tx["tokenSymbol"]
                token_amount = int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))
                if token_name in holdings:
                    holdings[token_name] += token_amount
                else:
                    holdings[token_name] = token_amount

            # Convert holdings to DataFrame
            tokens = list(holdings.keys())
            token_prices = fetch_token_prices(tokens)
            data = []
            for token, amount in holdings.items():
                price = token_prices.get(token.lower(), {}).get("usd", 0)
                value = price * amount
                data.append({"Token": token, "Amount": amount, "Price (USD)": price, "Value (USD)": value})
            portfolio = pd.DataFrame(data)

            # Display portfolio table
            st.subheader("Portfolio")
            st.table(portfolio)

            # Portfolio distribution pie chart
            st.subheader("Portfolio Distribution")
            fig, ax = plt.subplots()
            ax.pie(portfolio["Value (USD)"], labels=portfolio["Token"], autopct='%1.1f%%')
            st.pyplot(fig)

            # Download CSV button
            st.subheader("Export Portfolio")
            csv = portfolio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Portfolio as CSV",
                data=csv,
                file_name='portfolio.csv',
                mime='text/csv',
            )
        else:
            st.error("No holdings found or invalid wallet address.")
    else:
        st.error("Please enter a valid wallet address.")
