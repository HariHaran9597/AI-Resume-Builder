from typing import Dict, List, Tuple
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter
import re

class JobAnalyzer:
    def __init__(self):
        # Load spaCy model for NER and keyword extraction
        self.nlp = spacy.load("en_core_web_sm")
        # Load sentence transformer model for semantic similarity
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills and technical terms from text using enhanced NLP techniques"""
        doc = self.nlp(text)
        skills = []
        
        # Common technical skills and programming languages
        tech_keywords = {
            'python', 'java', 'javascript', 'c++', 'ruby', 'php', 'sql', 'nosql',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'devops', 'ci/cd',
            'machine learning', 'artificial intelligence', 'data science',
            'agile', 'scrum', 'git', 'rest api', 'graphql'
        }
        
        # Extract named entities that might be skills
        for ent in doc.ents:
            if ent.label_ in ["PRODUCT", "ORG", "GPE", "WORK_OF_ART"]:
                skills.append(ent.text)
        
        # Extract noun phrases as potential skills
        for chunk in doc.noun_chunks:
            if not any(char.isdigit() for char in chunk.text):  # Filter out numbers
                skills.append(chunk.text)
        
        # Look for technical keywords
        text_lower = text.lower()
        for keyword in tech_keywords:
            if keyword in text_lower:
                skills.append(keyword)
        
        # Clean and deduplicate skills
        cleaned_skills = []
        seen = set()
        for skill in skills:
            skill_clean = skill.lower().strip()
            # Remove very short skills and common words
            if len(skill_clean) > 2 and skill_clean not in seen:
                seen.add(skill_clean)
                cleaned_skills.append(skill_clean)
        
        return cleaned_skills
    
    def analyze_job_description(self, job_description: str) -> Dict:
        """Analyze job description to extract key information"""
        doc = self.nlp(job_description)
        
        # Extract skills
        skills = self.extract_skills(job_description)
        
        # Extract key requirements
        requirements = [sent.text.strip() for sent in doc.sents
                      if any(keyword in sent.text.lower()
                          for keyword in ["required", "must have", "requirements",
                                        "qualifications", "experience"])]
        
        return {
            "skills": skills,
            "requirements": requirements
        }
    
    def analyze_formatting(self, resume_text: str) -> Dict:
        """Analyze resume formatting and structure"""
        # Check for common formatting issues
        formatting_issues = []
        
        # Check for inconsistent bullet points
        bullet_points = re.findall(r'[•\-\*]\s.*', resume_text)
        bullet_chars = [point[0] for point in bullet_points]
        if len(set(bullet_chars)) > 1:
            formatting_issues.append("Inconsistent bullet point characters detected")
        
        # Check for section headers
        common_sections = ["summary", "experience", "education", "skills", "projects"]
        missing_sections = []
        for section in common_sections:
            if not re.search(rf"\b{section}\b", resume_text.lower()):
                missing_sections.append(section)
        
        # Check for date formatting
        dates = re.findall(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}\b|\d{1,2}/\d{4}|\d{4}', resume_text)
        date_formats = Counter([len(date) for date in dates])
        if len(date_formats) > 1:
            formatting_issues.append("Inconsistent date formatting detected")
        
        return {
            "formatting_issues": formatting_issues,
            "missing_sections": missing_sections,
            "bullet_points_count": len(bullet_points)
        }

    def calculate_ats_score(self, resume_text: str, job_description: str) -> float:
        """Calculate ATS optimization score based on various factors"""
        formatting_analysis = self.analyze_formatting(resume_text)
        
        # Base score starts at 100
        score = 100.0
        
        # Deduct points for formatting issues
        score -= len(formatting_analysis["formatting_issues"]) * 5
        score -= len(formatting_analysis["missing_sections"]) * 3
        
        # Analyze keyword density
        job_keywords = set(self.extract_skills(job_description))
        resume_keywords = set(self.extract_skills(resume_text))
        keyword_match_ratio = len(resume_keywords.intersection(job_keywords)) / len(job_keywords) if job_keywords else 1
        
        # Factor in keyword matches
        score *= (0.7 + 0.3 * keyword_match_ratio)
        
        return max(0, min(100, score))

    def calculate_match_score(self, resume_text: str, job_description: str) -> Tuple[float, Dict]:
        """Calculate match score between resume and job description"""
        # Get embeddings for resume and job description
        resume_embedding = self.model.encode([resume_text])
        job_embedding = self.model.encode([job_description])
        
        # Calculate similarity score
        similarity_score = cosine_similarity(resume_embedding, job_embedding)[0][0]
        
        # Analyze job requirements
        job_analysis = self.analyze_job_description(job_description)
        resume_skills = self.extract_skills(resume_text)
        
        # Calculate skill match
        matching_skills = [skill for skill in resume_skills
                         if any(job_skill in skill.lower()
                             for job_skill in job_analysis["skills"])]
        
        analysis = {
            "matching_skills": matching_skills,
            "missing_skills": [skill for skill in job_analysis["skills"]
                              if skill not in matching_skills],
            "key_requirements": job_analysis["requirements"]
        }
        
        # Calculate ATS optimization score
        ats_score = self.calculate_ats_score(resume_text, job_description)
        formatting_analysis = self.analyze_formatting(resume_text)
        
        # Add ATS and formatting analysis to the results
        analysis["ats_score"] = ats_score
        analysis["formatting_analysis"] = formatting_analysis
        
        return similarity_score, analysis