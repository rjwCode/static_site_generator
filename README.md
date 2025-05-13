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
├── src/
│   ├── main.py                   # Entry point for site generation
│   ├── markdown_blocks.py        # Markdown parsing & HTML logic
│   ├── htmlnode.py               # HTML tree system (LeafNode, ParentNode)
│   ├── textnode.py               # Inline markdown parsing
├── content/                      # Input .md files (nested allowed)
├── docs/                         # Output .html files (auto-generated)
├── static/                       # index.css, images, etc.
├── template.html                 # HTML skeleton with placeholders
├── .gitignore                    # Avoids __pycache__ tracking
├── main.sh / build.sh            # CLI scripts
└── tests/                        # Unit test files (all key modules)
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

