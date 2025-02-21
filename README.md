# AI-Powered Resume Tailoring Tool

An intelligent resume optimization tool that leverages Google's Gemini AI to help job seekers tailor their resumes to specific job descriptions. The tool analyzes resumes, suggests improvements, and helps align qualifications with job requirements.

## Features

- **Resume Analysis**: Analyzes resume sections and provides detailed improvement suggestions
- **Job Alignment**: Matches resume content with job requirements
- **Skill Gap Analysis**: Identifies missing skills and suggests ways to incorporate them
- **Professional Summary Generation**: Creates compelling summaries tailored to job descriptions
- **Bullet Point Optimization**: Enhances resume bullet points with stronger action verbs and metrics

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

1. Start the application:
```bash
python app.py
```

2. Use the tool to:
   - Upload your resume
   - Paste job descriptions
   - Get tailored optimization suggestions
   - Generate improved content

## Technical Architecture

### Components

- **GeminiOptimizer**: Core AI integration using Google's Gemini API
- **ResumeParser**: Handles resume document parsing and section extraction
- **JobAnalyzer**: Analyzes job descriptions and extracts key requirements
- **ResumeOptimizer**: Orchestrates the optimization process

### Tech Stack

- Python
- Google Gemini AI API
- Sentence Transformers for text analysis
- Natural Language Processing (NLP) tools

## Development

### Prerequisites

- Python 3.8+
- Google Gemini API access
- Required Python packages (see requirements.txt)

### Setting Up Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for providing the AI capabilities
- Sentence Transformers library for text analysis
- Contributors and maintainers

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Add support for multiple resume formats
- [ ] Implement batch processing capabilities
- [ ] Enhance AI suggestions with industry-specific insights
- [ ] Add resume template generation
- [ ] Implement user authentication and profile management