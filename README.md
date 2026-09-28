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

`requirements.txt` holds the exact package versions we all use. Don't install other versions of these packages. Its last line, `-e .`, also installs our own code from `src/vocabtree`, so scripts and notebooks can import it from any folder. Run this command again whenever `requirements.txt` changes.

### 5. Connect VS Code to the environment

Press **Cmd+Shift+P** (Mac) or **Ctrl+Shift+P** (Windows), type **Python: Select Interpreter**, and choose the one that shows `.venv`.

VS Code then uses this Python for the Run button, and every new terminal activates `.venv` by itself.

### 6. Set up notebooks

Notebooks save their images inside the file. One run of `notebooks/01_features.ipynb` makes it about 3 MB instead of 8 KB, and two people editing outputs cause merge conflicts. `nbstripout` removes the outputs automatically when you commit. Your own copy keeps them. Run once, with `(.venv)` showing:
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

### Folders

| Folder or file | What's in it |
|---|---|
| `src/vocabtree/` | All project code: `extract.py` (section 2), `vocab_tree.py` (section 3), `plot_utils.py` (saves figures) |
| `notebooks/` | Notebooks that import the code and draw figures |
| `figures/` | Figures for the report, written by the notebooks, committed |
| `Data2/` | The images, committed, don't edit |
| `features/` | Created by the extraction, not committed |
| `check_env.py`, `requirements.txt`, `pyproject.toml` | Setup |

Run scripts from the repository folder with `python -m`, for example `python -m vocabtree.extract`. Import in notebooks with `from vocabtree.extract import load_features`.

### Feature extraction (section 2),

Run once after cloning. It takes about 30 seconds and writes `features/server.npz` and `features/client.npz`. Git doesn't upload these files, so everyone runs it themselves.
```
python -m vocabtree.extract
```

Results for the report:

| | Images | Features in total | Mean per image | Mean per object |
|---|---|---|---|---|
| Server (database) | 149 | 536,769 | 3,602 | 10,735 |
| Client (queries) | 50 | 171,140 | 3,423 | 3,423 |

### Vocabulary tree (section 3), first version

```
python -m vocabtree.vocab_tree
```
Builds the three trees from the task and prints their size. Takes about 45 seconds.

### Notebooks

Code that computes things lives in `src/vocabtree/`. Notebooks in `notebooks/` only import from it and draw figures. A new section gets a new file in `src/vocabtree/` (for example `query.py`) and a new notebook (`02_...`, `03_...`).

- Before committing, run the notebook from top to bottom (**Run All**) so it works for the next person.

## Every time you work on the project

Open the project folder in VS Code and open a new terminal. Check that the line starts with `(.venv)`. If it doesn't, run the activate line from step 3.