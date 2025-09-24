# job_scraper.py
import time
import re
from typing import Dict, List
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (skill-matcher-bot)"}

def clean_text(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()

def fetch(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.text

def scrape_japandev(limit: int = 25) -> List[Dict]:
    # JapanDev jobs page
    index_html = fetch("https://japan-dev.com/jobs")
    soup = BeautifulSoup(index_html, "lxml")
    jobs = []
    # Basic anchors to job pages
    for a in soup.select("a[href^='/jobs']")[:limit]:
        href = a.get("href")
        if not href:
            continue
        url = "https://japan-dev.com" + href
        try:
            html = fetch(url)
        except Exception:
            continue
        s = BeautifulSoup(html, "lxml")
        title = s.select_one("h1")
        jd = s.select_one("main") or s.select_one("article") or s
        jobs.append({
            "source": "JapanDev",
            "url": url,
            "title": clean_text(title.get_text()) if title else "Unknown",
            "requirements": clean_text(jd.get_text())
        })
        time.sleep(0.3)
    return jobs

def scrape_tokyodev(limit: int = 25) -> List[Dict]:
    index_html = fetch("https://www.tokyodev.com/jobs")
    soup = BeautifulSoup(index_html, "lxml")
    jobs = []
    for card in soup.select("a[href^='/jobs/']")[:limit]:
        href = card.get("href")
        url = "https://www.tokyodev.com" + href
        try:
            html = fetch(url)
        except Exception:
            continue
        s = BeautifulSoup(html, "lxml")
        title = s.select_one("h1")
        jd = s.select_one("main") or s.select_one("article") or s
        jobs.append({
            "source": "TokyoDev",
            "url": url,
            "title": clean_text(title.get_text()) if title else "Unknown",
            "requirements": clean_text(jd.get_text())
        })
        time.sleep(0.3)
    return jobs

def scrape_indeed(limit: int = 25) -> List[Dict]:
    # Placeholder for Indeed scraping (requires more complex handling)
    index_html = fetch("https://www.indeed.com/q-software-developer-jobs.html")
    soup = BeautifulSoup(index_html, "lxml")
    # Implement actual scraping logic here
    jobs = []
    for card in soup.select("a[href^='/rc/clk']")[:limit]:
        href = card.get("href")
        if not href:
            continue
        url = "https://www.indeed.com" + href
        try:
            html = fetch(url)
        except Exception:
            continue
        s = BeautifulSoup(html, "lxml")
        title = s.select_one("h1")
        jd = s.select_one("#jobDescriptionText") or s
        jobs.append({
            "source": "Indeed",
            "url": url,
            "title": clean_text(title.get_text()) if title else "Unknown",
            "requirements": clean_text(jd.get_text())
        })
        time.sleep(0.3)
    return []

def scrape_stackoverflow(limit: int = 25) -> List[Dict]:
    # TODO: Implement actual scraping logic for StackOverflow Jobs
    # This is a placeholder example
    return [
        {
            "source": "StackOverflow",
            "url": "https://stackoverflow.com/jobs/123",
            "title": "Backend Developer",
            "requirements": "Python, Django, AWS, Docker"
        }
    ][:limit]

def scrape_githubjobs(limit: int = 25) -> List[Dict]:
    # TODO: Implement actual scraping logic for GitHub Jobs
    return [
        {
            "source": "GitHubJobs",
            "url": "https://jobs.github.com/positions/abc",
            "title": "Full Stack Engineer",
            "requirements": "React, Node.js, AWS, SQL"
        }
    ][:limit]

def scrape_remotepython(limit: int = 25) -> List[Dict]:
    # TODO: Implement actual scraping logic for Remote Python
    return [
        {
            "source": "RemotePython",
            "url": "https://remotepython.com/jobs/xyz",
            "title": "Remote Python Developer",
            "requirements": "Python, Flask, Docker, PostgreSQL"
        }
    ][:limit]

def get_latest_jobs(limit: int = 25) -> List[Dict]:
    jobs = []
    try:
        jobs.extend(scrape_japandev(limit))
    except Exception:
        pass
    try:
        jobs.extend(scrape_tokyodev(limit))
    except Exception:
        pass
    try:
        jobs.extend(scrape_indeed(limit))
    except Exception:
        pass
    try:
        jobs.extend(scrape_stackoverflow(limit))
    except Exception:
        pass
    try:
        jobs.extend(scrape_githubjobs(limit))
    except Exception:
        pass
    try:
        jobs.extend(scrape_remotepython(limit))
    except Exception:
        pass
    return jobs
