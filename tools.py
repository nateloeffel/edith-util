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
             "content": "Write React code to complete the objective fully. Ensure the code is clean, modern, and uses Tailwind CSS classes for styling. Respond only with the code."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        reply = reply.replace("```jsx", "").replace("```", "")
        if reply.startswith("javascript"):
            reply = reply[len("javascript"):].strip()
        return reply
    except Exception as e:
        print(f"An error occurred while generating code: {e}")
        return ""


def generate_code_css(prompt):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
             "content": "Write Tailwind CSS classes for the described design. Respond only with the classes."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        reply = reply.replace("```css", "").replace("```", "")
        return reply.strip()
    except Exception as e:
        print(f"An error occurred while generating CSS: {e}")
        return ""


def generate_functionality_instructions_prompt(simple_instruction):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
             "content": """
             Given the following simple instruction, generate detailed instructions for the functionality of the website: The detailed instructions should include components and specific functionalities. YOUR RESPONSE SHOULD INCLUDE NO CODE. I REPEAT NO CODE. The response should be an outline of the website functions. For example a response may look like this:

             React Cookbook Website Functionality Outline
             1. Home Page
             Header: A welcoming message or tagline for the cookbook website.
             Introduction Section: Brief overview of what the website offers.
             Featured Recipes: Display a few featured recipes with images and brief descriptions.
             Call to Action: Buttons or links to encourage visitors to explore recipes, learn more about the website, or contact the site owners.

             2. About Page
             Header: Title or tagline that introduces the About page.
             Website Description: Detailed description of the website’s purpose, history, and the team behind it.
             Call to Action: Buttons or links to navigate to the recipes page or contact page.

             3. Contact Page
             Header: Title or tagline that introduces the Contact page.
             Contact Form: Form with fields for name, email, subject, and message.
             Contact Information: Display email, phone number, and physical address if applicable.
             Social Media Links: Icons or links to social media profiles.
             Map: Embedded map showing the location if relevant.

             4. Recipes Page
             Header: Title or tagline that introduces the Recipes page.
             Cuisines List: Grid or list of cuisine categories (e.g., Italian, Mexican, Chinese) with images.
             Cuisine Navigation: Clickable elements that lead to individual cuisine pages.

             5. Individual Cuisine Pages
             Header: Title or tagline for the specific cuisine.
             Dishes List: Grid or list of dishes under the selected cuisine with images and brief descriptions.
             Dish Navigation: Clickable elements that lead to individual dish pages.

             6. Individual Dish Pages
             Header: Title or tagline for the specific dish.
             Recipe Details: Detailed recipe including ingredients, steps, cooking time, and serving size.
             Images: Photos of the dish at various stages of preparation and the final result.
             Call to Action: Buttons or links to navigate back to the cuisine page or the main recipes page.

             7. Navbar
             Navigation Links: Links to Home, About, Contact, and Recipes pages.
             Dropdown Menus: If necessary, for sub-categories like different cuisines under the Recipes link.
             Search Bar: Optionally, include a search bar to quickly find recipes or other content.
             """},
            {"role": "user", "content": simple_instruction}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print(f"An error occurred while generating functionality instructions: {e}")
        return ""

