import streamlit as st
import pandas as pd
import pickle, re, string


model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.set_page_config(
    page_title="Spam Detection AI",
    page_icon="📧",
    layout="wide",
)
data = pd.read_csv("spam.csv")
spam_examples = data[data['Category']=='spam']['Message'].tolist()
ham_examples = data[data['Category']=='ham']['Message'].tolist()


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #87CEEB 0%, #ffb6c1 100%) !important;
            background-attachment: fixed;
        }
        body {
            background: transparent !important;
        }
    </style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"


st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("About"):
    st.session_state.page = "About"
if st.sidebar.button("Spam Detection"):
    st.session_state.page = "Spam Detection"

page = st.session_state.page



if page == "Home":
    st.markdown("""
    <div style="background-color:#FFDDC1;padding:25px;border-radius:20px;margin-bottom:20px">
        <h1 style="color:#4B0082;text-align:center;">📧 Welcome to Spam Detection AI</h1>
        <p style="font-size:18px;text-align:center;">
        Instantly detect whether a message is Spam or Not Spam using AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
<div style="text-align: center;">
    <img src="https://images.unsplash.com/photo-1556740749-887f6717d7e4?auto=format&fit=crop&w=800&q=60" width="1100">
</div>
""", unsafe_allow_html=True)

    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Spam Messages**")
        for msg in spam_examples[:5]:
            st.info(msg)
    
    with col2:
        st.markdown("**Ham Messages**")
        for msg in ham_examples[:5]:
            st.success(msg)



elif page == "About":
    st.markdown("""
    <div style="background-color:#D6EAF8;padding:20px;border-radius:15px;margin-bottom:15px">
        <h1 style="color:#1B4F72;text-align:center;">💡 About Spam Detection AI</h1>
        <p style="font-size:16px;text-align:center;">
        AI-powered Streamlit app that classifies messages as Spam or Not Spam using NLP.
        </p>
    </div>
    """, unsafe_allow_html=True)

   
    st.markdown("""
        <style>
        .feature-box {
            padding: 10px;                  
            border-radius: 10px;
            text-align: center;
            min-height: 120px;               
            font-size: 14px;                 
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box" style="background-color:#D5F5E3;">
            <h4 style="color:#117A65;">🧠 AI Powered</h4>
            <p>Spam detection using ML.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box" style="background-color:#FCF3CF;">
            <h4 style="color:#B7950B;">📧 Real-time</h4>
            <p>Instant message check.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box" style="background-color:#FADBD8;">
            <h4 style="color:#C0392B;">🖥️ UI</h4>
            <p>Simple and clean layout.</p>
        </div>
        """, unsafe_allow_html=True)

    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="feature-box" style="background-color:#E8DAEF;">
            <h4 style="color:#7D3C98;">📊 Score</h4>
            <p>Spam probability.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="feature-box" style="background-color:#D1F2EB;">
            <h4 style="color:#148F77;">⚡ Fast</h4>
            <p>Quick results.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div class="feature-box" style="background-color:#FAD7A0;">
            <h4 style="color:#CA6F1E;"> 🔍NLP Engine </h4>
            <p>Clean & analyze messages.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Spam Detection":

    st.markdown("""
    <div style="background-color:#D5F5E3;padding:25px;border-radius:20px;margin-bottom:20px">
        <h1 style="color:#196F3D;text-align:center;">🚀 Spam Detection</h1>
        <p style="font-size:16px;text-align:center;">
        Enter a message below or select a sample spam message.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Select a Sample Spam Message")

    # --------------------------  
    # ONLY SPAM MESSAGES IN SELECTBOX  
    # --------------------------
    spam_choice = st.selectbox("Pick a spam message:", [""] + spam_examples[:20])

    # If user selects a spam example, auto-fill box
    selected_message = spam_choice if spam_choice else ""

    # --------------------------
    # Message Input Box
    # --------------------------
    message = st.text_area("Type your message here...", value=selected_message, height=150)

    # --------------------------
    # Predict Button
    # --------------------------
    if st.button("Check Message"):
        if message.strip() == "":
            st.warning("Please enter a message!")
        else:
            cleaned = clean_text(message)
            vect = vectorizer.transform([cleaned])
            prediction = model.predict(vect)[0]
            prob = model.predict_proba(vect)[0][1]

            if prediction == 1:
                st.error("🚫 SPAM Message")
                st.info(f"Spam Probability: {prob*100:.2f}%")
            else:
                st.success("✅ Not Spam")
                st.info(f"Spam Probability: {(1-prob)*100:.2f}%")