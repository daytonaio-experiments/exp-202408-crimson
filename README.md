# ⚠️THIS IS THE EXPERIMENTAL BRANCH⚠️
# Automated Generation of Standardized Development Environments

### Overview

This project aims to automate the setup of reproducible development environments for various software projects. By leveraging AI, we can extract relevant information from Git repositories and generate key reproducibility artifacts, ensuring that software runs seamlessly on any computer without manual intervention.

### Objectives

1. **Information Extraction:** 
    - Automatically extract relevant context from a Git repository, including details like programming languages used, dependency requirements, and other specifications.
2. **Artifact Generation:** 
    - Utilize machine learning (ML) to generate required reproducibility artifacts such as `devcontainer.json`, Dockerfiles, requirements files, Software Bill of Materials (SBOM), and README files based on the extracted information.
### Job to be Done

**When** automating the setup of reproducible development environments for various software projects,

**We want to** develop an AI system that can:

1. Extract relevant information from a Git repository and structure it into a standardized format.
2. Generate key reproducibility artifacts from the standardized input using a fine-tuned SLM.

**So that** software development teams can automatically generate comprehensive, reproducible environments that ensure the source code runs seamlessly on any computer.

### Non-Functional Requirements

- **Scalability:**
    - The system should handle large repositories and numerous dependencies.
- **Performance:**
    - Optimize information extraction and artifact generation processes for speed and efficiency.
- **Usability:**
    - Provide a user-friendly interface for inputting Git repository URLs and managing outputs.
- **Reliability:**
    - Ensure high reliability and accuracy in generating the required artifacts.

### System Architecture

```mermaid
graph TD
    A[User Input Git Repository URL] -->|Streamlit| B[Clone Repository]
    B -->|GitPython| C[Extract Repository Details]
    C -->|os, subprocess| D[Detect Primary Language]
    D -->|os| E[Find Dependency Files]
    E -->|GitPython| F[Extract Project Name and Author]
    F -->|AzureOpenAI| G{Generate Artifacts}
    G --> H[Generate devcontainer.json]
    G --> I[Generate Dockerfile]
    G --> J[Generate requirements.txt]
    G --> K[Generate SBOM]
    G --> L[Generate README.md]
    H -->|os| M[Save devcontainer.json]
    I -->|os| N[Save Dockerfile]
    J -->|os| O[Save requirements.txt]
    K -->|os| P[Save SBOM]
    L -->|os| Q[Save README.md]
    M --> R[User Downloads or Reviews Artifacts]
    N --> R
    O --> R
    P --> R
    Q --> R
```