import requests
import sys
from datetime import datetime, timedelta

def utc_to_vancouver(utc_str):
    utc_time = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
    vancouver_offset = timedelta(hours=-8)
    vancouver_time = utc_time + vancouver_offset
    return vancouver_time.strftime("%Y-%m-%d %H:%M:%S")

def get_repo_dates(repo_url):
    # Parse the repository owner and name
    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo_name = parts[-1]

    # Use GitHub API to fetch repository information
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        created_at = data.get("created_at", "N/A")
        pushed_at = data.get("pushed_at", "N/A")

        return utc_to_vancouver(created_at), utc_to_vancouver(pushed_at)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None, None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    created_at, pushed_at = get_repo_dates(repo_url)

    print(f"Created At (Vancouver Time): {created_at}")
    print(f"Last Pushed At (Vancouver Time): {pushed_at}")