def generate_design_instructions_prompt(simple_instruction):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
             "content": """
             Given the following simple instruction, generate detailed instructions for the design of the website: The detailed instructions should include themes, styling, and design elements. The design should be modern, visually appealing, and professional. Make sure that the text and body of each page is also visually appealing and professional. Text should follow the theme, and you should state in the design how the text should be formatted on different pages. Use Tailwind CSS for styling. YOUR RESPONSE SHOULD INCLUDE NO CODE. I REPEAT NO CODE. The response should be an outline of the website design. For example a response may look like this:

             React Cookbook Website Design Outline
             1. Design Theme
             Color Scheme: Light green and white theme throughout the entire website.
             Typography: Clean and readable fonts, consistent across all pages.
             Buttons: All buttons should be styled consistently and have clear purposes. No button should be without a specified action.
             Responsive Design: The website should be responsive, adjusting layout appropriately for different screen sizes (desktop, tablet, mobile).

             2. Home Page
             Consistent Styling: The home page should follow the light green and white theme, with clean and readable typography.
             Header: Styled with a welcoming message or tagline for the cookbook website.
             Introduction Section: Brief overview of what the website offers, styled with images and brief descriptions.

             3. About Page
             Consistent Styling: The about page should follow the light green and white theme, with clean and readable typography.
             Header: Title or tagline that introduces the About page, styled consistently.
             Images: Photos related to the team or the website's journey, styled with appropriate spacing and layout.

             4. Contact Page
             Consistent Styling: The contact page should follow the light green and white theme, with clean and readable typography.
             Header: Title or tagline that introduces the Contact page, styled consistently.
             Contact Form: Styled form fields for name, email, subject, and message.
             Contact Information: Display email, phone number, and physical address if applicable, styled consistently.
             Social Media Links: Icons or links to social media profiles, styled appropriately.
             Map: Embedded map showing the location if relevant, styled with appropriate size and layout.

             5. Recipes Page
             Consistent Styling: The recipes page should follow the light green and white theme, with clean and readable typography.
             Header: Title or tagline that introduces the Recipes page, styled consistently.
             Cuisines List: Grid or list of cuisine categories (e.g., Italian, Mexican, Chinese) with images, styled appropriately.

             6. Individual Cuisine Pages
             Consistent Styling: The individual cuisine pages should follow the light green and white theme, with clean and readable typography.
             Header: Title or tagline for the specific cuisine, styled consistently.
             Dishes List: Grid or list of dishes under the selected cuisine with images and brief descriptions, styled appropriately.

             7. Individual Dish Pages
             Consistent Styling: The individual dish pages should follow the light green and white theme, with clean and readable typography.
             Header: Title or tagline for the specific dish, styled consistently.
             Recipe Details: Detailed recipe including ingredients, steps, cooking time, and serving size, styled appropriately.
             Images: Photos of the dish at various stages of preparation and the final result, styled with appropriate spacing and layout.

             8. Navbar
             Consistent Styling: The navbar should follow the light green and white theme, with consistent styling across all pages.
             Navigation Links: Styled links to Home, About, Contact, and Recipes pages.
             Dropdown Menus: If necessary, for sub-categories like different cuisines under the Recipes link, styled appropriately.
             Search Bar: Optionally, include a styled search bar to quickly find recipes or other content.

             9. Footer
             Consistent Styling: The footer should follow the light green and white theme, with consistent styling across all pages.
             Links: Quick links to important pages (Home, About, Contact, Recipes), styled appropriately.
             Social Media Icons: Links to social media profiles, styled with appropriate icons.
             Copyright Information: Legal information and site credits, styled consistently.
             """},
            {"role": "user", "content": simple_instruction}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print(f"An error occurred while generating design instructions: {e}")
        return ""


