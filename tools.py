import asyncio
import assist
from icrawler.builtin import GoogleImageCrawler
import os
import time
import subprocess
from openai import OpenAI


def image_search(query):
    google_Crawler = GoogleImageCrawler(storage={"root_dir": r'./'})
    google_Crawler.crawl(keyword=query, max_num=1)
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
        messages = [{"role": "system",
                     "content": "Write python code to complete the objective. Do not include any non-code in your response. Respond only with the code. All code should be written in python"},
                    {"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        reply = reply.replace("```python", "").replace("```", "")
        return reply
    except Exception as e:
        return str(e)


import os
import subprocess
from openai import OpenAI

import os
import subprocess
from openai import OpenAI

import os
import subprocess
from openai import OpenAI

import os
import subprocess
from openai import OpenAI

def generate_code_react(prompt):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
             "content": "Write React code or Tailwind CSS code to complete the objective. Do not include any non-code in your response. Respond only with the code. All code should be written in JavaScript or JSX."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        reply = reply.replace("```jsx", "").replace("```css", "").replace("```", "")
        if reply.startswith("javascript"):
            reply = reply[len("javascript"):].strip()
        return reply
    except Exception as e:
        print(f"An error occurred while generating code: {e}")
        return ""

def generate_detailed_instructions_prompt(simple_instruction):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
            "content": "Given the following simple instruction, generate detailed instructions to create a full website:\n\n{simple_instruction}\n\nThe detailed instructions should include components, themes, and specific functionalities."},
            {"role": "user", "content": simple_instruction}
        ]
        response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages,
    )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print(f"An error occurred while validating information: {e}")
        return ""
    return

def infer_components_prompt(detailed_instructions):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
             "content": "Given the following description, list the components and their purpose: Be sure to look for themes and colors for CSS files in the instructions. List the components in the format: ComponentName: ComponentDescription. Do not put parenthesis around ComponentName. Ensure the ComponentName is a single word."},
            {"role": "user", "content": detailed_instructions}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print(f"An error occurred while validating information: {e}")
        return ""
    return

def validate_information(prompt):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
             "content": "Determine whether or not the information given to you is enough to make a full react app. If the information given is not enough, then generate pointed yes or no or multiple choice questions for the user to answer about the design of the website. Generate the questions with answer choices A. B. C. etc. depending on the number of options. If it is enough return 'all necessary components and functionalities are covered'."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print(f"An error occurred while validating information: {e}")
        return ""

def gather_detailed_instructions(simple_instruction):
    detailed_instructions = generate_detailed_instructions_prompt(simple_instruction)

    asked_questions = set()
    for _ in range(2):
        validation_result = validate_information(detailed_instructions)
        if "all necessary components and functionalities are covered" in validation_result:
            break

        questions = [q for q in validation_result.split('\n\n')[:10] if q not in asked_questions]
        if not questions:
            break

        for question in questions:
            print(f"Please answer the following question to provide more details:\n{question}")
            additional_info = input("Your answer: ")
            detailed_instructions += f"\n{question}\nAnswer: {additional_info}"
            asked_questions.add(question)

    return detailed_instructions

def create_component_files(component_name, instructions, project_path):
    component_jsx_code = generate_code_react(instructions['jsx'])
    component_css_code = generate_code_react(instructions['css'])



    component_dir = os.path.join(project_path, 'src', 'components', component_name)
    os.makedirs(component_dir, exist_ok=True)

    with open(os.path.join(component_dir, f'{component_name}.jsx'), 'w') as f:
        f.write(component_jsx_code)
    with open(os.path.join(component_dir, f'{component_name}.css'), 'w') as f:
        f.write(component_css_code)

def create_react_app(name, components_instructions, detailed_instructions):
    try:
        base_path = os.getenv('JARVIS_PROJECTS_PATH', '/Users/krishsarin/Downloads/jarvis_test')
        project_path = os.path.join(base_path, name)

        subprocess.run(["npx", "create-react-app", name], cwd=base_path, check=True)
        subprocess.run(["npm", "install", "react-router-dom"], cwd=project_path, check=True)

        # Generate and save components
        for component_name, instruction in components_instructions.items():
            print(component_name)
            create_component_files(component_name, instruction, project_path)

        # Generate main App component and CSS
        main_app_instructions = f"Generate a main App component for a React app with routes for components: {', '.join(components_instructions.keys())}. Use react-router-dom for routing. Ensure all import paths follow the pattern './components/ComponentName/ComponentName'."
        app_jsx_code = generate_code_react(main_app_instructions)
        main_css_instructions = f"Generate CSS for main App component inferred from the following description. {detailed_instructions}"
        app_css_code = generate_code_react(main_css_instructions)

        with open(os.path.join(project_path, 'src', 'App.jsx'), 'w') as f:
            f.write(app_jsx_code)
        with open(os.path.join(project_path, 'src', 'App.css'), 'w') as f:
            f.write(app_css_code)

        print("React project created successfully.")
        print("\nComponents and Descriptions:")
        for name, desc in components_instructions.items():
            print(f"{name}: {desc['description']}")
        print("\nDetailed Instructions:")
        print(detailed_instructions)

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    simple_instruction = "I want to create a cookbook website. This website should have a home page, about page, contact page, and recipes page. The first three pages should be pretty generic but the recipes page should have several cuisines listed and then you can click on those cuisines to get different dishes from that cuisine and then you can click on the dish to get the recipe. The whole theme should be a light green and white color throughout the entire website."
    detailed_instructions = gather_detailed_instructions(simple_instruction)

    # Generate component instructions
    components_prompt = infer_components_prompt(detailed_instructions)


    components = {}
    for line in components_prompt.split('\n'):
        if ':' in line:
            component_name, component_description = line.split(':', 1)
            components[component_name] = {
                'description': component_description.strip(),
                'jsx': f"Generate a {component_name} component. {component_description.strip()}. Do not include any CSS code in this file.",
                'css': f"Generate CSS for the {component_name} component. Ensure it matches the description. Do not include any JSX code in this file."
            }
    print(components)

    # Once all details are gathered, create the React app
    create_react_app("my_generated_website", components, detailed_instructions)

if __name__ == "__main__":
    main()



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
    main()
