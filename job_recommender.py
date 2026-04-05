JOB_MAP = {
    "machine learning": ["Machine Learning Engineer", "Data Scientist"],
    "react": ["Frontend Developer"],
    "node": ["Backend Developer"],
    "python": ["Software Developer", "Data Analyst"],
    "sql": ["Database Engineer", "Data Analyst"]
}

def get_job_links(skills):
    roles = set()
    
    for skill in skills:
        if skill in JOB_MAP:
            roles.update(JOB_MAP[skill])
    
    results = []
    
    for role in roles:
        query = role.replace(" ", "%20")
        link = f"https://www.linkedin.com/jobs/search/?keywords={query}"
        results.append((role, link))
    
    return results