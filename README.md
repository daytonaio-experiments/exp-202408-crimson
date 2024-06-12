### Automating the Generation of Standardized Dev Environments

**Job to be Done:**

**When** automating the setup of reproducible development environments for various software projects,

**We want to** develop an AI system that can:

1. Extract relevant information from a Git repository and structure it into a standardized format, including details like programming languages used, dependency requirements, and other specifications.
2. Fine-tune a Small Language Model (SLM) to generate key reproducibility artifacts such as `devcontainer.json`, Dockerfiles, requirements files, Software Bill of Materials (SBOM), and README files from the standardized input.

**So that** software development teams can automatically generate comprehensive, reproducible environments that ensure the source code runs seamlessly on any computer without manual intervention or specialized knowledge in setting up complex configurations.

This solution will streamline and automate the creation of vital development artifacts, enhancing the reproducibility, consistency, and ease of setup for various software projects. This not only accelerates the development cycle but also significantly reduces the overhead associated with setting up development environments.

### Objectives

1. **Information Extraction:** Automatically extract relevant context from a Git repository and structure it into a standardized format.
2. **Artifact Generation:** Fine-tune a Small Language Model (SLM) to generate required reproducibility artifacts based on the extracted and standardized information.
    - **Model Selection:**
        - A suitable Small Language Model (SLM) will be chosen based on requirements.
    - **Dataset Creation:**
        - A diverse dataset containing examples of various Git repositories and their respective reproducibility artifacts will be compiled.
    - **Fine-Tuning Process:**
        - Fine-tune the SLM on the dataset for generating needed artefacts, at min. SLM for generating dev container json file. Maybe we can have a mix of experts for different file types (e.g. dockerfile).
3. **Testing:**
    - Define set criteria or quality acceptance criteria.
    - Define failover measures, e.g. standard template devcontainer file that we know it works.

### Non-Functional Requirements

- **Scalability:**
    - The system should scale to handle large repositories and numerous dependencies.
- **Performance:**
    - The information extraction and artifact generation processes should be optimized for speed and efficiency.
- **Usability:**
    - The system should have a user-friendly interface to input Git repository URLs and manage outputs.
- **Reliability:**
    - Ensure high reliability and accuracy in generating the required artifacts.