def infer_components_prompt(detailed_instructions):
    client = OpenAI()
    try:
        messages = [
            {"role": "system",
             "content": "Given the following description, list the components and their purpose: Be sure to look for themes and colors for CSS files in the instructions. List the components in the format: ComponentName: ComponentDescription. Do not put parenthesis around ComponentName. Ensure the ComponentName is a single word and describe the component with an emphasis on visual appeal and modern design."},
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
    functionality_instructions = generate_functionality_instructions_prompt(simple_instruction)
    design_instructions = generate_design_instructions_prompt(simple_instruction)

    asked_questions_functionality = set()
    asked_questions_design = set()

    # Validate and refine functionality instructions
    for _ in range(2):
        validation_result_functionality = validate_information(functionality_instructions)
        if "all necessary components and functionalities are covered" in validation_result_functionality:
            break

        questions_functionality = [q for q in validation_result_functionality.split('\n\n')[:10] if q not in asked_questions_functionality]
        if not questions_functionality:
            break

        for question in questions_functionality:
            print(f"Please answer the following question to provide more details:\n{question}")
            additional_info = input("Your answer: ")
            functionality_instructions += f"\n{question}\nAnswer: {additional_info}"
            asked_questions_functionality.add(question)

    # Validate and refine design instructions
    for _ in range(2):
        validation_result_design = validate_information(design_instructions)
        if "all necessary components and functionalities are covered" in validation_result_design:
            break

        questions_design = [q for q in validation_result_design.split('\n\n')[:10] if q not in asked_questions_design]
        if not questions_design:
            break

        for question in questions_design:
            print(f"Please answer the following question to provide more details:\n{question}")
            additional_info = input("Your answer: ")
            design_instructions += f"\n{question}\nAnswer: {additional_info}"
            asked_questions_design.add(question)

    return functionality_instructions, design_instructions


def create_component_files(component_name, instructions, project_path):
    # Generate JSX code with Tailwind CSS classes
    component_jsx_code = generate_code_react(instructions['jsx'])

    component_css_code = ""

    component_dir = os.path.join(project_path, 'src', 'components', component_name)
    os.makedirs(component_dir, exist_ok=True)

    with open(os.path.join(component_dir, f'{component_name}.jsx'), 'w') as f:
        f.write(component_jsx_code)
    if component_css_code:
        with open(os.path.join(component_dir, f'{component_name}.css'), 'w') as f:
            f.write(component_css_code)


def create_react_app(name, components_instructions, detailed_instructions):
    try:
        base_path = os.getenv('JARVIS_PROJECTS_PATH', '/Users/krishsarin/Downloads/jarvis_test')
        project_path = os.path.join(base_path, name)

        subprocess.run(["npx", "create-react-app", name], cwd=base_path, check=True)
        subprocess.run(["npm", "install", "react-router-dom", "tailwindcss", "postcss", "autoprefixer", "react-icons"], cwd=project_path, check=True)

        # Initialize Tailwind CSS
        subprocess.run(["npx", "tailwindcss", "init", "-p"], cwd=project_path, check=True)
        with open(os.path.join(project_path, 'tailwind.config.js'), 'w') as f:
            f.write("""
module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false,
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
            """)

        with open(os.path.join(project_path, 'src', 'index.css'), 'w') as f:
            f.write("""
@tailwind base;
@tailwind components;
@tailwind utilities;
            """)

        # Generate and save components
        for component_name, instruction in components_instructions.items():
            print(component_name)
            create_component_files(component_name, instruction, project_path)

        # Generate main App component with Tailwind CSS classes
        main_app_instructions = f"Generate a main App component for a React app with routes for components: {', '.join(components_instructions.keys())}. Use react-router-dom for routing and Tailwind CSS for styling. Ensure all import paths follow the pattern './components/ComponentName/ComponentName'."
        app_jsx_code = generate_code_react(main_app_instructions)
        app_css_code = ""

        with open(os.path.join(project_path, 'src', 'App.jsx'), 'w') as f:
            f.write(app_jsx_code)
        if app_css_code:
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
    simple_instruction = "I want to create a cookbook website. This website should have a home page, about page, contact page, and recipes page. The first three pages should be pretty generic but the recipes page should have several cuisines listed and then you can click on those cuisines to get different dishes from the clicked cuisine and then you can click on the dishes to get the recipes. The whole theme should be a light green and white color throughout the entire website. It should include a navbar to connect all the pages, and every button should work with a specified purpose. No button should have no instruction."

    functionality_instructions = generate_functionality_instructions_prompt(simple_instruction)
    design_instructions = generate_design_instructions_prompt(simple_instruction)

    # Generate component instructions
    components_prompt = infer_components_prompt(functionality_instructions)

    components = {}
    for line in components_prompt.split('\n'):
        if ':' in line:
            component_name, component_description = line.split(':', 1)
            components[component_name.strip()] = {
                'description': component_description.strip(),
                'jsx': f"Generate a {component_name.strip()} component. {component_description.strip()}. Ensure it matches the description exactly and uses Tailwind CSS classes. Do not include any CSS code in this file.",
                'css': f"Generate Tailwind CSS classes for the {component_name.strip()} component based on the following JSX code:\n{component_description.strip()}"
            }
    print(components)

    # Once all details are gathered, create the React app
    create_react_app("food_web2", components, f"{functionality_instructions}\n\n{design_instructions}")

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
