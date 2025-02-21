from typing import Dict, List
import spacy
from sentence_transformers import SentenceTransformer
from collections import defaultdict

class ResumeOptimizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    def generate_skill_suggestions(self, missing_skill: str) -> str:
        """Generate context-aware suggestions for incorporating missing skills"""
        suggestions = {
            'machine learning': "Consider adding a project where you applied ML models, e.g., 'Developed an XGBoost-based prediction system with 95% accuracy'",
            'python': "Highlight Python projects or automation scripts, e.g., 'Built data processing pipeline using Python that reduced processing time by 60%'",
            'sql': "Showcase database experience, e.g., 'Optimized SQL queries resulting in 40% faster data retrieval'",
            'aws': "Demonstrate cloud expertise, e.g., 'Architected serverless applications on AWS, reducing operational costs by 30%'",
            'docker': "Include containerization experience, e.g., 'Containerized microservices using Docker, improving deployment efficiency by 50%'"
        }
        
        # Default suggestion template if specific skill not found
        default_template = f"Consider adding practical experience with {missing_skill}, e.g., 'Implemented {missing_skill} solutions that improved process efficiency'"
        
        return suggestions.get(missing_skill.lower(), default_template)

    def improve_bullet_point(self, bullet_point: str) -> str:
        """Improve bullet points with stronger action verbs and quantifiable metrics"""
        doc = self.nlp(bullet_point)
        
        # Check if bullet point starts with a weak verb
        weak_verbs = {'worked', 'helped', 'assisted', 'participated', 'involved'}
        strong_verbs = {
            'worked': 'spearheaded',
            'helped': 'facilitated',
            'assisted': 'coordinated',
            'participated': 'led',
            'involved': 'executed'
        }
        
        words = bullet_point.split()
        if words and words[0].lower() in weak_verbs:
            words[0] = strong_verbs[words[0].lower()]
            bullet_point = ' '.join(words)
        
        # Add metrics if none present
        has_numbers = any(token.like_num for token in doc)
        if not has_numbers:
            bullet_point += " resulting in 20% improvement in efficiency"
        
        return bullet_point

    def analyze_section(self, section_text: str, job_description: str) -> Dict:
        """Analyze a resume section and provide improvement suggestions"""
        doc = self.nlp(section_text)
        job_doc = self.nlp(job_description)
        
        suggestions = []
        impact_words = {
            'achieved', 'improved', 'increased', 'decreased', 'reduced',
            'developed', 'implemented', 'created', 'designed', 'led',
            'managed', 'coordinated', 'streamlined', 'optimized'
        }
        
        # Check for quantifiable achievements
        has_metrics = any(token.like_num for token in doc)
        if not has_metrics:
            suggestions.append("Add specific metrics or quantifiable achievements")
        
        # Check for action verbs
        has_impact_words = any(token.text.lower() in impact_words for token in doc)
        if not has_impact_words:
            suggestions.append("Use more impactful action verbs")
        
        # Check for alignment with job description
        job_keywords = set(token.text.lower() for token in job_doc if token.pos_ in ['NOUN', 'PROPN'])
        section_keywords = set(token.text.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN'])
        
        missing_keywords = job_keywords - section_keywords
        if missing_keywords:
            suggestions.append(f"Consider incorporating relevant keywords: {', '.join(list(missing_keywords)[:5])}")
        
        # Improve bullet points
        bullet_points = [line.strip() for line in section_text.split('\n') if line.strip().startswith(('•', '-', '*'))]
        improved_bullets = []
        
        for bullet in bullet_points:
            improved_bullet = self.improve_bullet_point(bullet)
            if improved_bullet != bullet:
                improved_bullets.append({
                    'original': bullet,
                    'improved': improved_bullet
                })
        
        # Generate skill-specific suggestions
        skill_suggestions = []
        for keyword in missing_keywords:
            suggestion = self.generate_skill_suggestions(keyword)
            if suggestion:
                skill_suggestions.append(suggestion)
        
        return {
            "suggestions": suggestions,
            "section_strength": len(suggestions) == 0,
            "improved_bullets": improved_bullets,
            "skill_suggestions": skill_suggestions[:3]  # Limit to top 3 suggestions
        }
    
    def optimize_resume(self, resume_sections: Dict[str, str], job_description: str) -> Dict:
        """Analyze and provide suggestions for each resume section"""
        optimization_results = {}
        
        for section_name, content in resume_sections.items():
            if content.strip():
                analysis = self.analyze_section(content, job_description)
                optimization_results[section_name] = analysis
        
        return optimization_results