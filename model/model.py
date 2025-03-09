from crewai import Agent, LLM ,Task 
import os
from .tools import serper_tool, local_html_tool
from dotenv import load_dotenv



load_dotenv()


my_llm = LLM(
    model='gemini/gemini-1.5-flash',
    api_key=os.getenv('GOOGLE_API_KEY')
)

# Define common instructions for all agents
common_instructions = [
    "Format your response for later inclusion in an HTML document.",
    "Use proper markdown formatting with ## for headings, ** for bold text, and proper list formatting.",
    "DO NOT save your output as a separate file - just return the formatted content."
]

#defiening the agents

professor_agent = Agent(
    name="Professor",
    role="Research and Knowledge Specialist",
    llm=my_llm,
    goal="Create comprehensive knowledge bases on requested topics",
    backstory="You are an expert professor with decades of research experience across multiple disciplines.",
    tools=[local_html_tool],
    instructions=common_instructions + [
        "Develop an exhaustive and well-structured knowledge base that covers fundamental principles, advanced concepts, and latest developments of the given topic.",
    ],
    show_tool_calls=True,
    markdown=True,
    verbose=True,
)


academic_advisor_agent = Agent(
    name="Academic Advisor",
    role="Learning Path Designer",
    llm=my_llm,
    goal="Create structured learning roadmaps",
    backstory="You are a seasoned academic advisor with a track record of creating effective learning roadmaps.",
    tools=[local_html_tool],
    instructions=common_instructions + [
        "Create a learning roadmap that logically progresses from beginner to expert.",
        "Ensure the roadmap includes subtopics, estimated learning times, and recommended study resources.",
    ],
    show_tool_calls=True,
    markdown=True,
    verbose=True,
)


research_librarian_agent = Agent(
    name="Research Librarian",
    role="Learning Resource Specialist",
    llm=my_llm,
    goal="Curate high-quality learning resources",
    backstory="You are a skilled research librarian with access to the best educational resources.",
    tools=[serper_tool, local_html_tool],
    instructions=common_instructions + [
        "Find a list of the best learning resources for the topic, including books, tutorials, documentation, and GitHub repositories.",
        "Use SerperDev to search for the most relevant and up-to-date materials.",
        "Format the response with a list of resources, descriptions, and links.",
    ],
    show_tool_calls=True,
    markdown=True,
    verbose=True,
)


teaching_assistant_agent = Agent(
    name="Teaching Assistant",
    role="Exercise Creator",
    llm=my_llm,
    goal="Generate practice exercises and quizzes",
    backstory="You are an experienced teaching assistant with a passion for creating engaging and effective practice exercises.",
    tools=[serper_tool, local_html_tool],
    instructions=common_instructions + [
        "Create a mix of conceptual, coding, and real-world exercises on the topic.",
        "Include progressive exercises from beginner to expert level.",
        "Ensure there are solutions and explanations for all exercises.",
    ],
    show_tool_calls=True,
    markdown=True,
    verbose=True,
)


