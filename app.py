import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Jeevan Currency Converter",
    page_icon="💱",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a,
            #1e293b,
            #312e81
        );
        color: white;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 30px;
    }

    .converter-box {
        background: rgba(255, 255, 255, 0.08);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }

    .result-box {
        background: linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        margin-top: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }

    .result-value {
        font-size: 36px;
        font-weight: 800;
    }

    .rate-text {
        font-size: 16px;
        color: #e2e8f0;
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        color: #94a3b8;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">💱 Jeevan Currency Converter</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Convert currencies quickly using live exchange rates</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# CURRENCY DATA
# --------------------------------------------------

currencies = {
    "🇺🇸 USD - US Dollar": "USD",
    "🇮🇳 INR - Indian Rupee": "INR",
    "🇪🇺 EUR - Euro": "EUR",
    "🇬🇧 GBP - British Pound": "GBP",
    "🇯🇵 JPY - Japanese Yen": "JPY",
    "🇦🇺 AUD - Australian Dollar": "AUD",
    "🇨🇦 CAD - Canadian Dollar": "CAD",
    "🇨🇳 CNY - Chinese Yuan": "CNY",
    "🇸🇬 SGD - Singapore Dollar": "SGD",
    "🇦🇪 AED - UAE Dirham": "AED",
    "🇨🇭 CHF - Swiss Franc": "CHF",
    "🇳🇿 NZD - New Zealand Dollar": "NZD"
}

# --------------------------------------------------
# CONVERTER BOX
# --------------------------------------------------

st.markdown('<div class="converter-box">', unsafe_allow_html=True)

amount = st.number_input(
    "💰 Enter Amount",
    min_value=0.0,
    value=1.0,
    step=1.0
)

col1, col2 = st.columns(2)

with col1:
    from_currency_name = st.selectbox(
        "From Currency",
        list(currencies.keys()),
        index=1
    )

with col2:
    to_currency_name = st.selectbox(
        "To Currency",
        list(currencies.keys()),
        index=0
    )

convert_button = st.button(
    "🔄 Convert Currency",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# CURRENCY CONVERSION
# --------------------------------------------------

if convert_button:

    converted_amount = None
    exchange_rate = None

    from_currency = currencies[from_currency_name]
    to_currency = currencies[to_currency_name]

    if amount <= 0:

        st.warning("⚠️ Please enter an amount greater than 0.")

    elif from_currency == to_currency:

        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-value">
                    {amount:,.2f} {to_currency}
                </div>
                <div class="rate-text">
                    Same currency selected
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        url = (
            f"https://api.frankfurter.app/latest"
            f"?amount={amount}"
            f"&from={from_currency}"
            f"&to={to_currency}"
        )

        try:

            response = requests.get(
                url,
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()
                converted_amount = data["rates"][to_currency]

                rate_url = (
                    f"https://api.frankfurter.app/latest"
                    f"?amount=1"
                    f"&from={from_currency}"
                    f"&to={to_currency}"
                )

                rate_response = requests.get(
                    rate_url,
                    timeout=10
                )

                if rate_response.status_code == 200:
                    rate_data = rate_response.json()
                    exchange_rate = rate_data["rates"][to_currency]
                else:
                    exchange_rate = converted_amount / amount

                st.success("✅ Currency converted successfully!")
                st.metric(
                    label="💱 Converted Amount",
                    value=f"{converted_amount:,.2f} {to_currency}"
                )
                st.info(
                    f"📊 Exchange Rate: 1 {from_currency} = "
                    f"{exchange_rate:,.4f} {to_currency}"
                )

            else:

                st.error(
                    "❌ Unable to get exchange rates. "
                    "Please try again."
                )

        except requests.exceptions.Timeout:

            st.error(
                "⏳ Request timed out. "
                "Please check your internet connection and try again."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "🌐 Could not connect to the currency service. "
                "Please check your internet connection."
            )

        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )

# --------------------------------------------------
# INFORMATION
# --------------------------------------------------

st.markdown("---")

st.subheader("ℹ️ About This App")

st.write(
    """
    This application converts one currency into another using
    exchange-rate data from an online currency service.

    **Features:**
    - 💱 Multiple currencies
    - ⚡ Live exchange-rate conversion
    - 🎨 Modern Streamlit interface
    - 🛡️ Error handling
    - 📱 Responsive layout
    - 🌐 Deployment ready
    """
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        🚀 Built with Python + Streamlit
        <br>
        Created by Jeevan Kowshik
    </div>
    """,
    unsafe_allow_html=True
)