import asyncio
import assist
from icrawler.builtin import GoogleImageCrawler
import os
import time
import subprocess
from openai import OpenAI




def image_search(query):
    google_Crawler = GoogleImageCrawler(storage= {"root_dir": r'./'})
    google_Crawler.crawl(keyword= query, max_num=1)
    print("Image Found")

def create_directory(dirname):
    base_path = os.getenv('JARVIS_PROJECTS_PATH')
    if not dirname:
        dirname = str(int(time.time()))
    folder = dirname
    os.makedirs(os.path.join(base_path, folder), exist_ok=True)

def create_python_env(name):
    base_path = os.getenv('JARVIS_PROJECTS_PATH')
    if not name:
        print("No environment name was given")
        return

    project_path = os.path.join(base_path, name)
    venv_path = os.path.join(project_path, "venv")

    try:
        os.makedirs(project_path, exist_ok=True)
        subprocess.run(["python3", "-m", "venv", venv_path], check=True)

        main_py_path = os.path.join(project_path, "main.py")
        with open(main_py_path, 'w') as f:
            f.write("""# This is the main.py file""")

        return project_path
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_code(prompt):
    client = OpenAI()
    try:
        messages = [{"role": "system", "content": "Write python code to complete the objective. Do not include any non-code in your response. Respond only with the code. All code should be written in python"},
                    {"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        reply = response.choices[0].message.content
        reply = reply.replace("```python", "").replace("```", "")
        return reply
    except Exception as e:
        return str(e)

def generate_code_react(prompt):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
             "content": "Write React code to complete the objective. Do not include any non-code in your response. Respond only with the code. All code should be written in JavaScript or JSX."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        reply = response.choices[0].message.content
        print(f"Generated code: {reply}")
        reply = reply.replace("```jsx", "").replace("```css", "").replace("```", "")
        return reply
    except Exception as e:
        print(f"An error occurred while generating code: {e}")
        return ""

def create_react_app(name, overall_instructions):
    base_path = os.getenv('JARVIS_PROJECTS_PATH')
    if not name:
        print("No project name was given")
        return

    project_path = os.path.join(base_path, name)

    try:
        os.makedirs(project_path, exist_ok=True)
        subprocess.run(["npx", "create-react-app", name], cwd=base_path)

        app_jsx_instructions = f"Generate the main App.jsx content for a React application. The application should follow these overall instructions: {overall_instructions}. Include necessary imports and a basic component structure. Start with import React from 'react';"
        app_css_instructions = f"Generate the main App.css content for a React application. The application should follow these overall instructions: {overall_instructions}. Include basic CSS styles."
        component_instructions = f"Generate a simple React functional component for a React application. The application should follow these overall instructions: {overall_instructions}. Do not include import statements."

        app_jsx_code = generate_code(app_jsx_instructions)
        app_css_code = generate_code(app_css_instructions)
        component_code = generate_code(component_instructions)

        app_jsx_path = os.path.join(project_path, "src", "App.jsx")
        app_css_path = os.path.join(project_path, "src", "App.css")
        component_path = os.path.join(project_path, "src", "components", "Calculator.jsx")

        os.makedirs(os.path.dirname(component_path), exist_ok=True)

        with open(app_jsx_path, 'w') as f:
            f.write(app_jsx_code)

        with open(app_css_path, 'w') as f:
            f.write(app_css_code)

        with open(component_path, 'w') as f:
            f.write(component_code)

        index_js_path = os.path.join(project_path, "src", "index.js")
        with open(index_js_path, 'r') as f:
            index_js_content = f.read()

        index_js_content = index_js_content.replace('./App', './App.jsx')

        with open(index_js_path, 'w') as f:
            f.write(index_js_content)

        print(f"React project and custom files created successfully in {project_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
def create_python_script(instructions, dir_path):
    base_path = {dir_path}
    create_python_env(base_path)
    try:
        code = generate_code(instructions)
        print(f"Generated code: {code}")

        file_path = os.path.join(base_path, "main.py")

        with open(file_path, 'w') as f:
            f.write(code)

        print(f"Python script created successfully at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")









def parse_command(command, *args):
    if command == "print":
        print("Hello World!")
    elif command == "light_on":
        print("Turning on the light")
    elif command == "light_off":
        print("Turning off the light")
    elif command == "exit":
        print("Exiting program")
        exit()
    elif command == "get_weather":
        if args:
            location = args[0]
            assist.TTS(f"The current weather in {location} is sunny.")
        else:
            assist.TTS("No location provided.")
    elif command == "morning_news":
        print("Here are the morning news...")
    elif command == "search":
        if args:
            query = args[0]
            print("searching for a " + query)
            image_search(query)
        else:
            assist.TTS("No image query provided")
    elif command == "create_directory":
        print(args)
        create_directory(args[0])
    elif command == "create_python_environment":
        print(args)
        create_python_env(args[0])
    elif command == "create_python_script":
        if args and len(args) > 1:
            instructions = args[0]
            dir_path = args[1]
            create_python_script(instructions, dir_path)
            assist.TTS("We're done!")
        else:
            print("Insufficient arguments for creating a Python script.")
    elif command == "create_react_app":
        if args and len(args) > 1:
            name = args[0]
            instructions = args[1]
            create_react_app(name, instructions)
            assist.TTS("React app created!")
        else:
            print("Insufficient arguments for creating a React app.")
    else:
        print("Invalid command")


if __name__ == "__main__":
    base_path = os.getenv('JARVIS_PROJECTS_PATH')
    print(f"JARVIS_PROJECTS_PATH: {base_path}")
    react_app_name = "calculator_app1"
    overall_instructions = "Create a React app with a calculator that can perform addition, subtraction, multiplication, and division. The calculator should have buttons for digits 0-9, operations (+, -, *, /), and a display to show the current input and result. The design should look aesthetically pleasing, similar to a phone application with an orange and black theme."

    create_react_app(react_app_name, overall_instructions)




