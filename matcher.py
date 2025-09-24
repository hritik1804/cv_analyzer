# matcher.py
from typing import Dict, List, Set, Tuple
from collections import Counter
from rapidfuzz import fuzz
import re

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()

def extract_job_skills(text: str, skills_dict: Dict[str, List[str]], fuzzy_threshold: int = 92) -> Set[str]:
    # fuzzy map job requirement text to canonical skills
    found = set()
    norm_text = normalize(text)
    for canonical, variants in skills_dict.items():
        all_variants = set(v.strip().lower() for v in variants + [canonical])
        # substring hit
        if any(v in norm_text for v in all_variants if len(v) >= 2):
            found.add(canonical)
            continue
        # fuzzy scan word-wise
        words = set(re.findall(r"[A-Za-z0-9\+\.\-/#]{2,}|[\u3040-\u30ff\u3400-\u9fff]{1,}", norm_text))
        for w in words:
            if any(fuzz.ratio(w, v) >= fuzzy_threshold for v in all_variants):
                found.add(canonical)
                break
    return found

def match_resume_to_jobs(resume_skills: Set[str], jobs: List[Dict], skills_dict: Dict[str, List[str]]) -> Tuple[List[Dict], List[str], List[str]]:
    results = []
    demand_counter = Counter()
    for job in jobs:
        job_skill_hits = extract_job_skills(job.get("requirements", ""), skills_dict)
        demand_counter.update(job_skill_hits)
        overlap = sorted(resume_skills & job_skill_hits)
        missing = sorted(job_skill_hits - resume_skills)
        score = int(100 * len(overlap) / max(1, len(job_skill_hits)))
        results.append({
            "title": job.get("title", "Unknown"),
            "source": job.get("source", "Unknown"),
            "url": job.get("url", ""),
            "score": score,
            "overlap": overlap,
            "missing": missing
        })
    # high-demand skills: frequent in jobs but not in resume
    missing_global = [s for s, _ in demand_counter.most_common() if s not in resume_skills]
    # unique resume skills: present in resume but rarely in jobs
    unique_resume = [s for s in sorted(resume_skills) if demand_counter[s] == 0]
    return results, missing_global, unique_resume
