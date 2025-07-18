import advanced_mcp_client as mcp_client
import chat_assistant

our_mcp_client = mcp_client.MCPClient(["python", "mcp_server.py"])

our_mcp_client.start_server()
our_mcp_client.initialize()
our_mcp_client.initialized()

import json

import os
import dlt
import yaml
import requests
from openai import AzureOpenAI
from dataclasses import dataclass


@dataclass
class LLMServiceConfig:
    host: str
    api_key: str
    api_version: str
    model: str


with open("../OPENAI_API_KEY.yaml") as f:
    details = yaml.safe_load(f)["Glossary Terms Extraction Service"]

service_config = LLMServiceConfig(
    host=f"{details['protocol']}://{details['host']}",
    api_key=details['api_key'],
    api_version=details['api_version'],
    model=details['model']
)
client = AzureOpenAI(
    api_version=service_config.api_version,
    azure_endpoint=service_config.host,
    api_key=service_config.api_key
)
model = service_config.model


class MCPTools:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.tools = None

    def get_tools(self):
        if self.tools is None:
            mcp_tools = self.mcp_client.get_tools()
            self.tools = mcp_client.convert_tools_list(mcp_tools)
        return self.tools

    def function_call(self, tool_call_response):
        function_name = tool_call_response.name
        arguments = json.loads(tool_call_response.arguments)

        result = self.mcp_client.call_tool(function_name, arguments)

        return {
            "type": "function_call_output",
            "call_id": tool_call_response.call_id,
            "output": json.dumps(result, indent=2),
        }

our_mcp_client = mcp_client.MCPClient(["python", "mcp_server.py"])

our_mcp_client.start_server()
our_mcp_client.initialize()
our_mcp_client.initialized()

mcp_tools = mcp_client.MCPTools(mcp_client=our_mcp_client)


developer_prompt = """
You help users find out the weather in their cities. 
If they didn't specify a city, ask them. Make sure we always use a city.
""".strip()

chat_interface = chat_assistant.ChatInterface()

chat = chat_assistant.ChatAssistant(
    tools=mcp_tools,
    developer_prompt=developer_prompt,
    chat_interface=chat_interface,
    client=client
)

chat.run()