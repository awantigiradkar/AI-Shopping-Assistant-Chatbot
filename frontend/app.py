import streamlit as st
import requests
import json

# Configure page settings
st.set_page_config(page_title="Shop Assistant", layout="wide")

# ---- Inject Premium Custom CSS Styles ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Make background dark-violet theme */
    .stApp {
        background-color: #0d0a1b !important;
        background-image: radial-gradient(at 0% 0%, rgba(108, 92, 231, 0.15) 0px, transparent 50%),
                          radial-gradient(at 100% 100%, rgba(253, 121, 168, 0.12) 0px, transparent 50%) !important;
    }
    
    /* Premium Sidebar glassmorphic overrides */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 12, 30, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Title overrides */
    h1, h2, h3 {
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(108, 92, 231, 0.08), rgba(253, 121, 168, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
        text-align: center;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(to right, #a29bfe, #fd79a8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #b2bec3;
        font-weight: 400;
    }
    
    /* Custom Styling for Streamlit Selectboxes */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(108, 92, 231, 0.4) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Custom Styling for Text Input */
    div[data-testid="stTextInput"] input {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 10px 14px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #6c5ce7 !important;
        box-shadow: 0 0 10px rgba(108, 92, 231, 0.3) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Custom Scrollbar for Sidebar Chat */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 14px;
        padding: 10px 5px;
        max-height: 380px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: rgba(255, 255, 255, 0.1) transparent;
    }
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
    }
    
    /* Product Cards */
    .product-card {
        background-color: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 12px;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 35px 0 rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .product-card:hover {
        box-shadow: 0 14px 45px 0 rgba(108, 92, 231, 0.15);
        transform: translateY(-5px);
        border-color: rgba(108, 92, 231, 0.35);
        background-color: rgba(255, 255, 255, 0.03);
    }
    .product-title {
        font-size: 20px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .product-desc {
        font-size: 14px;
        color: #a4b0be;
        line-height: 1.6;
        margin-top: 10px;
    }
    
    /* Badges / Chips */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 14px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-brand { background-color: rgba(108, 92, 231, 0.15); color: #a29bfe; border: 1px solid rgba(108, 92, 231, 0.25); }
    .badge-gender { background-color: rgba(0, 206, 201, 0.12); color: #81ecec; border: 1px solid rgba(0, 206, 201, 0.2); }
    .badge-color { background-color: rgba(253, 203, 110, 0.12); color: #ffeaa7; border: 1px solid rgba(253, 203, 110, 0.2); }
    .badge-price { background-color: rgba(255, 118, 117, 0.18); color: #ff7675; border: 1px solid rgba(255, 118, 117, 0.28); font-size: 14px; font-weight: 700; border-radius: 12px; }
    
    /* Chat Bubble styling */
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 20px;
        font-size: 14px;
        line-height: 1.5;
        width: fit-content;
        max-width: 88%;
        margin-bottom: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .user-bubble {
        background: linear-gradient(135deg, #6c5ce7, #855efc);
        color: #ffffff;
        align-self: flex-end;
        border-bottom-right-radius: 4px;
        margin-left: auto;
    }
    .bot-bubble {
        background-color: rgba(255, 255, 255, 0.04);
        color: #ecf0f1;
        align-self: flex-start;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Cart Container */
    .cart-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 16px;
        margin-top: 10px;
        margin-bottom: 15px;
        backdrop-filter: blur(12px);
    }
    .cart-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        color: #b2bec3;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        padding-bottom: 6px;
    }
    .cart-item-name {
        font-weight: 500;
        color: #ffffff;
    }
    .cart-total {
        display: flex;
        justify-content: space-between;
        font-weight: 700;
        color: #a29bfe;
        font-size: 15px;
        margin-top: 10px;
    }

    /* Style for buttons in the main content area */
    div[data-testid="stMain"] div.stButton > button {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 6px 12px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stMain"] div.stButton > button:hover {
        background: rgba(108, 92, 231, 0.15) !important;
        border-color: rgba(108, 92, 231, 0.4) !important;
        color: #a29bfe !important;
        transform: translateY(-2px) !important;
    }
    div[data-testid="stMain"] div.stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Sidebar buttons style */
    section[data-testid="stSidebar"] div.stButton > button {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        width: 100% !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.06) !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
    }
    
    /* Prominent Send button in sidebar */
    section[data-testid="stSidebar"] div.send-btn div.stButton > button {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.2) !important;
    }
    section[data-testid="stSidebar"] div.send-btn div.stButton > button:hover {
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Reset button in sidebar */
    section[data-testid="stSidebar"] div.reset-btn div.stButton > button {
        background: rgba(255, 118, 117, 0.08) !important;
        border: 1px solid rgba(255, 118, 117, 0.15) !important;
        color: #ff7675 !important;
    }
    section[data-testid="stSidebar"] div.reset-btn div.stButton > button:hover {
        background: rgba(255, 118, 117, 0.15) !important;
        border-color: #ff7675 !important;
        color: #ff7675 !important;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Helper function to send a query to the chatbot API
def send_query_to_bot(query_text):
    if not query_text.strip():
        return
    try:
        res = requests.post("http://127.0.0.1:8001/chat", json={
            "query": query_text,
            "history": st.session_state.chat_history,
            "brand": st.session_state.get("selected_brand", "All"),
            "gender": st.session_state.get("selected_gender", "All")
        })
        if res.status_code == 200:
            data = res.json()
            st.session_state.chat_history = data["history"]
        elif res.status_code == 503:
            st.sidebar.error("The AI service is currently busy. Please try again!")
        else:
            st.sidebar.error(f"API Error (Status {res.status_code}): {res.text or 'Error'}")
    except Exception as e:
        st.sidebar.error(f"Network Error: {e}")

# ---- Sidebar Chat UI ----
st.sidebar.title("Shop Assistant")

# Interactive Chat Starters
st.sidebar.markdown("**Quick Suggestions:**")
if st.sidebar.button("Under ₹5000", key="starter_budget"):
    st.session_state.chat_history.append("User: What are the best shoes under ₹5000?")
    send_query_to_bot("What are the best shoes under ₹5000?")
    st.rerun()

st.sidebar.markdown("---")

# Render chat bubbles in sidebar
chat_html = "<div class='chat-container'>"
for msg in st.session_state.chat_history:
    if msg.startswith("User:"):
        text = msg[len("User:"):].strip()
        chat_html += f"<div class='chat-bubble user-bubble'><b>You</b><br>{text}</div>"
    elif msg.startswith("Assistant:"):
        text = msg[len("Assistant:"):].strip()
        chat_html += f"<div class='chat-bubble bot-bubble'><b>Assistant</b><br>{text}</div>"
chat_html += "</div>"
st.sidebar.markdown(chat_html, unsafe_allow_html=True)

# User input text input and action buttons
with st.sidebar:
    user_query = st.text_input("Your question:", key="user_query")
    
    col_send, col_clear = st.columns([2, 1])
    with col_send:
        st.markdown('<div class="send-btn">', unsafe_allow_html=True)
        if st.button("Send", key="send_chat_btn"):
            if user_query.strip():
                st.session_state.chat_history.append(f"User: {user_query}")
                with st.spinner("Assistant is typing..."):
                    send_query_to_bot(user_query)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_clear:
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("Clear", key="clear_chat_btn"):
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Shopping Cart Widget in Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Your Shopping Cart")
if not st.session_state.cart:
    st.sidebar.info("Your cart is empty. Click 'Add to Cart' on catalog products.")
else:
    cart_html = "<div class='cart-container'>"
    total_price = 0
    for item_name, item_info in st.session_state.cart.items():
        item_total = item_info["price"] * item_info["qty"]
        total_price += item_total
        cart_html += f"<div class='cart-item'><div class='cart-item-name'>{item_name} (x{item_info['qty']})</div><div>₹{int(item_total)}</div></div>"
    cart_html += f"<div class='cart-total'><div>Total:</div><div>₹{int(total_price)}</div></div></div>"
    st.sidebar.markdown(cart_html, unsafe_allow_html=True)
    
    cart_col1, cart_col2 = st.sidebar.columns(2)
    with cart_col1:
        if st.sidebar.button("Checkout", key="checkout_btn"):
            st.sidebar.success("Checkout simulated successfully!")
            st.session_state.cart = {}
            st.rerun()
    with cart_col2:
        if st.sidebar.button("Clear Cart", key="clear_cart_btn"):
            st.session_state.cart = {}
            st.rerun()

# ---- Main Page Hero Banner ----
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Shop AI Smart Catalog</div>
        <div class="hero-subtitle">Discover premium apparel curated for you with real-time AI conversation guidance.</div>
    </div>
""", unsafe_allow_html=True)

# Fetch product data from backend
try:
    response = requests.get("http://127.0.0.1:8001/products")
    products = response.json()

    if not products:
        st.warning("No products found.")
    else:
        # Get filter values
        brands = sorted(set(p["ProductBrand"] for p in products if p["ProductBrand"]))
        genders = sorted(set(p["Gender"] for p in products if p["Gender"]))

        st.subheader("Filter Products")
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_brand = st.selectbox("Brand", ["All"] + brands, key="selected_brand")
        with col2:
            selected_gender = st.selectbox("Gender", ["All"] + genders, key="selected_gender")
        with col3:
            sort_order = st.selectbox("Sort by Price", ["Default", "Low to High", "High to Low"])

        # Apply filters
        filtered = products
        if selected_brand != "All":
            filtered = [p for p in filtered if p["ProductBrand"] == selected_brand]
        if selected_gender != "All":
            filtered = [p for p in filtered if p["Gender"] == selected_gender]

        # Apply sorting
        if sort_order == "Low to High":
            filtered = sorted(filtered, key=lambda x: float(x["Price"]))
        elif sort_order == "High to Low":
            filtered = sorted(filtered, key=lambda x: float(x["Price"]), reverse=True)

        # Display products in two columns
        cols = st.columns(2)
        for idx, product in enumerate(filtered):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="product-card">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px;">
                                <div class="product-title">{product['ProductName']}</div>
                                <span class="badge badge-price">₹{product['Price']}</span>
                            </div>
                            <div style="margin-top: 10px; margin-bottom: 10px;">
                                <span class="badge badge-brand">🏷️ {product['ProductBrand']}</span>
                                <span class="badge badge-gender">👥 {product['Gender']}</span>
                                <span class="badge badge-color">🎨 {product['PrimaryColor']}</span>
                            </div>
                            <div class="product-desc">{product['Description']}</div>
                        </div>
                        <div style="margin-top: 12px; margin-bottom: 8px;">
                            <a href="https://www.google.com/search?tbm=isch&q={product['ProductBrand']}+{product['ProductName']}+shoe" target="_blank" style="text-decoration: none; color: #a29bfe; font-size: 13px; font-weight: 500;">🔍 Search Google Images</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Card Actions: Add to Cart and Ask Assistant
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("Add to Cart", key=f"add_{product['ProductID']}"):
                        p_name = product['ProductName']
                        p_price = float(product['Price'])
                        p_brand = product['ProductBrand']
                        if p_name in st.session_state.cart:
                            st.session_state.cart[p_name]["qty"] += 1
                        else:
                            st.session_state.cart[p_name] = {"price": p_price, "qty": 1, "brand": p_brand}
                        st.toast(f"Added {p_name} to cart!", icon="🛒")
                        st.rerun()
                with btn_col2:
                    if st.button("Ask Bot", key=f"ask_{product['ProductID']}"):
                        q_text = f"Tell me more about the {product['ProductBrand']} {product['ProductName']}."
                        st.session_state.chat_history.append(f"User: {q_text}")
                        send_query_to_bot(q_text)
                        st.rerun()

except Exception as e:
    st.error(f"Could not fetch products: {e}")