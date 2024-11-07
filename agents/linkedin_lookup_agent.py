import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub


def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini"
    )
    template = """given the full name {name_of_person} I want you to get it me a link of their LinkedIn profile page.
    Your answer should contain only a URL"""
    
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Goolge 4 linkedin profile page",
            func="?",
            description="useful for when you need get the LinkedIn Page URL"
        )
    ]
    return "https://www.linkedin.com/in/lucasdeavila"

if __name__ == "__main__":
    linkedin_url = lookup("lucasdeavila")
    print(linkedin_url)