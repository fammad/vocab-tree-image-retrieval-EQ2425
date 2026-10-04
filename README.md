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
| `project2.ipynb` | The whole project: sections 2, 3 and 4 |
| `Data2/` | The images, don't edit |
| `check_env.py`, `requirements.txt` | Setup |

### How to run

Open `project2.ipynb`, choose the `.venv` kernel, click **Run All**. It takes about 2 minutes (SIFT on full-size images, then three trees).

### Results so far

| | Value |
|---|---|
| 2(a) average SIFT features per database object | 8,940.58 |
| 2(b) average SIFT features per query object | 3,000.3 |

| Tree | Leaves | Leaves with idf = 0 | Leaves with df = 1 |
|---|---|---|---|
| b=4, depth=3 | 64 | 63 | 0 |
| b=4, depth=5 | 1,024 | about 150 | 0 |
| b=5, depth=7 | about 70,000 | 0 | about 29,000 |

Section 4 (querying and recall) is in progress: the TODO cells in the notebook.

## Every time you work on the project

Open the project folder in VS Code and open a new terminal. Check that the line starts with `(.venv)`. If it doesn't, run the activate line from step 3.