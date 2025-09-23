#!/usr/bin/env python
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# Import orchestrator from package path for script entry points
from jurisai.crew import JurisAIOrchestrator

def main():
    """Deprecated: retained for direct script execution. Use run()."""
    run()

def run():
    """CLI entrypoint used by project scripts (run_crew/jurisai)."""
    print("🏛️ Welcome to JurisAI - Your AI Legal Assistant")
    print("=" * 60)

    orchestrator = JurisAIOrchestrator()

    print("Choose a mode:")
    print("1. Document analysis")
    print("2. Demo mode")
    print("3. Legal query")

    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        handle_document_analysis(orchestrator)
    elif choice == "2":
        demo_mode()
    elif choice == "3":
        query = input("Enter your legal question: ").strip()
        client_type = input("Client type (citizen/lawyer/business) [citizen]: ").strip() or "citizen"
        jurisdiction = input("Jurisdiction [federal]: ").strip() or "federal"
        result = orchestrator.process_legal_query(query=query, client_type=client_type, jurisdiction=jurisdiction)
        print("\n" + "=" * 60)
        if result['status'] == 'success':
            print("✅ Query processed successfully")
            print(str(result['result']))
        else:
            print(f"❌ Error: {result['error']}")
        print("=" * 60)
    else:
        print("Invalid choice. Exiting.")

def handle_document_analysis(orchestrator):
    """Handle document analysis interaction"""
    print("\n📄 Document Analysis Mode")
    print("-" * 25)
    
    print("Choose document input method:")
    print("1. Type/paste document content")
    print("2. Load from file (coming soon)")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        print("\nPaste your document content below (press Ctrl+D when done):")
        print("-" * 40)
        
        try:
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            
            document_content = "\n".join(lines)
            
            if not document_content.strip():
                print("No document content provided.")
                return
                
        except KeyboardInterrupt:
            print("\nDocument input cancelled.")
            return
    
    elif choice == "2":
        print("File loading feature coming soon!")
        return
    
    else:
        print("Invalid choice.")
        return
    
    # Get analysis focus
    print("\nWhat type of analysis do you need?")
    print("1. General analysis")
    print("2. Contract review")
    print("3. Risk assessment")
    print("4. Compliance check")
    
    analysis_map = {
        "1": "general",
        "2": "contract", 
        "3": "risk",
        "4": "compliance"
    }
    
    analysis_choice = input("Enter choice (1-4): ").strip()
    analysis_focus = analysis_map.get(analysis_choice, "general")
    
    # Get client type
    client_type = input("Client type (citizen/lawyer/business) [citizen]: ").strip() or "citizen"
    
    print(f"\n🔍 Analyzing document...")
    print(f"Analysis Focus: {analysis_focus.title()}")
    print(f"Client Type: {client_type.title()}")
    
    # Process the document
    result = orchestrator.analyze_document(
        document_content=document_content,
        analysis_focus=analysis_focus,
        client_type=client_type
    )
    
    # Display results
    print("\n" + "="*60)
    print("📄 JURISAI DOCUMENT ANALYSIS")
    print("="*60)
    
    if result['status'] == 'success':
        print(result['result'])
    else:
        print(f"❌ Error: {result['error']}")
    
    print("="*60)

def demo_mode():
    """Run JurisAI in demo mode with sample queries"""
    print("\n🎬 JurisAI Demo Mode")
    print("=" * 25)
    
    orchestrator = JurisAIOrchestrator()
    
    # Demo legal queries
    demo_queries = [
        {
            "query": "My landlord won't return my security deposit after I moved out. What are my rights?",
            "client_type": "citizen",
            "jurisdiction": "federal"
        },
        {
            "query": "I need to review a non-compete clause in an employment contract.",
            "client_type": "lawyer", 
            "jurisdiction": "california"
        }
    ]
    
    # Demo document
    demo_document = """
    RENTAL AGREEMENT
    
    This agreement is between John Doe (Tenant) and ABC Properties (Landlord).
    
    1. Property: 123 Main Street, Anytown, State
    2. Term: 12 months starting January 1, 2024
    3. Rent: $1,500 per month, due on the 1st
    4. Security Deposit: $1,500
    5. Tenant is responsible for all utilities
    6. No pets allowed without written permission
    7. Landlord may enter with 24-hour notice
    """
    
    print("Running demo queries...")
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n--- Demo Query {i} ---")
        print(f"Query: {demo['query']}")
        print(f"Client: {demo['client_type']}")
        
        result = orchestrator.process_legal_query(**demo)
        
        if result['status'] == 'success':
            print("✅ Query processed successfully")
            print(f"Result: {str(result['result'])[:200]}...")
        else:
            print(f"❌ Error: {result['error']}")
    
    print("\n--- Document Analysis Demo ---")
    print("Analyzing sample rental agreement...")
    
    doc_result = orchestrator.analyze_document(
        document_content=demo_document,
        analysis_focus="contract",
        client_type="citizen"
    )
    
    if doc_result['status'] == 'success':
        print("✅ Document analyzed successfully")
        print(f"Result: {str(doc_result['result'])[:200]}...")
    else:
        print(f"❌ Error: {doc_result['error']}")

if __name__ == "__main__":
    # Check if running in demo mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mode()
    else:
        run()

# Additional script entry points referenced in pyproject.toml
def train():
    """Placeholder for training workflows (not implemented)."""
    print("Training pipeline is not implemented yet.")

def replay():
    """Placeholder for replaying previous runs (not implemented)."""
    print("Replay functionality is not implemented yet.")

def test():
    """Placeholder for running tests via script entry point."""
    print("Running tests...")
    # Delegate to pytest if available
    try:
        import pytest  # type: ignore
        raise SystemExit(pytest.main([str(Path(__file__).parent.parent.parent / 'tests')]))
    except ModuleNotFoundError:
        print("pytest not installed. Please install dev dependencies.")
