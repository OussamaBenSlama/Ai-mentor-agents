from crewai_tools import SerperDevTool 
from crewai.tools import BaseTool 
from typing import Dict
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re

load_dotenv()

# Define the SerperDevTool object
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
serper_tool = SerperDevTool()



class LocalHtmlSaveTool(BaseTool):
    name: str = "HtmlSaveTool"
    description: str = "Replaces the content inside an existing .html file within a div with class 'content'. If the file doesn't exist, it creates one."

    def _run(self, content_dict: Dict, title: str = "Generated_Document"):
        if 'is_final_document' not in content_dict or not content_dict['is_final_document']:
            return content_dict.get('content', str(content_dict))

        static_dir = os.path.join(os.getcwd(), "templates")
        os.makedirs(static_dir, exist_ok=True)
        file_name = "content.html"
        file_path = os.path.join(static_dir, file_name)

        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    soup = BeautifulSoup(file.read(), 'html.parser')
                content_div = soup.find('div', class_='content')
                
                if content_div:
                    content_div.clear()
                    new_content_html = self._generate_content(content_dict)
                    new_content_soup = BeautifulSoup(new_content_html, 'html.parser')
                    content_div.append(new_content_soup)
                    
                else:
                    container = soup.find('div', class_='container')
                    if container:
                        new_div = soup.new_tag('div', attrs={'class': 'content'})
                        new_content_html = self._generate_content(content_dict)
                        new_content_soup = BeautifulSoup(new_content_html, 'html.parser')
                        new_div.append(new_content_soup)
                        container.append(new_div)
                        print("Content div created in container!")
                    else:
                        body = soup.find('body')
                        if body:
                            new_div = soup.new_tag('div', attrs={'class': 'content'})
                            new_content_html = self._generate_content(content_dict)
                            new_content_soup = BeautifulSoup(new_content_html, 'html.parser')
                            new_div.append(new_content_soup)
                            body.append(new_div)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(str(soup))
            else:
                updated_content = f"""<!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8" />
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                        <title>Instructo</title>
                        <link rel="stylesheet" href="{{ url_for('static', filename='content.css') }}">
                    </head>
                    <body>
                        <div id="app">
                            <div class="container">
                                <div class="content">
                                    {self._generate_content(content_dict)}
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                """
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(updated_content)
            return f"Document updated successfully at {file_path}"

        except Exception as e:
            import traceback
            return f"Error updating document: {str(e)}\n{traceback.format_exc()}"

    def _generate_content(self, content_dict):
        content = ""
        for section, content_item in content_dict.items():
            if section != 'is_final_document':
                content += f"<div class='section'>{self._format_content(content_item)}</div>\n"
        return content

    def _format_content(self, content):
        if not isinstance(content, str):
            content = str(content)
        content = re.sub(r'^(#{1,6})\s*(.*?)$', 
                         lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', 
                         content, flags=re.MULTILINE)

        content = content.replace("\n", "<br>")
        content = content.replace("```", "")
        content = re.sub(r'\*\*(.*?)\*\*|__(.*?)__', r'<strong>\1\2</strong>', content)
        content = re.sub(r'\*(.*?)\*|_(.*?)_', r'<em>\1\2</em>', content)
        content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
        content = re.sub(r'^[\-\*] (.*?)$', r'<li>\1</li>', content, flags=re.MULTILINE)
        content = re.sub(r'(<li>.*?</li>)+', lambda m: f"<ul>{m.group(0)}</ul>", content, flags=re.DOTALL)
        content = re.sub(r'^\d+\.\s(.*?)$', r'<li>\1</li>', content, flags=re.MULTILINE)
        content = re.sub(r'(<li>.*?</li>)+', lambda m: f"<ol>{m.group(0)}</ol>", content, flags=re.DOTALL)

        return content


local_html_tool = LocalHtmlSaveTool()

