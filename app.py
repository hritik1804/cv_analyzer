# app.py
import json
import streamlit as st
from resume_parser import load_skills_dict, parse_resume
from job_scraper import scrape_japandev, scrape_tokyodev, scrape_indeed, scrape_stackoverflow, scrape_githubjobs, scrape_remotepython
from matcher import match_resume_to_jobs, extract_job_skills
from collections import Counter

st.set_page_config(page_title="JP/EN Resume Keyword Analyzer", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.markdown(
    """
    <style>
    .sidebar-title {font-size:1.3rem; font-weight:700; margin-bottom:0.5em;}
    .sidebar-btn {margin-bottom:0.5em; width:100%;}
    </style>
    """, unsafe_allow_html=True
)
st.sidebar.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
nav_resume = st.sidebar.button("Resume Analyzer", key="nav_resume", help="Analyze your resume")
nav_skills = st.sidebar.button("Top Skills in Japan", key="nav_skills", help="View trending skills")

# --- Sidebar Settings ---
st.sidebar.header("Settings")
top_k_jobs = st.sidebar.slider("Jobs to fetch (per board)", 5, 50, 20)
suggestion_lang = st.sidebar.selectbox("Suggestion language", ["English", "日本語"])
fuzzy_threshold = st.sidebar.slider("Fuzzy threshold", 80, 100, 92)

# --- Sidebar: Job Sources Selection ---
st.sidebar.markdown("---")
st.sidebar.subheader("Job Sources")
job_sources = st.sidebar.multiselect(
    "Select job sources",
    ["JapanDev", "TokyoDev", "Indeed", "StackOverflow", "GitHubJobs", "RemotePython"],
    default=["JapanDev", "TokyoDev"]
)

# --- Sidebar Filters for Top Skills ---
st.sidebar.markdown("---")
st.sidebar.subheader("Skill Filters (Top Skills Page)")
job_type = st.sidebar.selectbox("Job Type", ["All", "Data", "Developer"])
skill_count = st.sidebar.radio("Skill Count", ["Top 10", "All"])

skills_dict = load_skills_dict("skills.json")

# --- Navigation Logic ---
if 'page' not in st.session_state:
    st.session_state.page = "Resume Analyzer"
if nav_resume:
    st.session_state.page = "Resume Analyzer"
if nav_skills:
    st.session_state.page = "Top Skills in Japan"
page = st.session_state.page

# --- Helper: Get jobs from selected sources ---
def get_jobs_with_sources(limit, sources):
    jobs = []
    if "JapanDev" in sources:
        try: jobs.extend(scrape_japandev(limit))
        except: pass
    if "TokyoDev" in sources:
        try: jobs.extend(scrape_tokyodev(limit))
        except: pass
    if "Indeed" in sources:
        try: jobs.extend(scrape_indeed(limit))
        except: pass
    if "StackOverflow" in sources:
        try: jobs.extend(scrape_stackoverflow(limit))
        except: pass
    if "GitHubJobs" in sources:
        try: jobs.extend(scrape_githubjobs(limit))
        except: pass
    if "RemotePython" in sources:
        try: jobs.extend(scrape_remotepython(limit))
        except: pass
    return jobs

# --- Resume Analyzer Page ---
if page == "Resume Analyzer":
    st.title("Resume/CV Keyword Analyzer (JP/EN)")
    st.markdown("""
    <style>
    .big-header {font-size:2rem; font-weight:700;}
    .section {background:#f7f7fa; padding:1em; border-radius:8px; margin-bottom:1em;}
    </style>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload a resume (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded:
        file_bytes = uploaded.read()
        try:
            lang, text, tokens, resume_skills = parse_resume(file_bytes, uploaded.name, skills_dict)
        except Exception as e:
            st.error(f"Failed to parse resume: {e}")
            st.stop()

        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("#### Detected Language")
        st.write(lang)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("#### Extracted Skills")
        st.write(sorted(resume_skills))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("#### Fetching Latest Jobs")
        jobs = get_jobs_with_sources(limit=top_k_jobs, sources=job_sources)
        st.write(f"Collected {len(jobs)} jobs")
        st.markdown('</div>', unsafe_allow_html=True)

        results, missing_global, unique_resume = match_resume_to_jobs(resume_skills, jobs, skills_dict)

        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("#### Match Results")
        for r in sorted(results, key=lambda x: x["score"], reverse=True)[:30]:
            st.markdown(f"**{r['title']}** ({r['source']}) — Score: {r['score']}%  \n{r['url']}")
            st.write("Overlap:", ", ".join(r["overlap"]) if r["overlap"] else "None")
            st.write("Missing:", ", ".join(r["missing"]) if r["missing"] else "None")
            st.divider()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("#### Suggestions")
        if suggestion_lang == "日本語":
            st.write("不足スキル（需要が高い）:", "、".join(missing_global[:20]) or "なし")
            st.write("履歴書に特有（需要が低い）:", "、".join(unique_resume) or "なし")
        else:
            st.write("Missing high-demand skills:", ", ".join(missing_global[:20]) or "None")
            st.write("Unique in resume (low demand):", ", ".join(unique_resume) or "None")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("#### You have")
        st.write(", ".join(sorted(resume_skills)) or "None found")
        st.markdown("#### Desired by jobs (top)")
        st.write(", ".join(missing_global[:15]) or "None")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Top Skills in Japan Page ---
elif page == "Top Skills in Japan":
    st.title("🌏 Top Tech Skills Across Domains")
    st.markdown("""
    <style>
    .skill-card {background:#f7f7fa; border-radius:8px; padding:1em; margin-bottom:0.7em;}
    .skill-title {font-weight:600; font-size:1.1rem;}
    .skill-count {color:#0072E5; font-weight:500;}
    </style>
    """, unsafe_allow_html=True)
    st.info("Live skill demand from selected job boards. Use filters in the sidebar!")

    jobs = get_jobs_with_sources(limit=top_k_jobs, sources=job_sources)
    all_skills = []
    filtered_jobs = []

    # --- Job Type Filtering ---
    for job in jobs:
        title = job.get("title", "").lower()
        reqs = job.get("requirements", "").lower()
        if job_type == "Data":
            if any(x in title or x in reqs for x in ["data", "analytics", "machine learning", "ai", "ml", "分析", "データ"]):
                filtered_jobs.append(job)
        elif job_type == "Developer":
            if any(x in title or x in reqs for x in ["developer", "engineer", "dev", "開発", "エンジニア", "プログラマー"]):
                filtered_jobs.append(job)
        else:
            filtered_jobs.append(job)

    for job in filtered_jobs:
        job_skills = extract_job_skills(job.get("requirements", ""), skills_dict, fuzzy_threshold)
        all_skills.extend(job_skills)
    skill_counts = Counter(all_skills)
    if skill_count == "Top 10":
        top_skills = skill_counts.most_common(10)
    else:
        top_skills = skill_counts.most_common()

    # --- Tabs for Chart and List ---
    tab1, tab2 = st.tabs(["📊 Chart", "📝 Skill Cards"])
    with tab1:
        st.markdown("### Skill Frequency Chart")
        st.bar_chart(dict(top_skills))

    with tab2:
        st.markdown("### Skill Cards")
        for skill, count in top_skills:
            st.markdown(
                f'<div class="skill-card"><span class="skill-title">{skill}</span> '
                f'<span class="skill-count">({count} jobs)</span></div>',
                unsafe_allow_html=True
            )
