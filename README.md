# Vocabulary Tree Image Retrieval

Repository: https://github.com/fammad/vocab-tree-image-retrieval-EQ2425

We will do visual search built from scratch with SIFT features, a vocabulary tree (hierarchical k-means) and TF-IDF scoring. Given one photo of a building, the system finds the same building among 50. EQ2425 Analysis and Search of Visual Data, KTH, Project 2. Deadline October 5, 2026.

## Setup

Do this once. It takes about 15 minutes. Everything happens inside **VS Code**, in its terminal.

To open the terminal in VS Code: **Terminal** menu, **New Terminal**. On Mac this is zsh, on Windows it is PowerShell. Paste each command block and press Enter.

### 1. Install Python 3.11, Git and GitHub CLI

**Mac.** First check whether Homebrew is installed:
```
brew install python@3.11 git gh
```

**Windows:**
```
winget install -e --id Python.Python.3.11
winget install -e --id Git.Git
winget install -e --id GitHub.cli
```
Accept the prompts. Then **close VS Code completely and open it again**, so the terminal finds the new programs.

### 2. Clone the repository

Accept the GitHub invite in your email first. Then clone in one of two ways.

**With the GitHub Desktop app:** open the **File** menu, click **Clone Repository**, open the **URL** tab and paste:
```
https://github.com/fammad/vocab-tree-image-retrieval-EQ2425
```
Set **Local Path** to your Documents folder and click **Clone**.

**With the VS Code terminal:**
```
cd ~/Documents
git clone https://github.com/fammad/vocab-tree-image-retrieval-EQ2425.git
```
The repository is private, so the terminal needs your GitHub login. Run this once before cloning and choose **GitHub.com**, **HTTPS**, **Yes**, **Login with a web browser**:
```
gh auth login
```
Don't type your GitHub password into the terminal when git asks, because GitHub rejects it.

The images are included (about 450 MB), so this takes a few minutes. Don't rename, edit or delete anything in `Data2`, so we all run on identical files.

Now open the project: **File** menu, **Open Folder**, choose `Documents/vocab-tree-image-retrieval-EQ2425`. Open a new terminal. It now starts inside the project folder.

### 3. Create and activate the virtual environment

The virtual environment (`.venv`) is a folder holding this project's own Python and packages. It keeps everyone on the same versions and leaves the rest of your computer untouched.

Mac:
```
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows:
```
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

The terminal line now starts with `(.venv)`. That means it is active.

On Windows, if you get a red error saying running scripts is disabled, run this once and activate again:
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 4. Install the packages

With `(.venv)` showing:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` holds the exact package versions we all use. Don't install other versions of these packages. Run this command again whenever `requirements.txt` changes.

### 5. Connect VS Code to the environment

Press **Cmd+Shift+P** (Mac) or **Ctrl+Shift+P** (Windows), type **Python: Select Interpreter**, and choose the one that shows `.venv`.

VS Code then uses this Python for the Run button, and every new terminal activates `.venv` by itself.

### 6. Set up notebooks

Notebooks save their images inside the file. One run of `project2.ipynb` makes it several MB instead of about 10 KB. `nbstripout` removes the outputs automatically when you commit. Your own copy keeps them. Run once, with `(.venv)` showing:
```
nbstripout --install
```
When you open a notebook in VS Code, click **Select Kernel** in the top right and choose `.venv`. If VS Code asks to install the Jupyter extension, accept.

### 7. Check that everything works

```
python check_env.py
```

The last line must say `ALL OK`. If it says `FAIL`, the line tells you what is wrong. Fix it and run the check again.

## Project code

| File | What it is |
|---|---|
| `project2.ipynb` | The whole project: sections 2, 3 and 4, with results and figures |
| `extract.py` | Section 2: SIFT feature extraction |
| `vocab_tree.py` | Section 3: `hi_kmeans(data, b, depth)` and the leaf data for TF-IDF |
| `figures/` | Figures for the report, saved by the notebook |
| `Data2/` | The images, don't edit |
| `check_env.py`, `requirements.txt` | Setup |

`features/` appears after the first run. It is not uploaded.

### How to run

1. Once, in the terminal: `python extract.py` (about 30 s, creates `features/`).
2. Open `project2.ipynb`, choose the `.venv` kernel, click **Run All**. Section 3 builds the trees, about 45 s.

### Results so far
| | Images | Features in total | Mean per object |
|---|---|---|---|
| Server (database) | 149 | 536,769 | 10,735 |
| Client (queries) | 50 | 171,140 | 3,423 |

| Tree | Leaves | Distances per descriptor, tree | Flat vocabulary |
|---|---|---|---|
| b=4, depth=3 | 64 | 12 | 64 |
| b=4, depth=5 | 1,024 | 20 | 1,024 |
| b=5, depth=7 | about 75,000 | 35 | 78,125 |

Section 4 is open.

## Every time you work on the project

Open the project folder in VS Code and open a new terminal. Check that the line starts with `(.venv)`. If it doesn't, run the activate line from step 3.