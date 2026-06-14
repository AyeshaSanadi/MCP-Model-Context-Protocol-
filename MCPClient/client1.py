import asyncio
from dotenv import load_dotenv
import streamlit as st

from langchain_core.messages import (
    HumanMessage,
    ToolMessage
)
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv()

SERVERS = {
    "ExpenseTracker": {
        "transport": "stdio",
        "command": r"C:\Users\AYESHA\AppData\Local\Programs\Python\Python313\Scripts\uv.exe",
        "args": [
            "--directory",
            r"F:\MCP\ExpenseTracker",
            "run",
            "main.py"
        ]
    }
}


@st.cache_resource
def get_event_loop():
    return asyncio.new_event_loop()


async def get_agent():

    client = MultiServerMCPClient(SERVERS)

    tools = await client.get_tools()

    tool_dict = {
        tool.name: tool
        for tool in tools
    }

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools, tool_dict


async def process_message(user_input):

    llm_with_tools, tool_dict = await get_agent()

    response = await llm_with_tools.ainvoke(
        [HumanMessage(content=user_input)]
    )

    if not response.tool_calls:
        return response.content

    tool_messages = []

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})
        tool_call_id = tool_call["id"]

        tool_result = await tool_dict[
            tool_name
        ].ainvoke(tool_args)

        tool_messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call_id
            )
        )

    final_response = await llm_with_tools.ainvoke(
        [
            HumanMessage(content=user_input),
            response,
            *tool_messages
        ]
    )

    return final_response.content


# -------------------------
# Streamlit UI
# -------------------------

st.set_page_config(
    page_title="Expense Tracker Agent",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Expense Tracker MCP Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Ask something..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            loop = get_event_loop()

            answer = loop.run_until_complete(
                process_message(prompt)
            )

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )