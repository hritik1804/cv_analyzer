# 🎯 CV Analyzer - JP/EN Tech Jobs

A comprehensive tool to analyze your resume/CV against Japanese tech job market requirements. Upload your resume, get matched with current job postings, and receive actionable recommendations to improve your profile.

## 🚀 Features

- **Multi-format Support**: Upload PDF or DOCX resumes
- **Bilingual Processing**: Support for English, Japanese, and mixed resumes
- **Real-time Job Matching**: Compare against current JapanDev and TokyoDev job postings
- **Fuzzy Skill Matching**: Advanced matching algorithms with synonym recognition
- **Interactive Dashboard**: Beautiful Streamlit interface with charts and analytics
- **Skill Gap Analysis**: Identify missing skills and get learning recommendations
- **Market Insights**: Understand skill demand in the Japanese tech market
- **Export Results**: Download analysis reports for future reference

## 📁 Project Structure

```
cv_analyzer/
├── app.py                    # Main Streamlit application
├── resume_parser.py          # Resume parsing and skill extraction
├── job_scraper.py           # Job scraping from various sources
├── matcher.py               # Skill matching and analysis engine
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── data/                   # Data directory
│   ├── skills_database.json # Skills and synonyms database
│   └── sample_resumes/     # Sample resume files for testing
├── tests/                  # Unit tests
│   ├── test_parser.py
│   ├── test_scraper.py
│   └── test_matcher.py
└── docs/                   # Documentation
    ├── installation.md
    ├── usage.md
    └── api_reference.md
```

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/cv-analyzer.git
cd cv-analyzer
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv cv_analyzer_env
cv_analyzer_env\Scripts\activate

# macOS/Linux
python3 -m venv cv_analyzer_env
source cv_analyzer_env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLP Models (Optional but Recommended)

```bash
# For English NLP processing
python -m spacy download en_core_web_sm

# For Japanese NLP processing (optional)
python -m spacy download ja_core_news_sm
```

### Step 5: Create Data Directory

```bash
mkdir -p data/sample_resumes
```

## 🚀 Quick Start

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Basic Usage

1. **Upload Resume**: Choose your PDF or DOCX resume file
2. **Select Language**: Choose English, Japanese, or Mixed
3. **Choose Job Sources**: Select from JapanDev, TokyoDev, or Sample Data
4. **Analyze**: Click the "Analyze Resume" button
5. **Review Results**: Explore matched skills, gaps, and recommendations
6. **Export**: Download your analysis report

## 📊 Features in Detail

### Resume Parsing

- **PDF Support**: Advanced PDF text extraction using pdfminer.six
- **DOCX Support**: Full document parsing including tables
- **Skill Extraction**: Intelligent skill recognition with 500+ tech skills
- **Contact Info**: Automatic extraction of email, phone, LinkedIn, GitHub
- **Experience Analysis**: Extract years of experience for different technologies
- **Entity Recognition**: NLP-powered extraction of companies, locations, dates

### Job Market Analysis

- **Live Scraping**: Real-time job data from popular job boards
- **Sample Data**: Built-in sample jobs for testing and demo
- **Skill Aggregation**: Analyze demand across hundreds of job postings
- **Company Insights**: See which companies are hiring
- **Location Analysis**: Understand geographic distribution of opportunities
- **Salary Information**: Extract and analyze salary ranges

### Skill Matching Engine

- **Exact Matching**: Direct skill name matching
- **Fuzzy Matching**: Handle variations and typos (80%+ similarity threshold)
- **Synonym Recognition**: 200+ skill synonyms and variations
- **Bilingual Support**: English-Japanese skill translation
- **Category Classification**: Group skills into programming, frameworks, tools, etc.
- **Demand Weighting**: Prioritize high-demand skills in matching

### Analytics and Insights

- **Match Score**: Overall compatibility percentage
- **Skill Demand**: See how often each skill appears in job postings
- **Gap Analysis**: Identify top skills missing from your resume
- **Learning Path**: Prioritized recommendations for skill development
- **Market Trends**: Understand what skills are hot in the Japanese market
- **Company Analysis**: See hiring patterns by company and location

