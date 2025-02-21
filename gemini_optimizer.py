import time
from typing import Dict, List
from google.generativeai import GenerativeModel
import google.generativeai as genai

class GeminiOptimizer:
    def __init__(self, api_key: str, max_retries: int = 3, initial_delay: float = 1.0):
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        self.model = GenerativeModel('gemini-pro')
        self.max_retries = max_retries
        self.initial_delay = initial_delay
    
    def _make_api_call_with_retry(self, prompt: str) -> str:
        """Make API call with exponential backoff retry logic"""
        delay = self.initial_delay
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                last_exception = e
                if '429' in str(e):  # Rate limit error
                    if attempt < self.max_retries - 1:  # Don't sleep on last attempt
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                    continue
                raise  # Re-raise non-rate-limit errors
        
        # If we get here, we've exhausted retries
        error_msg = f"API quota exceeded after {self.max_retries} retries. Please try again later."
        if last_exception:
            error_msg += f" Original error: {str(last_exception)}"
        raise Exception(error_msg)
    
    def improve_bullet_point(self, bullet_point: str, job_context: str) -> Dict[str, str]:
        """Improve a resume bullet point using Gemini's context-aware suggestions"""
        prompt = f"""
        Given this resume bullet point:
        "{bullet_point}"
        
        And this job context:
        "{job_context}"
        
        Please improve this bullet point to:
        1. Use stronger action verbs
        2. Include specific metrics and achievements
        3. Align better with the job requirements
        4. Make it more impactful and professional
        
        Return only the improved version.
        """
        
        try:
            improved = self._make_api_call_with_retry(prompt)
            return {
                'original': bullet_point,
                'improved': improved
            }
        except Exception as e:
            return {
                'original': bullet_point,
                'improved': bullet_point,
                'error': str(e)
            }
    
    def generate_skill_suggestions(self, missing_skill: str, job_description: str) -> str:
        """Generate context-aware suggestions for incorporating missing skills using Gemini"""
        prompt = f"""
        Given this missing skill from a resume: {missing_skill}
        And this job description: {job_description}
        
        Suggest a specific, practical way to demonstrate this skill in a resume bullet point.
        Focus on measurable achievements and real-world applications.
        """
        
        try:
            return self._make_api_call_with_retry(prompt)
        except Exception as e:
            return f"Consider adding practical experience with {missing_skill} in a measurable way"
    
    def analyze_section(self, section_text: str, job_description: str) -> Dict:
        """Analyze a resume section and provide AI-powered improvement suggestions"""
        prompt = f"""
        Analyze this resume section:
        "{section_text}"
        
        For this job description:
        "{job_description}"
        
        Provide:
        1. Specific suggestions for improvement
        2. Key missing keywords or skills
        3. Ways to make the content more impactful
        4. Alignment with job requirements
        
        Format the response as a JSON string with these keys:
        - suggestions: list of general improvements
        - missing_keywords: list of important missing terms
        - impact_suggestions: list of ways to increase impact
        """
        
        try:
            response_text = self._make_api_call_with_retry(prompt)
            if not response_text.startswith('{'): # Handle non-JSON responses
                return {
                    'suggestions': [response_text],
                    'skill_suggestions': [],
                    'improved_bullets': []
                }
            
            try:
                import json
                analysis = json.loads(response_text)
                # Structure the response in a more organized way
                return {
                    'key_improvements': ['• ' + item for item in analysis.get('suggestions', [])],
                    'missing_skills': ['• ' + skill for skill in analysis.get('missing_keywords', [])],
                    'impact_suggestions': ['• ' + suggestion for suggestion in analysis.get('impact_suggestions', [])],
                    'job_requirements': {
                        requirement: ('✓' if status else '✗')
                        for requirement, status in analysis.get('alignment_with_job_requirements', {}).items()
                    }
                }
            except Exception as e:
                return {
                    'suggestions': ["Error analyzing section: " + str(e)],
                    'skill_suggestions': [],
                    'improved_bullets': []
                }
        except Exception as e:
            return {
                'suggestions': ["Error analyzing section: " + str(e)],
                'skill_suggestions': [],
                'improved_bullets': []
            }

    def generate_professional_summary(self, resume_text: str, job_description: str) -> str:
        """Generate a professional summary section based on resume content and job requirements"""
        prompt = f"""
        Based on this resume content:
        "{resume_text}"
        
And this job description:
        "{job_description}"
        
Generate a compelling professional summary that:
        1. Highlights key qualifications and experience
        2. Aligns with the job requirements
        3. Includes relevant achievements and skills
        4. Is concise (3-4 sentences)
        
Format with markdown for emphasis on key points.
        """
        
        try:
            return self._make_api_call_with_retry(prompt)
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def optimize_resume(self, resume_sections: Dict[str, str], job_description: str) -> Dict[str, dict]:
        """Optimize resume sections using Gemini's AI capabilities"""
        results = {}
        
        for section_name, section_content in resume_sections.items():
            try:
                # Analyze the section and get improvement suggestions
                section_analysis = self.analyze_section(section_content, job_description)
                
                # Add the analysis results to the overall results
                results[section_name] = section_analysis
                
            except Exception as e:
                results[section_name] = {
                    'suggestions': [f"Error analyzing section: {str(e)}"],
                    'skill_suggestions': [],
                    'improved_bullets': []
                }
        
        return results
    
    def format_analysis_report(self, analysis_results: Dict) -> str:
        """Format analysis results into a professional markdown report"""
        report = ["# Resume Optimization Suggestions\n"]

        # Add overall assessment
        report.append("## Detailed Optimization Suggestions\n")
        report.append("### General Improvements:")
        for improvement in analysis_results.get('key_improvements', []):
            report.append(improvement)
        report.append("\n")

        # Add skills analysis
        report.append("### Missing Keywords and Skills:")
        for skill in analysis_results.get('missing_skills', []):
            report.append(skill)
        report.append("\n")

        # Add impact suggestions
        report.append("### Impact Enhancement Suggestions:")
        for suggestion in analysis_results.get('impact_suggestions', []):
            report.append(suggestion)
        report.append("\n")

        # Add job requirement alignment
        report.append("### Job Requirements Alignment:")
        for req, status in analysis_results.get('job_requirements', {}).items():
            icon = '✅' if status == '✓' else '❌'
            report.append(f"{icon} {req}")

        return '\n'.join(report)