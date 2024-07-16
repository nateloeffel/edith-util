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


def infer_components(overall_instructions):
    prompt = f"Given the following description, list the components and their purpose:\n\n{overall_instructions}\n\nList the components in the format: ComponentName: ComponentDescription"
    response = generate_code(prompt)

    component_instructions = {}
    for line in response.split('\n'):
        if ':' in line:
            component_name, component_description = line.split(':', 1)
            component_instructions[component_name.strip()] = {
                'jsx': f"Generate a {component_name.strip()} component. {component_description.strip()}",
                'css': f"Generate CSS for the {component_name.strip()} component. Ensure it matches the description."
            }
    return component_instructions

def create_react_app(name, overall_instructions):
    try:
        base_path = os.getenv('JARVIS_PROJECTS_PATH', '/Users/krishsarin/Downloads/jarvis_test')
        project_path = os.path.join(base_path, name)

        subprocess.run(["npx", "create-react-app", name], cwd=base_path, check=True)

        main_app_instructions = f"Generate a main App component for a React app with a navbar and routes for components inferred from the following description. Use react-router-dom for routing. {overall_instructions}"
        app_js_code = generate_code_react(main_app_instructions)
        app_css_code = generate_code_react("Generate CSS for the main App component with a dark theme and vibrant accent colors.")

        with open(os.path.join(project_path, 'src', 'App.jsx'), 'w') as f:
            f.write(app_js_code)
        with open(os.path.join(project_path, 'src', 'App.css'), 'w') as f:
            f.write(app_css_code)

        components_instructions = infer_components(overall_instructions)


        for component_name, instruction in components_instructions.items():
            component_jsx_code = generate_code_react(instruction['jsx'])
            component_css_code = generate_code_react(instruction['css'])

            component_dir = os.path.join(project_path, 'src', 'components')
            os.makedirs(component_dir, exist_ok=True)

            with open(os.path.join(component_dir, f'{component_name}.jsx'), 'w') as f:
                f.write(component_jsx_code)
            with open(os.path.join(component_dir, f'{component_name}.css'), 'w') as f:
                f.write(component_css_code)

        print(f"React project created successfully at {project_path}")
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
    react_app_name = "modern_web_app1"
    overall_instructions = """
    Create a React app for a modern, responsive website. The website should have a home page, an about page, a services page, and a contact page. Each page should be a separate component. The design should be visually appealing with a dark theme and vibrant accent colors (e.g., neon blue and pink). Use a clean, minimalist design with ample white space. Include a navigation bar at the top with links to each page. The home page should have a hero section with a catchy headline and a call-to-action button. The services page should have cards to display different services offered, with icons and descriptions. The contact page should have a form to collect user's name, email, and message. The app should be fully responsive and look great on both desktop and mobile devices. Use CSS for styling and ensure good accessibility practices are followed.
    """
    create_react_app(react_app_name, overall_instructions)




