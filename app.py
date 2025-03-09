from flask import Flask, render_template, request
from crewai import Crew,Task
from model.model import professor_agent, academic_advisor_agent, research_librarian_agent, teaching_assistant_agent
from model.tools import local_html_tool

app = Flask(__name__)





@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        knowledge_base_task = Task(
            description=f"Write a well-structured knowledge base about {topic}. Only return the content, do not save a file.",
            agent=professor_agent,
            expected_output="Knowledge base content in markdown format",
        )

        learning_roadmap_task = Task(
            description=f"Develop a structured learning roadmap for mastering {topic}. Only return the content, do not save a file.",
            agent=academic_advisor_agent,
            expected_output="Learning roadmap content in markdown format",
        )

        learning_resources_task = Task(
            description=f"Find and list high-quality learning resources for {topic}. Only return the content, do not save a file.",
            agent=research_librarian_agent,
            expected_output="Learning resources content in markdown format",
        )

        exercises_task = Task(
            description=f"Generate exercises and quizzes to practice {topic}. Only return the content, do not save a file.",
            agent=teaching_assistant_agent,
            expected_output="Practice exercises content in markdown format",
        )
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
        return render_template("content.html")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

