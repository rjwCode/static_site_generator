# 🛠️ Static Site Generator

This is a fully functional static site generator built in Python. It recursively converts markdown files to styled HTML pages using a custom templating system, Markdown parser, and object-oriented HTML rendering. Built as part of Boot.dev’s backend curriculum.

---

## 📦 Features

- ✅ Convert Markdown to HTML (headings, lists, code blocks, links, images)
- ✅ Inline markdown formatting: **bold**, *italic*, `code`, [links](#), ![images](#)
- ✅ Custom HTMLNode rendering system (like a mini DOM)
- ✅ Template-based layout injection with `{{ Title }}` and `{{ Content }}`
- ✅ Recursive directory traversal for `.md` content
- ✅ Static file handling (CSS, images, etc.)
- ✅ Unit-tested with full coverage using `unittest`
- ✅ CLI integration with `main.py`, `main.sh`, and `build.sh`

---

## 🚀 How to Run

### 🛠️ Setup
1. Make sure you have **Python 3** installed
2. Clone this repository and navigate to the root folder
3. Ensure these folders/files exist:
   - `content/` — contains your Markdown files
   - `static/` — contains images and `index.css`
   - `template.html` — your base HTML template

---

```bash
# Generate the site and start a local server
./main.sh
# OR build using a custom base path (for GitHub Pages)
./build.sh /static_site_generator/
```

You can then visit your generated site at:  
📂 `http://localhost:8888`

---

## 📁 Folder Structure

```
static_site_generator/
├── build.sh                   # Script to build with base path (e.g., for GitHub Pages)
├── main.sh                    # Script to generate site and launch dev server
├── template.html              # Base HTML layout with {{ Title }} and {{ Content }}
├── test.sh                    # (Optional) test runner script
│
├── content/                   # Input markdown files (converted to HTML and placed in docs/)
│   ├── index.md
│   ├── contact/
│   │   └── index.md
│   └── blog/
│       ├── glorfindel/
│       │   └── index.md
│       ├── majesty/
│       │   └── index.md
│       └── tom/
│           └── index.md
│
├── docs/                      # Output folder (auto-generated)
│   ├── index.html
│   ├── index.css
│   ├── contact/index.html
│   └── blog/
│       ├── glorfindel/index.html
│       ├── majesty/index.html
│       └── tom/index.html
│   └── images/
│       ├── glorfindel.png
│       ├── rivendell.png
│       ├── tolkien.png
│       └── tom.png
│
├── static/                    # Assets to copy into docs/
│   ├── index.css
│   └── images/
│       ├── glorfindel.png
│       ├── rivendell.png
│       ├── tolkien.png
│       └── tom.png
│
├── src/                       # Source code and test modules
│   ├── main.py
│   ├── htmlnode.py
│   ├── markdown_blocks.py
│   ├── textnode.py
│   ├── test_convert.py
│   ├── test_extract_markdown.py
│   ├── test_htmlnode.py
│   ├── test_markdown_blocks.py
│   ├── test_split_nodes.py
│   └── test_textnode.py
```

---

## 🧪 Example

```markdown
# This is my example site

This is **bold**, _italic_, and `code`.

![glorfindel](images/glorfindel.png)
```

Will be converted to HTML inside your template with styling, and saved to `/docs/`.

---

## 📚 What I Learned

- How to build a Markdown parser from scratch
- Designing HTML with object-oriented structures
- Recursive file I/O and CLI scripting
- Unit testing Python projects with `unittest`
- Template-based rendering and static asset management

---

## 🛠️ Tech Stack

- Python 3
- `unittest` for testing
- Custom markdown parsing & templating
- Bash for CLI scripts