## 🛠️ Configuration

### Skills Database

The application uses a JSON-based skills database (`data/skills_database.json`) that includes:

- **Programming Languages**: Python, JavaScript, Java, Go, etc.
- **Frameworks**: React, Angular, Django, Spring, etc.  
- **Databases**: MySQL, PostgreSQL, MongoDB, etc.
- **Cloud Platforms**: AWS, Azure, GCP, etc.
- **Tools**: Git, Docker, Jenkins, etc.
- **Japanese Translations**: パイソン, リアクト, etc.

You can extend this database by adding new skills and categories.

### Customizing Job Sources

To add new job sources, extend the `JobScraper` class:

```python
def scrape_new_source_jobs(self, limit: int = 20) -> List[Dict]:
    # Implement scraping logic
    pass
```

### Adjusting Matching Parameters

Modify matching sensitivity in `matcher.py`:

```python
matcher = SkillMatcher(
    fuzzy_threshold=80,        # Fuzzy match threshold (0-100)
    exact_match_weight=1.0,    # Weight for exact matches
    fuzzy_match_weight=0.7     # Weight for fuzzy matches
)
```

## 📈 Usage Examples

### Analyzing a Python Developer Resume

```python
from resume_parser import ResumeParser
from job_scraper import JobScraper
from matcher import SkillMatcher

# Initialize components
parser = ResumeParser()
scraper = JobScraper()
matcher = SkillMatcher()

# Parse resume
with open('my_resume.pdf', 'rb') as f:
    resume_data = parser.parse_file(f, language='english')

# Get job data
jobs = scraper.get_sample_jobs()

# Analyze skills
analysis = matcher.analyze_skills(resume_data, jobs)
print(f"Match Score: {analysis['match_score']:.1f}%")
print(f"Matched Skills: {analysis['matched_skills']}")
print(f"Missing Skills: {analysis['missing_skills']}")
```

### Custom Skill Analysis

```python
# Compare with specific job
job_data = {
    'title': 'Senior Python Developer',
    'skills': ['Python', 'Django', 'PostgreSQL', 'Docker', 'AWS']
}

result = matcher.compare_with_specific_job(resume_data, job_data)
print(f"Job Match Score: {result['match_score']:.1f}%")
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_parser.py -v
```

### Test Data

Sample test files are provided in `data/sample_resumes/`:

- `sample_en_resume.pdf` - English tech resume
- `sample_jp_resume.docx` - Japanese resume
- `sample_mixed_resume.pdf` - Bilingual resume

## 🌐 API Reference

### ResumeParser Class

```python
parser = ResumeParser(skills_db_path="data/skills_database.json")

# Parse file
resume_data = parser.parse_file(uploaded_file, language="english")

# Add custom skill
parser.add_skill_to_database("FastAPI", "frameworks", "english")

# Search skills
matching = parser.search_skills("react", "english")
```

### JobScraper Class

```python
scraper = JobScraper()

# Scrape from multiple sources
jobs = scraper.scrape_jobs(["JapanDev", "TokyoDev"], limit_per_source=10)

# Get sample data
sample_jobs = scraper.get_sample_jobs()

# Save/load jobs
scraper.save_jobs_to_file(jobs, "jobs.json")
loaded_jobs = scraper.load_jobs_from_file("jobs.json")

# Get skill summary
skill_summary = scraper.get_job_skills_summary(jobs)
```

### SkillMatcher Class

```python
matcher = SkillMatcher(fuzzy_threshold=80)

# Basic skill analysis
analysis = matcher.analyze_skills(resume_data, job_data)

# Advanced gap analysis
gap_analysis = matcher.get_skill_gap_analysis(resume_data, job_data, target_role="Python Developer")

# Compare with specific job
job_match = matcher.compare_with_specific_job(resume_data, single_job_data)
```

## 🎨 Customization

### Adding New Skills

1. **Via UI**: The application automatically learns new skills from job postings
2. **Manually**: Edit `data/skills_database.json`:

```json
{
  "frameworks": {
    "english": ["React", "Angular", "Vue.js", "FastAPI"],
    "japanese": ["リアクト", "アンギュラー", "ビューJS"]
  }
}
```

