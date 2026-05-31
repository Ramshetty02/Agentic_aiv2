import json
from typing import Union
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert AI Research Analyst.
Analyze the research data and return a structured markdown report with:
## Summary
## Key Trends
## Critical Insights
## Data Gaps & Limitations
## Conclusion
Be precise, cite specific data points, avoid generic statements."""),
    ("human", "Analyze this data:\n\n{data}")
])

def analyst_agent(data: Union[dict, str]) -> str:
    """Analyze research data using a structured LangChain prompt chain."""
    raw = data.get("raw_content", json.dumps(data, indent=2)) if isinstance(data, dict) else str(data)
    chain = PROMPT | llm
    return chain.invoke({"data": raw[:8000]}).content
