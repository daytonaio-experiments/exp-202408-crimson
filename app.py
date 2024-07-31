import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import git
import json
import subprocess
import streamlit as st

# Load environment variables from .env file
load_dotenv()


# Function to check if necessary environment variables are set
def check_env_vars():
    required_vars = ['AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        st.error(f"Missing environment variables: {', '.join(missing_vars)}. Please configure the .env file properly.")
        return False
    return True


# Initialize the AzureOpenAI client
openai = AzureOpenAI(
    api_version='2024-06-01',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY')
)


# Function to clone a Git repository
def clone_repo(repo_url, clone_dir='cloned_repo'):
    if os.path.exists(clone_dir):
        subprocess.run(['rm', '-rf', clone_dir])
    os.makedirs(clone_dir, exist_ok=True)
    git.Repo.clone_from(repo_url, clone_dir)
    return clone_dir


# Function to detect the primary language used in the repository
def detect_primary_language(clone_dir):
    lang_count = {}
    for root, _, files in os.walk(clone_dir):
        for file in files:
            if file.endswith(('.py', '.js', '.java', '.cpp', '.rb', '.go', '.php', '.cs')):
                lang = file.split('.')[-1]
                lang_count[lang] = lang_count.get(lang, 0) + 1
    if lang_count:
        return max(lang_count, key=lang_count.get)
    return None


# Function to find the dependency file based on the detected language
def find_dependency_file(clone_dir, language):
    dep_files = {
        'py': 'requirements.txt',
        'js': 'package.json',
        'java': 'pom.xml',
        'cpp': 'CMakeLists.txt',
        'rb': 'Gemfile',
        'go': 'go.mod',
        'php': 'composer.json',
        'cs': 'packages.config'
    }
    return os.path.join(clone_dir, dep_files.get(language, ''))


# Function to extract repository details such as project name, description, language, dependencies, and author
def extract_repo_details(clone_dir):
    details = {
        'project_name': '',
        'description': '',
        'language': '',
        'dependencies': [],
        'author': '',
    }

    readme_path = os.path.join(clone_dir, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as file:
            details['description'] = file.readline().strip()

    repo = git.Repo(clone_dir)
    details['project_name'] = repo.remotes.origin.url.split('/')[-1].replace('.git', '')
    try:
        details['author'] = repo.git.log('-1', '--pretty=format:%an')
    except:
        details['author'] = 'Unknown'

    details['language'] = detect_primary_language(clone_dir)

    dependency_file_path = find_dependency_file(clone_dir, details['language'])
    if os.path.exists(dependency_file_path):
        with open(dependency_file_path, 'r') as file:
            details['dependencies'] = file.read().splitlines()

    return details


# Function to generate a file using the OpenAI API based on a given prompt
def generate_file(prompt):
    response = openai.chat.completions.create(
        model='gpt-35-turbo-16k',
        messages=[
            {'role': 'system',
             'content': 'Return only the content of the file. Do not provide additional information.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    return response.choices[0].message.content.strip()


# Function to generate devcontainer.json based on project details
def generate_devcontainer(data):
    prompt = f'Generate devcontainer.json for a project with the following details: {json.dumps(data)}'
    return generate_file(prompt)


# Function to generate Dockerfile based on project details
def generate_dockerfile(data):
    prompt = f'Generate a Dockerfile for a project with the following details: {json.dumps(data)}'
    return generate_file(prompt)


# Function to generate requirements.txt based on project details
def generate_requirements(data):
    prompt = f'Generate requirements.txt for a project with the following details: {json.dumps(data)}'
    return generate_file(prompt)


# Function to generate SBOM (Software Bill of Materials) based on project details
def generate_sbom(data):
    prompt = f'Generate a Software Bill of Materials (SBOM) for a project with the following details: {json.dumps(data)}'
    return generate_file(prompt)


# Function to generate README.md based on project details
def generate_readme(data):
    prompt = f'Generate a README.md for a project with the following details: {json.dumps(data)}'
    return generate_file(prompt)


# Function to save content to a specified file in a specified directory
def save_to_file(directory, filename, content):
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as file:
        file.write(content)


# Function to process the repository by cloning it and extracting details
def process_repo(repo_url):
    clone_dir = clone_repo(repo_url)
    details = extract_repo_details(clone_dir)
    return details, clone_dir


# Function to generate selected files based on user choices and save them in the cloned repository directory
def generate_files(details, clone_dir, files_to_generate):
    if 'devcontainer' in files_to_generate:
        devcontainer_content = generate_devcontainer(details)
        save_to_file(clone_dir, 'devcontainer.json', devcontainer_content)

    if 'dockerfile' in files_to_generate:
        dockerfile_content = generate_dockerfile(details)
        save_to_file(clone_dir, 'Dockerfile', dockerfile_content)

    if 'requirements' in files_to_generate:
        requirements_content = generate_requirements(details)
        save_to_file(clone_dir, 'requirements.txt', requirements_content)

    if 'sbom' in files_to_generate:
        sbom_content = generate_sbom(details)
        save_to_file(clone_dir, 'SBOM.txt', sbom_content)

    if 'readme' in files_to_generate:
        readme_content = generate_readme(details)
        save_to_file(clone_dir, 'README.md', readme_content)

    return 'Selected files have been generated and saved.'


# Main function to create the Streamlit app
def main():
    st.title("Repository Processor and File Generator")

    # Check if the necessary environment variables are set
    if not check_env_vars():
        return

    repo_url = st.text_input("Enter the repository URL:")
    if st.button("Process Repository"):
        if repo_url:
            with st.spinner("Processing..."):
                details, clone_dir = process_repo(repo_url)
                st.success("Repository processed successfully!")
                st.session_state['details'] = details  # Store details in session state
                st.session_state['clone_dir'] = clone_dir  # Store clone directory in session state
                st.json(details)
        else:
            st.error("Please enter a repository URL.")

    if 'details' in st.session_state:
        st.header("Select files to generate:")
        files_to_generate = st.multiselect(
            "Choose files",
            ['devcontainer', 'dockerfile', 'requirements', 'sbom', 'readme']
        )

        if st.button("Generate Files"):
            if files_to_generate:
                with st.spinner("Generating files..."):
                    result = generate_files(st.session_state['details'], st.session_state['clone_dir'],
                                            files_to_generate)
                    st.success(result)
            else:
                st.error("Please select at least one file to generate.")


if __name__ == "__main__":
    main()
