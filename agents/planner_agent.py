from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from agents.plan_schema import ResearchPlan
from agents.llm_backend import get_mode, get_llm
from agents.demo_agents import demo_planner

parser = PydanticOutputParser(pydantic_object=ResearchPlan)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strategic research planner AI.\n{format_instructions}"),
    ("human", "Research task: {task}")
])


def planner_agent(task: str) -> ResearchPlan:
    """Generate a structured research plan using LangChain chains + Pydantic."""
    if get_mode() == "demo":
        return demo_planner(task)

    chain = prompt | get_llm() | parser
    return chain.invoke({
        "task": task,
        "format_instructions": parser.get_format_instructions()
    })
