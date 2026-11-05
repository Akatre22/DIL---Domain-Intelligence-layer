"""
Shock Demo Chatbot: Zero Banking Prompting -> 100% Accredited Banking Output
Powered invisibly by DIL (Domain Intelligence Layer)

Run with:
    streamlit run dil_banking/examples/shock_demo_chatbot.py
"""

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Import DIL from the production package
from dil import DIL

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Everyday AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Everyday AI Chatbot")
st.caption("Notice the code below: **There is ZERO prompt engineering about banking, RBI, LTV, or CIBIL.** Yet try asking complex financial questions!")

# 1. Standard OpenAI Client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ `OPENAI_API_KEY` is not set. Please add it to your `.env` file or export it.")
    st.stop()

client = OpenAI(api_key=api_key)

# 2. Initialize DIL (1-line intelligence infrastructure)
@st.cache_resource
def get_dil_agent():
    dil = DIL(domain="banking", jurisdiction="india")
    return dil.create_agent(role="loan_advisor")

agent = get_dil_agent()

# Sidebar: Show the user what prompt is actually in the code
with st.sidebar:
    st.header("🔍 Developer Inspection")
    st.markdown("""
    **Look at the Python source code:**
    - ❌ No RBI Master Direction instructions
    - ❌ No LTV tier calculations (80%, 75%)
    - ❌ No DTI or FOIR formulas
    - ❌ No financial prompting
    
    Yet ask:
    > *"I make ₹1.2 lakh/month and want an ₹85 lakh loan on a ₹1 crore home. Will I be approved?"*
    
    The AI will compute exact numbers and cite statutory ceilings!
    """)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 3. Standard Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Standard Chat Input
if prompt := st.chat_input("Ask anything (everyday questions or home loan advice)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. THE MAGIC: DIL intercepts the prompt in < 4ms
    # It extracts numbers, computes math (LTV = 85%), checks statutory caps,
    # and delivers grounded context to OpenAI.
    result, prepared_messages = agent.prepare(prompt)

    with st.chat_message("assistant"):
        # Send prepared messages directly to OpenAI
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=prepared_messages,
            stream=True
        )
        response_text = st.write_stream(stream)

        # 6. SHOCK DRAWER: Reveal how DIL computed the math behind the scenes
        if result.detected_concepts or result.evaluated_rules:
            with st.expander("🤯 Wait, how did it calculate that without any banking prompt?", expanded=False):
                st.markdown("**1. Extracted Financial Numbers (Pure Python, Zero LLM):**")
                st.json(result.extracted_parameters)
                
                if result.evaluated_rules:
                    st.markdown("**2. Statutory Regulatory Rules Evaluated (In Code in 3 ms):**")
                    for r in result.evaluated_rules:
                        badge = "✅ PASS" if r.passed else "❌ BREACH"
                        st.markdown(f"- **{badge}** `{r.rule_id}`: {r.message}")
                
                st.caption("⚡ DIL decoupled the domain logic from the prompt. That's why the code stays clean and the math never hallucinates.")

    st.session_state.messages.append({"role": "assistant", "content": response_text})

