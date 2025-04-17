import os
import requests

GITHUB_API_URL = "https://api.github.com"
REPO = "Amoako419/Amoako419"
README_FILE = "README.md"

def fetch_merged_prs():
    token = os.getenv("TOKEN")
    if not token:
        raise EnvironmentError("Missing TOKEN environment variable. Make sure it's set correctly in your GitHub Actions workflow.")

    headers = {"Authorization": f"token {token}"}
    url = f"{GITHUB_API_URL}/search/issues?q=repo:{REPO}+is:pr+is:merged+author:Amoako419"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise
    except Exception as err:
        print(f"Other error occurred during API call: {err}")
        raise

    try:
        data = response.json()
    except Exception as json_err:
        print(f"Error decoding JSON: {json_err}")
        raise

    return data.get("items", [])

def update_readme(merged_prs):
    try:
        with open(README_FILE, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"{README_FILE} not found.")
        raise
    except Exception as err:
        print(f"Error reading {README_FILE}: {err}")
        raise

    start_marker = "<!-- START Merged PRs -->"
    end_marker = "<!-- END Merged PRs -->"

    try:
        start_index = lines.index(f"{start_marker}\n")
        end_index = lines.index(f"{end_marker}\n")
    except ValueError as ve:
        print(f"Marker not found in {README_FILE}: {ve}")
        raise

    pr_list = [f"- [{pr['title']}]({pr['html_url']})" for pr in merged_prs]
    pr_section = "\n".join(pr_list)

    new_lines = lines[:start_index + 1] + [pr_section + "\n"] + lines[end_index:]

    try:
        with open(README_FILE, "w") as file:
            file.writelines(new_lines)
    except Exception as err:
        print(f"Error writing to {README_FILE}: {err}")
        raise

def main():
    try:
        merged_prs = fetch_merged_prs()
        update_readme(merged_prs)
    except Exception as err:
        print(f"Script failed with error: {err}")
        exit(1)

if __name__ == "__main__":
    main()
