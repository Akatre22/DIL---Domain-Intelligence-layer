import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Force DIL package from dil_banking/src to the front of sys.path
SRC_PATH = str(Path(__file__).resolve().parent / "dil_banking" / "src")
if SRC_PATH in sys.path:
    sys.path.remove(SRC_PATH)
sys.path.insert(0, SRC_PATH)

# Clear any cached legacy dil module from previous imports
for mod_name in list(sys.modules.keys()):
    if mod_name == "dil" or mod_name.startswith("dil."):
        del sys.modules[mod_name]

from dil import DIL, create_openai_callable

# Streamlit Page Config - Standard, clean Chatbot layout
st.set_page_config(
    page_title="AI Assistant",
    page_icon="💬",
    layout="centered",
)

st.title("💬 AI Assistant")
st.caption("A general conversational chatbot powered by **DIL (Domain Intelligence Layer)**. Ask anything — from general questions to specialized banking and lending advice.")

# Initialize DIL engine in background
@st.cache_resource
def get_dil_engine():
    # Banking pack loaded with India regulatory overlay
    return DIL(domain="banking", jurisdiction="india")

dil = get_dil_engine()

# Sidebar: minimal, clean general settings
with st.sidebar:
    st.header("Settings")
    st.write("This is a standard chatbot. When you ask banking or financial questions, **DIL automatically detects the domain** and activates expert reasoning, deterministic rules, and policy guardrails in the background.")
    
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Check OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.warning("⚠️ `OPENAI_API_KEY` not found in environment or .env. Please configure it to chat.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your AI assistant. You can chat with me about everyday topics or ask detailed financial and banking questions (e.g. loan eligibility, interest rates, RBI rules, or EMI calculations). How can I help you today?"
        }
    ]

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # If DIL detected banking domain for this turn, show a subtle badge & audit drawer
        if msg.get("domain_active"):
            concepts = msg.get("concepts", [])
            rules = msg.get("rules", [])
            params = msg.get("params", {})
            
            with st.expander("⚡ DIL Banking Domain Activated", expanded=False):
                if concepts:
                    st.caption(f"**Recognized Concepts:** {', '.join([f'`{c}`' for c in concepts])}")
                if params:
                    st.caption(f"**Extracted Financial Parameters:** {params}")
                if rules:
                    st.markdown("**Deterministic Rule Checks (Calculated in Code):**")
                    for r in rules:
                        icon = "✅" if r["passed"] else ("⚠️" if r["status"] == "REFER" else "❌")
                        st.markdown(f"- {icon} **{r['rule_title']}** (`{r['rule_id']}`): {r['message']}")

# Standard Chat Input
user_query = st.chat_input("Type your message here...")

if user_query:
    # 1. Display user query
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 2. Process through DIL and LLM
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Prepare conversation history for the LLM
            history_turns = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]
                if m.get("role") in ("user", "assistant")
            ]

            # DIL inspects the query:
            # - Detects if banking domain concepts or terminology are present
            # - Automatically extracts numbers (salary, EMI, loan amount, CIBIL)
            # - Evaluates deterministic rules if numbers are present
            # - Applies banking expertise & guardrails ONLY when domain is triggered
            context_result, prepared_messages = dil.build_messages(
                query=user_query,
                history=history_turns,
            )

            # Connect LLM
            llm = create_openai_callable(
                api_key=api_key,
                model="gpt-4o-mini",
                temperature=0.2,
            )

            with st.spinner("Thinking..."):
                response_text = llm(messages=prepared_messages)

            message_placeholder.markdown(response_text)

            # If DIL was triggered, display the intelligence breakdown
            if context_result.domain_active:
                with st.expander("⚡ DIL Banking Domain Activated", expanded=False):
                    if context_result.detected_concepts:
                        st.caption(f"**Recognized Concepts:** {', '.join([f'`{c}`' for c in context_result.detected_concepts])}")
                    if context_result.extracted_parameters:
                        st.caption(f"**Extracted Financial Parameters:** {context_result.extracted_parameters}")
                    if context_result.evaluated_rules:
                        st.markdown("**Deterministic Rule Checks (Calculated in Code):**")
                        for r in context_result.evaluated_rules:
                            icon = "✅" if r.passed else ("⚠️" if r.status == "REFER" else "❌")
                            st.markdown(f"- {icon} **{r.rule_title}** (`{r.rule_id}`): {r.message}")

            # Save assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "domain_active": context_result.domain_active,
                "concepts": context_result.detected_concepts,
                "rules": [r.__dict__ for r in context_result.evaluated_rules],
                "params": context_result.extracted_parameters,
            })

        except Exception as e:
            err_msg = f"❌ Error: {str(e)}"
            message_placeholder.error(err_msg)
            st.session_state.messages.append({"role": "assistant", "content": err_msg})
