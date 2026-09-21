import streamlit as st
from copilot import agent_executor

st.set_page_config(page_title="GenAI SQL Copilot", page_icon="🤖", layout="wide")

st.title("🤖 Enterprise GenAI SQL Copilot")
st.markdown("Type your business questions below to query the **PostgreSQL** storage structures live.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me any analytical question about our orders, customers, or products!"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_prompt := st.chat_input("e.g., What is our gross revenue or who spent the most?"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("AI is examining schema boundaries and executing SQL..."):
            try:
                response = agent_executor.invoke({"input": user_prompt})
                ai_reply = response["output"]
                st.write(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                st.error(f"❌ Error: {e}")
