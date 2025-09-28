# Jurisai Crew

Welcome to the Jurisai Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/jurisai/config/agents.yaml` to define your agents
- Modify `src/jurisai/config/tasks.yaml` to define your tasks
- Modify `src/jurisai/crew.py` to add your own logic, tools and specific args
- Modify `src/jurisai/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the jurisai Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The jurisai Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Jurisai Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.


# JurisAI - AI Legal Assistant

A collaborative AI solution empowering lawyers to review and research cases faster, draft smarter, and advise with precision. JurisAI also enables citizens to seek legal advice through an intelligent AI assistant.

## Features

- **Multi-Agent Legal Research**: Specialized AI agents for different legal domains
- **Document Analysis**: Contract review and legal document processing
- **Citizen Legal Guidance**: Accessible legal advice for everyday citizens
- **Lawyer Collaboration**: Seamless handoff between AI and human lawyers
- **AWS Integration**: Built on AWS Bedrock, Lambda, and other AWS services

## Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/iankisali/jurisai.git
cd jurisai
```

2. **Install dependencies**
```bash
pip install -e .
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your AWS credentials and API keys
```

4. **Run JurisAI**
```bash
python src/jurisai/main.py
```

## Project Structure

```
Jurisai/
├── .gitignore
├── knowledge/              # Knowledge base files
├── pyproject.toml         # Project dependencies
├── README.md              # This file
├── .env                   # Environment variables
└── src/
    └── jurisai/
        ├── __init__.py
        ├── main.py        # Entry point
        ├── crew.py        # Crew orchestration
        ├── tools/         # Custom tools
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml    # Agent definitions
            └── tasks.yaml     # Task definitions
```

## AWS Setup

1. Configure AWS credentials
2. Enable Amazon Bedrock access
3. Set up required AWS services (Lambda, S3, DynamoDB)

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/
```

## License

MIT License - see LICENSE file for details.
