import httpx

from contextforge.models import Project

def _repo_to_project(repo: dict) -> Project:
    return Project(
        name=repo["name"],
        repo_url=repo["html_url"],
        language=repo.get("language"),
    )

def list_repos(org: str, token: str) -> list[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    projects = []

    try:
        page = 1
        results = []
        
        for endpoint in [f"https://api.github.com/orgs/{org}/repos", f"https://api.github.com/users/{org}/repos"]:
            response = httpx.get(endpoint, headers=headers, params={"page": 1, "per_page": 1})
            if response.status_code == 200:
                url = endpoint
                break
        else:
            raise ValueError(f"Could not find org or user: {org}")

        while True:
            response = httpx.get(url, headers=headers, params={"page": page, "per_page": 100})
            response.raise_for_status()
            repos = response.json()
            results.extend(repos)

            if len(repos) < 100:
                break
            page += 1

        used_repos = [r for r in results if not r["archived"] and not r["fork"]]
        for repo in used_repos:
            project = _repo_to_project(repo)
            projects.append(project)

        return projects
    except httpx.HTTPError as e:
        print(f"Request failed: {e}")