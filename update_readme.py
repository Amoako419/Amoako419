import os
import requests

GITHUB_API_URL = "https://api.github.com"
REPO = "Amoako419/Amoako419"
README_FILE = "README.md"

def fetch_merged_prs():
    token = os.getenv("TOKEN")
    headers = {"Authorization": f"token {token}"}
    url = f"{GITHUB_API_URL}/search/issues?q=repo:{REPO}+is:pr+is:merged+author:Amoako419"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data.get("items", [])

def update_readme(merged_prs):
    with open(README_FILE, "r") as file:
        lines = file.readlines()

    start_marker = "<!-- START Merged PRs -->"
    end_marker = "<!-- END Merged PRs -->"
    start_index = lines.index(f"{start_marker}\n")
    end_index = lines.index(f"{end_marker}\n")

    pr_list = [f"- [{pr['title']}]({pr['html_url']})" for pr in merged_prs]
    pr_section = "\n".join(pr_list)

    new_lines = lines[:start_index + 1] + [pr_section + "\n"] + lines[end_index:]
    with open(README_FILE, "w") as file:
        file.writelines(new_lines)

def main():
    print("Token exists:", bool(token))
    merged_prs = fetch_merged_prs()
    update_readme(merged_prs)

if __name__ == "__main__":
    main()
