# SkillGraph-AI-
# SkillGraph AI

SkillGraph AI is a Streamlit-based skill gap analysis application that helps users understand the skills required for a selected career role.

The application compares a user's existing skills with role requirements, identifies missing skills, analyzes their prerequisites, and generates a structured learning path.

## Features

* Select a target career role
* Select existing skills
* Calculate skill coverage
* Identify missing skills
* Analyze skill prerequisites
* Generate a dependency-based learning path
* Visualize skill dependencies as an interactive graph
* View a summary of the skill gap

## How It Works

```text
User Skills
     |
     v
Select Target Role
     |
     v
Compare Required Skills
     |
     v
Identify Skill Gaps
     |
     v
Analyze Skill Dependencies
     |
     v
Generate Learning Path
     |
     v
Visualize Skill Graph
```
<img width="954" height="503" alt="image" src="https://github.com/user-attachments/assets/9ed46559-e6d9-4978-a770-d7d6ca2a6297" />


## Example

For a Backend Developer role, the application may identify dependencies such as:

```text
Java
  |
 OOP
  |
Spring Boot
  |
REST API
  |
Docker
  |
 AWS
```

If the user already knows Java and SQL, the application focuses the learning path on the remaining required skills and their prerequisites.

## Supported Roles

* Backend Developer
* Frontend Developer
* Data Scientist
* ML Engineer
* Cloud Engineer

## Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* NetworkX
* Plotly
* JSON

## Project Structure

```text
SkillGraph-AI/
├── app.py
├── skills.json
├── roles.json
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/SkillGraph-AI.git
```

Move into the project directory:

```bash
cd SkillGraph-AI
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## Data

The project uses JSON files to maintain the skill knowledge base.

`skills.json` contains:

* Skill names
* Skill categories
* Skill prerequisites

`roles.json` contains:

* Career roles
* Required skills for each role

This structure makes it easy to add new skills, dependencies, and career roles without changing the main application logic.

## Current Approach

The current version uses a rule-based dependency graph to identify skill gaps and generate the learning path.

NetworkX is used to represent skill relationships, while Plotly is used to visualize the dependency graph.

## Future Improvements

* Skill proficiency levels
* Custom skill input
* More career roles and skills
* Machine learning-based skill recommendations
* Resume-based skill extraction
* Job description analysis
* User progress tracking
* Persistent database storage
* Personalized learning recommendations

## Live Demo

Coming soon.

## License

This project is for educational and personal use.
