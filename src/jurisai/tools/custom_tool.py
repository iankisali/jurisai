import os
import boto3
from typing import Dict, Any, Optional
from crewai_tools import BaseTool
from pydantic import Field
import json

class LegalResearchTool(BaseTool):
    name: str = "Legal Research Tool"
    description: str = "Search legal databases for case law, statutes, and regulations"

    def _run(self, query: str, jurisdiction: str = "federal") -> str:
        """
        Perform legal research using various sources
        
        Args:
            query: Legal research query
            jurisdiction: Legal jurisdiction (federal, state, etc.)
        
        Returns:
            Research results as formatted string
        """
        try:
            # In a real implementation, this would connect to legal databases
            # For demo purposes, we'll simulate research results
            
            research_results = {
                "query": query,
                "jurisdiction": jurisdiction,
                "case_law": [
                    {
                        "case_name": "Sample v. Case (2023)",
                        "citation": "123 F.3d 456",
                        "summary": "Relevant case law summary based on query",
                        "relevance_score": 0.85
                    }
                ],
                "statutes": [
                    {
                        "title": "Relevant Statute Title",
                        "section": "§ 123.45",
                        "text": "Applicable statutory text...",
                        "jurisdiction": jurisdiction
                    }
                ],
                "analysis": f"Legal research analysis for: {query} in {jurisdiction} jurisdiction"
            }
            
            # Format results for agent consumption
            formatted_results = self._format_legal_research(research_results)
            return formatted_results
            
        except Exception as e:
            return f"Error performing legal research: {str(e)}"
    
    def _format_legal_research(self, results: Dict[str, Any]) -> str:
        """Format research results for agent consumption"""
        formatted = f"Legal Research Results for: {results['query']}\n"
        formatted += f"Jurisdiction: {results['jurisdiction']}\n\n"
        
        if results['case_law']:
            formatted += "RELEVANT CASE LAW:\n"
            for case in results['case_law']:
                formatted += f"- {case['case_name']} ({case['citation']})\n"
                formatted += f"  Summary: {case['summary']}\n"
                formatted += f"  Relevance: {case['relevance_score']:.2f}\n\n"
        
        if results['statutes']:
            formatted += "APPLICABLE STATUTES:\n"
            for statute in results['statutes']:
                formatted += f"- {statute['title']} {statute['section']}\n"
                formatted += f"  Text: {statute['text']}\n\n"
        
        formatted += f"Analysis: {results['analysis']}\n"
        return formatted

class DocumentAnalysisTool(BaseTool):
    name: str = "Document Analysis Tool"
    description: str = "Analyze legal documents for key terms, risks, and recommendations"
    
    def _run(self, document_content: str, analysis_type: str = "general") -> str:
        """
        Analyze legal document content
        
        Args:
            document_content: Text content of the document
            analysis_type: Type of analysis (general, contract, risk, etc.)
        
        Returns:
            Document analysis results
        """
        try:
            # In a real implementation, this would use AWS Textract, Comprehend, etc.
            # For demo purposes, we'll simulate document analysis
            
            analysis_results = {
                "document_type": self._identify_document_type(document_content),
                "key_terms": self._extract_key_terms(document_content),
                "risk_factors": self._identify_risks(document_content),
                "recommendations": self._generate_recommendations(document_content, analysis_type),
                "compliance_issues": self._check_compliance(document_content)
            }
            
            formatted_analysis = self._format_document_analysis(analysis_results)
            return formatted_analysis
            
        except Exception as e:
            return f"Error analyzing document: {str(e)}"
    
    def _identify_document_type(self, content: str) -> str:
        """Identify the type of legal document"""
        content_lower = content.lower()
        
        if "agreement" in content_lower or "contract" in content_lower:
            return "Contract/Agreement"
        elif "lease" in content_lower:
            return "Lease Agreement"
        elif "employment" in content_lower:
            return "Employment Document"
        elif "will" in content_lower or "testament" in content_lower:
            return "Will/Testament"
        else:
            return "General Legal Document"
    
    def _extract_key_terms(self, content: str) -> list:
        """Extract key terms from document"""
        # Simplified key term extraction
        key_terms = []
        
        # Look for common legal terms
        legal_keywords = ["party", "agreement", "contract", "liability", "damages", 
                         "termination", "breach", "obligation", "payment", "deadline"]
        
        for keyword in legal_keywords:
            if keyword in content.lower():
                key_terms.append(keyword.capitalize())
        
        return key_terms[:5]  # Return top 5 for demo
    
    def _identify_risks(self, content: str) -> list:
        """Identify potential legal risks"""
        risks = []
        content_lower = content.lower()
        
        risk_indicators = {
            "unlimited liability": "High",
            "no termination clause": "Medium", 
            "vague payment terms": "Medium",
            "missing dispute resolution": "Low",
            "broad indemnification": "High"
        }
        
        for risk, level in risk_indicators.items():
            if any(word in content_lower for word in risk.split()):
                risks.append({"risk": risk, "level": level})
        
        return risks
    
    def _generate_recommendations(self, content: str, analysis_type: str) -> list:
        """Generate recommendations based on analysis"""
        recommendations = [
            "Review all payment terms and deadlines carefully",
            "Consider adding a dispute resolution clause",
            "Clarify liability limitations where possible",
            "Ensure all parties' obligations are clearly defined"
        ]
        
        if analysis_type == "contract":
            recommendations.extend([
                "Add termination conditions and notice periods",
                "Include intellectual property protection clauses"
            ])
        
        return recommendations[:4]  # Return top 4 for demo
    
    def _check_compliance(self, content: str) -> list:
        """Check for basic compliance issues"""
        compliance_issues = []
        
        # Basic compliance checks
        if "signature" not in content.lower():
            compliance_issues.append("Missing signature requirements")
        
        if "date" not in content.lower():
            compliance_issues.append("Missing execution date")
        
        return compliance_issues
    
    def _format_document_analysis(self, results: Dict[str, Any]) -> str:
        """Format document analysis results"""
        formatted = f"DOCUMENT ANALYSIS RESULTS\n"
        formatted += f"Document Type: {results['document_type']}\n\n"
        
        if results['key_terms']:
            formatted += "KEY TERMS IDENTIFIED:\n"
            for term in results['key_terms']:
                formatted += f"- {term}\n"
            formatted += "\n"
        
        if results['risk_factors']:
            formatted += "RISK ASSESSMENT:\n"
            for risk in results['risk_factors']:
                formatted += f"- {risk['risk']} (Risk Level: {risk['level']})\n"
            formatted += "\n"
        
        if results['recommendations']:
            formatted += "RECOMMENDATIONS:\n"
            for i, rec in enumerate(results['recommendations'], 1):
                formatted += f"{i}. {rec}\n"
            formatted += "\n"
        
        if results['compliance_issues']:
            formatted += "COMPLIANCE ISSUES:\n"
            for issue in results['compliance_issues']:
                formatted += f"⚠️ {issue}\n"
        
        return formatted
