from crewai import Crew
from model import professor_agent, academic_advisor_agent, research_librarian_agent, teaching_assistant_agent
from model import knowledge_base_task, learning_roadmap_task, learning_resources_task, exercises_task
from tools import local_html_tool

topic = "Cloud Computing"

crew = Crew(
    agents=[professor_agent, academic_advisor_agent, research_librarian_agent, teaching_assistant_agent],
    tasks=[knowledge_base_task, learning_roadmap_task, learning_resources_task, exercises_task],
    verbose=True
)

results = crew.kickoff()
tasks_outputs = results.tasks_output
try:
    content_dict = {
        'is_final_document': True 
    }
    for task, section_name in [
        (knowledge_base_task, "Knowledge Base"),
        (learning_roadmap_task, "Learning Roadmap"),
        (learning_resources_task, "Learning Resources"),
        (exercises_task, "Practice Exercises")
    ]:
        task_output = next((output for output in tasks_outputs if output.description == task.description), None)
        if task_output:
            content_dict[section_name] = task_output.raw
            print(f"Content found for {section_name}: {task_output.raw}")
        else:
            content_dict[section_name] = f"No content available for {section_name}"
            print(f"No content found for {section_name}")
    final_status = local_html_tool._run(
        content_dict,
        title=f"{topic}_Complete_Guide"
    )
    print(f"Final document status: {final_status}")
except Exception as e:
    import traceback
    print(f"Error creating final document: {str(e)}")
    print(traceback.format_exc())