### Custom Styling

Modify the CSS in `app.py`:

```python
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #your-color1, #your-color2);
        /* Your custom styles */
    }
    </style>
    """, unsafe_allow_html=True)
```

### Adding New Job Sources

1. Create a new scraper method in `job_scraper.py`:

```python
def scrape_your_site_jobs(self, limit: int = 20) -> List[Dict]:
    jobs = []
    # Your scraping logic here
    return jobs
```

2. Add to the main scraping method:

```python
def scrape_jobs(self, sources: List[str], limit_per_source: int = 10):
    for source in sources:
        if source == "YourSite":
            jobs = self.scrape_your_site_jobs(limit_per_source)
```

## 🔍 Troubleshooting

### Common Issues

**1. PDF parsing fails**
```bash
# Install additional dependencies
pip install pdfminer.six==20231228
```

**2. Japanese text not processing**
```bash
# Install Japanese tokenizer
pip install janome
# OR
pip install mecab-python3
```

**3. Fuzzy matching not working**
```bash
# Install fuzzy matching libraries
pip install fuzzywuzzy python-levenshtein
```

**4. SpaCy models missing**
```bash
# Download required models
python -m spacy download en_core_web_sm
python -m spacy download ja_core_news_sm
```

**5. Streamlit port already in use**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

For large resumes or many jobs:

```python
# Limit job analysis
jobs = scraper.scrape_jobs(sources, limit_per_source=5)

# Reduce fuzzy matching threshold
matcher = SkillMatcher(fuzzy_threshold=90)
```

## 📊 Sample Analysis Output

Here's what a typical analysis looks like:

```
📋 Resume Analysis Results
========================
Total Skills Found: 12
Matched Skills: 8 (66.7%)
Missing Skills: 4
Unique Skills: 4

✅ Matched Skills:
Python, JavaScript, React, Node.js, PostgreSQL, Docker, Git, Agile

❌ Missing High-Demand Skills:
AWS (demanded in 78% of jobs)
Kubernetes (demanded in 65% of jobs) 
TypeScript (demanded in 54% of jobs)
MongoDB (demanded in 45% of jobs)

⭐ Your Unique Skills:
MATLAB, Photoshop, Unity, C++

💡 Recommendations:
1. HIGH PRIORITY: Learn AWS - critical for 78% of jobs
2. MEDIUM PRIORITY: Add Kubernetes experience
3. ENHANCE: Strengthen your React skills with more projects

🎯 Match Score: 72.3%
Application Readiness: Good
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Make your changes
5. Run tests: `pytest`
6. Submit a pull request

### Areas for Contribution

- **New Job Sources**: Add scrapers for more Japanese job sites
- **Language Support**: Improve Japanese text processing
- **Skill Database**: Expand the skills database
- **UI Improvements**: Enhance the Streamlit interface
- **Performance**: Optimize parsing and matching algorithms
- **Testing**: Add more comprehensive tests

### Code Style

We use Black for code formatting:

```bash
black *.py
flake8 *.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SpaCy**: NLP processing
- **Streamlit**: Web application framework
- **Beautiful Soup**: Web scraping
- **FuzzyWuzzy**: Fuzzy string matching
- **PDFMiner**: PDF text extraction
- **Janome**: Japanese text tokenization

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cv-analyzer/issues)
- **Documentation**: [Project Wiki](https://github.com/yourusername/cv-analyzer/wiki)
- **Email**: your.email@example.com

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Machine learning skill categorization
- [ ] Resume template generation
- [ ] Integration with LinkedIn API
- [ ] Mobile app version
- [ ] Multi-language support (Korean, Chinese)
- [ ] ATS optimization suggestions
- [ ] Salary prediction based on skills

### Version 1.1 (In Progress)
- [ ] Improved Japanese text processing
- [ ] More job sources (Indeed Japan, Wantedly)
- [ ] Better error handling
- [ ] Resume comparison feature
- [ ] Skill trend analysis

---

**Made with ❤️ for the Japanese tech community**

*Star ⭐ this repository if you find it helpful!*