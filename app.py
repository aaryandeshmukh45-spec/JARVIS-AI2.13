import os
import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")
st.title("🤖 Jarvis - Personal AI Assistant")

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if not api_key:
    st.warning("कृपया काम सुरू करण्यासाठी Gemini API Key टाका.")
    st.stop()

genai.configure(api_key=api_key)

system_instruction = (
    "You are Jarvis, a highly intelligent, polite, and helpful AI assistant. "
    "Respond concisely, smartly, and address the user politely."
)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_prompt = st.chat_input("Jarvis ला काहीही विचारा...")

def speak_text(text):
    safe_text = text.replace('"', '\\"').replace("\n", " ")
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{safe_text}");
        msg.rate = 1.0;
        msg.pitch = 0.9;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Jarvis विचार करत आहे..."):
            response = model.generate_content(user_prompt)
            reply = response.text
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            speak_text(reply)
