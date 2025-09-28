import os
from typing import Dict, Any, Optional
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_aws import ChatBedrock
import boto3
import yaml
from dotenv import load_dotenv

from .tools.custom_tool import LegalResearchTool, DocumentAnalysisTool

# Load environment variables
load_dotenv()

@CrewBase
class JurisAICrew():
    """JurisAI Crew for legal assistance and research"""
    
    # Configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        self.setup_llm()
        self.setup_tools()
    
    def setup_llm(self):
        """Initialize AWS Bedrock LLM using LiteLLM"""
        try:
            # Configure LiteLLM environment variables
            os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID', '')
            os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY', '')
            os.environ['AWS_DEFAULT_REGION'] = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
            
            # Set the model name for LiteLLM
            model_name = os.getenv('BEDROCK_MODEL_ID', 'us.amazon.nova-lite-v1:0')
            self.litellm_model = f"bedrock/{model_name}"
            
            # Test LiteLLM connection
            from litellm import completion
            test_response = completion(
                model=self.litellm_model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
                temperature=0.1
            )
            
            # If test succeeds, set up the LLM for CrewAI
            self.llm = self.litellm_model
            print("✅ AWS Bedrock LLM initialized successfully with LiteLLM")
            
        except Exception as e:
            print(f"⚠️ Error initializing Bedrock LLM: {e}")
            print("Falling back to OpenAI (ensure OPENAI_API_KEY is set)")
            self.setup_openai_fallback()
    
    def setup_openai_fallback(self):
        """Setup OpenAI as fallback LLM using LiteLLM"""
        try:
            # Set OpenAI API key for LiteLLM
            os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
            
            # Use LiteLLM model string for OpenAI
            self.llm = "gpt-4o-mini"
            print("✅ OpenAI LLM initialized as fallback with LiteLLM")
            
        except Exception as e:
            print(f"❌ Error initializing OpenAI fallback: {e}")
            self.llm = None
    
    def setup_tools(self):
        """Initialize custom tools"""
        self.legal_research_tool = LegalResearchTool()
        self.document_analysis_tool = DocumentAnalysisTool()
        print("✅ Custom tools initialized")

    @agent
    def legal_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['legal_researcher'],
            llm=self.llm,
            tools=[self.legal_research_tool],
            verbose=True
        )

    @agent  
    def document_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['document_analyst'],
            llm=self.llm,
            tools=[self.document_analysis_tool],
            verbose=True
        )

    @agent
    def legal_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['legal_advisor'],
            llm=self.llm,
            tools=[],
            verbose=True
        )

    @agent
    def client_intake(self) -> Agent:
        return Agent(
            config=self.agents_config['client_intake'],
            llm=self.llm,
            tools=[],
            verbose=True
        )

    @task
    def legal_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['legal_research_task'],
            agent=self.legal_researcher()
        )

    @task
    def document_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['document_analysis_task'],
            agent=self.document_analyst()
        )

    @task
    def legal_advice_task(self) -> Task:
        return Task(
            config=self.tasks_config['legal_advice_task'],
            agent=self.legal_advisor()
        )

    @task
    def client_intake_task(self) -> Task:
        return Task(
            config=self.tasks_config['client_intake_task'],
            agent=self.client_intake()
        )

    @crew
    def crew(self) -> Crew:
        """Create the JurisAI crew with all agents and tasks"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            planning=True
        )

class JurisAIOrchestrator:
    """Main orchestrator for JurisAI operations"""
    
    def __init__(self):
        self.crew_instance = JurisAICrew()
        print("🚀 JurisAI Orchestrator initialized")
    
    def process_legal_query(
        self, 
        query: str, 
        client_type: str = "citizen",
        jurisdiction: str = "federal"
    ) -> Dict[str, Any]:
        """
        Process a legal query through the appropriate workflow
        
        Args:
            query: The legal question or issue
            client_type: Type of client (citizen, lawyer, business)
            jurisdiction: Legal jurisdiction (federal, state, etc.)
        
        Returns:
            Processed response with legal research and advice
        """
        try:
            print(f"📋 Processing legal query: {query[:100]}...")
            
            # Prepare inputs for the crew
            inputs = {
                'legal_query': query,
                'client_query': query,
                'client_type': client_type,
                'jurisdiction': jurisdiction,
                'client_situation': f"Client ({client_type}) has asked: {query}",
                'research_results': 'Legal research will be conducted',
                'document_analysis': 'No document analysis required for this query'
            }
            
            # Create a targeted crew for legal queries (research + advice only)
            legal_query_crew = Crew(
                agents=[self.crew_instance.legal_researcher(), self.crew_instance.legal_advisor()],
                tasks=[self.crew_instance.legal_research_task(), self.crew_instance.legal_advice_task()],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the targeted crew
            result = legal_query_crew.kickoff(inputs=inputs)
            
            print("✅ Legal query processed successfully")
            return {
                'status': 'success',
                'result': result,
                'client_type': client_type,
                'query': query
            }
            
        except Exception as e:
            print(f"❌ Error processing legal query: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'query': query
            }
    
    def analyze_document(
        self, 
        document_content: str, 
        analysis_focus: str = "general",
        client_type: str = "citizen"
    ) -> Dict[str, Any]:
        """
        Analyze a legal document
        
        Args:
            document_content: The text content of the document
            analysis_focus: Type of analysis (general, risk, contract, etc.)
            client_type: Type of client requesting analysis
        
        Returns:
            Document analysis results
        """
        try:
            print(f"📄 Analyzing document (focus: {analysis_focus})")
            
            # Prepare inputs for document analysis
            inputs = {
                'document_content': document_content,
                'analysis_focus': analysis_focus,
                'client_type': client_type
            }
            
            # For document analysis, we'll use a simplified workflow
            # focusing on the document analysis task
            document_crew = Crew(
                agents=[self.crew_instance.document_analyst(), self.crew_instance.legal_advisor()],
                tasks=[self.crew_instance.document_analysis_task(), self.crew_instance.legal_advice_task()],
                process=Process.sequential,
                verbose=True
            )
            
            # Add additional inputs for legal advice task
            inputs.update({
                'research_results': 'Document analysis focused',
                'document_analysis': 'Analyzing provided document',
                'client_situation': f'Document analysis requested by {client_type}'
            })
            
            result = document_crew.kickoff(inputs=inputs)
            
            print("✅ Document analysis completed")
            return {
                'status': 'success',
                'result': result,
                'analysis_focus': analysis_focus,
                'client_type': client_type
            }
            
        except Exception as e:
            print(f"❌ Error analyzing document: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'analysis_focus': analysis_focus
            }