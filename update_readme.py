```python
import os
import requests

# -------------------------------
# CONFIG
# -------------------------------
USERNAME = "shaillybhardwaj123"
README_PATH = "README.md"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("❌ Please set your GITHUB_TOKEN environment variable.")

headers = {"Authorization": f"token {TOKEN}"}

# -------------------------------
# FETCH ALL REPOS
# -------------------------------
def get_all_repos():
    repos = []
    page = 1

    while True:
        repos_url = f"https://api.github.com/user/repos?per_page=100&page={page}&type=all"
        response = requests.get(repos_url, headers=headers)

        if response.status_code != 200:
            print("❌ Error fetching repos:", response.json())
            break

        page_repos = response.json()

        if not page_repos:
            break

        repos.extend(page_repos)
        page += 1

    return repos


repos = get_all_repos()
print(f"✅ Found {len(repos)} repositories")

# -------------------------------
# CALCULATE LANGUAGES
# -------------------------------
lang_totals = {}

for repo in repos:
    repo_name = repo["name"]

    lang_url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/languages"
    lang_response = requests.get(lang_url, headers=headers)

    if lang_response.status_code == 200:
        langs = lang_response.json()

        for lang, bytes_count in langs.items():
            lang_totals[lang] = lang_totals.get(lang, 0) + bytes_count

if not lang_totals:
    print("⚠️ No language data found.")
    exit()

total_bytes = sum(lang_totals.values())

sorted_langs = sorted(
    lang_totals.items(),
    key=lambda x: x[1],
    reverse=True
)

print("\n📊 Languages Found:")
for lang, bytes_count in sorted_langs[:8]:
    percent = (bytes_count / total_bytes) * 100
    print(f"  {lang}: {percent:.2f}%")

# -------------------------------
# TAKE TOP 6 LANGUAGES
# -------------------------------
top_languages = sorted_langs[:6]

# -------------------------------
# CREATE LANGUAGE BAR SECTION
# -------------------------------
top_langs_html = "<!--START_SECTION:top_langs-->\n"

top_langs_html += '''
<div align="center"
style="
background:#282828;
padding:20px;
border-radius:12px;
margin:20px 0;
max-width:700px;
color:#ebdbb2;
text-align:center;
font-family:Arial,sans-serif;
border:1px solid #665c54;
">
'''

top_langs_html += '''
<h3 style="
color:#fabd2f;
margin-bottom:20px;
font-weight:700;
font-size:24px;
">
Most Used Languages
</h3>
'''

top_langs_html += '''
<div style="
display:grid;
grid-template-columns:1fr 1fr;
gap:15px;
max-width:650px;
margin:0 auto;
">
'''

for lang, bytes_count in top_languages:

    percent = (bytes_count / total_bytes) * 100

    # Gruvbox progress colors
    if percent >= 50:
        fill_color = "#fabd2f"   # yellow
    elif percent >= 15:
        fill_color = "#fe8019"   # orange
    elif percent >= 5:
        fill_color = "#d79921"   # dark yellow
    elif percent >= 1:
        fill_color = "#b16286"   # purple
    else:
        fill_color = "#83a598"   # blue

    top_langs_html += f'''
    <div style="
    background:#3c3836;
    padding:15px;
    border-radius:10px;
    text-align:left;
    border:1px solid #665c54;
    ">
    '''

    top_langs_html += f'''
    <p style="
    color:#ebdbb2;
    margin:0 0 10px 0;
    font-weight:600;
    font-size:15px;
    display:flex;
    justify-content:space-between;
    ">
    <span>{lang}</span>
    <span>{percent:.2f}%</span>
    </p>
    '''

    top_langs_html += f'''
    <div style="
    background:#504945;
    border-radius:999px;
    height:10px;
    width:100%;
    overflow:hidden;
    ">
    '''

    top_langs_html += f'''
    <div style="
    background:{fill_color};
    height:10px;
    border-radius:999px;
    width:{percent:.2f}%;
    transition:width 0.5s ease;
    ">
    </div>
    '''

    top_langs_html += '''
    </div>
    </div>
    '''

top_langs_html += '''
</div>
</div>
'''

top_langs_html += "\n<!--END_SECTION:top_langs-->"

# -------------------------------
# UPDATE README
# -------------------------------
with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start_tag = "<!--START_SECTION:top_langs-->"
end_tag = "<!--END_SECTION:top_langs-->"

if start_tag in content and end_tag in content:

    old_section = content.split(start_tag)[1].split(end_tag)[0]

    content = content.replace(
        f"{start_tag}{old_section}{end_tag}",
        top_langs_html
    )

else:
    content += "\n\n" + top_langs_html

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ README updated successfully!")
print("🎯 Top Languages:")

for lang, bytes_count in top_languages:
    percent = (bytes_count / total_bytes) * 100
    print(f"   {lang}: {percent:.2f}%")
```
