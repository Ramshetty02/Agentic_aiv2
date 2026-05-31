from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

class ResearchPlan(BaseModel):
    """Structured research plan with Pydantic validation."""
    objective: str = Field(description="Clear research objective")
    steps: List[str] = Field(description="Ordered research steps")
    expected_sources: List[str] = Field(description="Types of sources to target")
    key_questions: List[str] = Field(description="Key questions to answer")

parser = PydanticOutputParser(pydantic_object=ResearchPlan)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strategic research planner AI.\n{format_instructions}"),
    ("human", "Research task: {task}")
])

def planner_agent(task: str) -> str:
    """Generate a structured research plan using LangChain chains + Pydantic."""
    chain = prompt | llm | parser
    plan = chain.invoke({
        "task": task,
        "format_instructions": parser.get_format_instructions()
    })
    out = f"## 🎯 Objective\n{plan.objective}\n\n## 📋 Steps\n"
    for i, step in enumerate(plan.steps, 1):
        out += f"{i}. {step}\n"
    out += "\n## ❓ Key Questions\n"
    for q in plan.key_questions:
        out += f"- {q}\n"
    return out
