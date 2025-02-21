import streamlit as st
import os
import plotly.express as px
import pandas as pd
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
from gemini_optimizer import GeminiOptimizer

# Initialize the analyzers
job_analyzer = JobAnalyzer()
gemini_optimizer = GeminiOptimizer(os.getenv('GEMINI_API_KEY'))

# Set page configuration
st.set_page_config(
    page_title="AI Resume Tailoring Tool",
    page_icon="📄",
    layout="wide"
)

# Main title and description
st.title("AI-Powered Resume Tailoring Tool 📄")
st.markdown("""
    Optimize your resume for ATS systems and job descriptions using AI technology.
    Upload your resume and job description to get started!
""")

# Create two columns for resume and job description uploads
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Your Resume")
    resume_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"]
    )

with col2:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200
    )

# Add analyze button
if st.button("Analyze Resume", type="primary"):
    if resume_file is None:
        st.error("Please upload your resume first!")
    elif not job_description:
        st.error("Please provide the job description!")
    else:
        with st.spinner("Analyzing your resume..."):
            # Get file type and content
            file_type = resume_file.name.split('.')[-1]
            file_content = resume_file.read()
            
            # Parse resume
            resume_text = ResumeParser.parse_resume(file_content, file_type)
            
            if resume_text:
                st.success("Resume parsed successfully!")
                
                # Generate professional summary
                summary = gemini_optimizer.generate_professional_summary(resume_text, job_description)
                
                # Display professional summary
                with st.expander("✨ AI-Generated Professional Summary", expanded=True):
                    st.markdown(summary)
                
                # Analyze resume and job description match
                similarity_score, analysis = job_analyzer.calculate_match_score(resume_text, job_description)
                
                # Display results
                st.subheader("Analysis Results")
                
                # Create columns for scores
                score_col1, score_col2 = st.columns(2)
                
                # Display match score with progress bar
                with score_col1:
                    st.metric("Resume-Job Match Score", f"{similarity_score * 100:.1f}%")
                    st.progress(float(similarity_score))
                
                # Display ATS optimization score
                with score_col2:
                    st.metric("ATS Optimization Score", f"{analysis['ats_score']:.1f}%")
                    st.progress(float(analysis['ats_score']) / 100)
                
                # Create skill visualization
                matching_skills = analysis.get('matching_skills', [])
                missing_skills = analysis.get('missing_skills', [])
                
                # Prepare data for visualization
                skill_data = pd.DataFrame({
                    'Skill': matching_skills + missing_skills,
                    'Status': ['Matched'] * len(matching_skills) + ['Missing'] * len(missing_skills),
                    'Count': [1] * (len(matching_skills) + len(missing_skills))
                })
                
                # Create bar chart
                fig = px.bar(
                    skill_data,
                    x='Status',
                    y='Count',
                    color='Status',
                    title='Skills Analysis',
                    labels={'Count': 'Number of Skills'},
                    color_discrete_map={'Matched': 'green', 'Missing': 'red'}
                )
                
                # Display chart
                st.plotly_chart(fig)
                
                # Display formatting analysis
                with st.expander("📋 Formatting Analysis"):
                    if analysis["formatting_analysis"]["formatting_issues"]:
                        st.error("Formatting Issues Found:")
                        for issue in analysis["formatting_analysis"]["formatting_issues"]:
                            st.write(f"• {issue}")
                    else:
                        st.success("No formatting issues found!")
                    
                    if analysis["formatting_analysis"]["missing_sections"]:
                        st.warning("Missing Sections:")
                        for section in analysis["formatting_analysis"]["missing_sections"]:
                            st.write(f"• {section.title()}")
                
                # Display skills analysis with suggestions in a card layout
                st.markdown("""
                    <style>
                    .skills-card {
                        padding: 1.5rem;
                        border-radius: 10px;
                        margin-bottom: 1rem;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    .matching-skills {
                        background-color: #E8F5E9;
                        border: 1px solid #81C784;
                    }
                    .missing-skills {
                        background-color: #FFEBEE;
                        border: 1px solid #E57373;
                    }
                    .suggestion-box {
                        background-color: #E3F2FD;
                        border: 1px solid #64B5F6;
                        padding: 0.8rem;
                        border-radius: 8px;
                        margin-top: 0.5rem;
                    }
                    </style>
                """, unsafe_allow_html=True)

                skill_col1, skill_col2 = st.columns(2)
                
                with skill_col1:
                    st.markdown('<div class="skills-card matching-skills">', unsafe_allow_html=True)
                    st.markdown("### ✅ Matching Skills")
                    for skill in matching_skills:
                        st.markdown(f"**•** {skill}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with skill_col2:
                    st.markdown('<div class="skills-card missing-skills">', unsafe_allow_html=True)
                    st.markdown("### ❌ Missing Skills")
                    for skill in missing_skills:
                        st.markdown(f"**•** {skill}")
                        suggestion = gemini_optimizer.generate_skill_suggestions(skill, job_description)
                        st.markdown(f'<div class="suggestion-box">💡 {suggestion}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Generate and display downloadable report
                report = gemini_optimizer.format_analysis_report(analysis)
                st.download_button(
                    label="📥 Download Analysis Report",
                    data=report,
                    file_name="resume_analysis_report.md",
                    mime="text/markdown"
                )
                
                # Display skills analysis
                skill_col1, skill_col2 = st.columns(2)
                
                with skill_col1:
                    st.write("✅ **Matching Skills:**")
                    if analysis["matching_skills"]:
                        for skill in analysis["matching_skills"]:
                            st.success(f"• {skill}")
                    else:
                        st.info("No direct skill matches found")
                
                with skill_col2:
                    st.write("❌ **Missing Skills:**")
                    if analysis["missing_skills"]:
                        for skill in analysis["missing_skills"]:
                            st.error(f"• {skill}")
                    else:
                        st.success("No missing skills identified")
                
                # Display key requirements
                with st.expander("View Key Requirements"):
                    for req in analysis["key_requirements"]:
                        st.write(f"• {req}")
                
                # Add resume optimization section
                st.subheader("Resume Optimization Suggestions")
                
                # Initialize resume optimizer
                from gemini_optimizer import GeminiOptimizer
                
                # Get Gemini API key from environment variable or Streamlit secrets
                gemini_api_key = os.getenv('GEMINI_API_KEY') or st.secrets.get('GEMINI_API_KEY')
                if not gemini_api_key:
                    st.warning("⚠️ Gemini API key not found. Some advanced AI features may be limited.")
                    resume_optimizer = ResumeOptimizer()
                else:
                    resume_optimizer = GeminiOptimizer(gemini_api_key)
                
                # Split resume into sections (simplified for now)
                resume_sections = {"content": resume_text}
                
                # Get optimization suggestions
                optimization_results = resume_optimizer.optimize_resume(resume_sections, job_description)
                
                # Display optimization suggestions with improved UI
                st.subheader("📝 Detailed Optimization Suggestions")
                
                for section_name, section_analysis in optimization_results.items():
                    with st.expander(f"Suggestions for {section_name.title()}"):
                        # General suggestions
                        if section_analysis["suggestions"]:
                            st.write("General Improvements:")
                            for suggestion in section_analysis["suggestions"]:
                                st.info(f"• {suggestion}")
                        
                        # Skill-specific suggestions
                        if section_analysis.get("skill_suggestions"):
                            st.write("\n💡 How to Include Missing Skills:")
                            for suggestion in section_analysis["skill_suggestions"]:
                                st.write(f"• {suggestion}")
                        
                        # Improved bullet points
                        if section_analysis.get("improved_bullets"):
                            st.write("\n✍️ Suggested Bullet Point Improvements:")
                            for bullet in section_analysis["improved_bullets"]:
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("Before:")
                                    st.warning(bullet["original"])
                                with col2:
                                    st.write("After:")
                                    st.success(bullet["improved"])
                        
                        if not any([section_analysis["suggestions"], 
                                   section_analysis.get("skill_suggestions"),
                                   section_analysis.get("improved_bullets")]):
                            st.success("✨ This section looks good! No immediate improvements needed.")
            else:
                st.error("Failed to parse the resume. Please check the file format and try again.")


# Add footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit and AI</p>
    </div>
""", unsafe_allow_html=True)