# chat_ui.py
import asyncio
import threading

import httpx
import streamlit as st
from agents import Runner

from app.agents.researcher import research_agent
from app.context import AppContext

from dotenv import load_dotenv
load_dotenv()  # must run first so LANGSMITH_* reach os.environ

from agents import set_trace_processors
from langsmith.integrations.openai_agents_sdk import OpenAIAgentsTracingProcessor

set_trace_processors([OpenAIAgentsTracingProcessor()])

st.set_page_config(page_title="Research Report Agent", page_icon="🔎")
st.title("🔎 Research Report Agent")


# One event loop that lives for the whole Streamlit process.
# This prevents the "Event loop is closed" error from asyncio.run().
@st.cache_resource
def get_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()
    return loop


def run_async(coro):
    """Run a coroutine on the shared loop and wait for the result."""
    return asyncio.run_coroutine_threadsafe(coro, get_loop()).result()


async def ask_agent(history: list[dict]) -> str:
    async with httpx.AsyncClient(timeout=20) as http:
        ctx = AppContext(user_id="streamlit-user", http=http)
        result = await Runner.run(research_agent, history, context=ctx)
        return result.final_output


# Chat history survives reruns via session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Settings")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Replay history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Enter a research topic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            try:
                answer = run_async(ask_agent(st.session_state.messages))
            except Exception as e:
                answer = f"Something went wrong: `{type(e).__name__}: {e}`"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})