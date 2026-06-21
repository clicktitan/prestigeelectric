# Cursor Desktop transfer file

Use this file to move the current project context from Cursor Cloud into Cursor Desktop.

## Project

- Repository: `clicktitan/prestigeelectric`
- GitHub URL: `https://github.com/clicktitan/prestigeelectric`
- Base branch: `main`
- Cloud handoff branch: `cursor/desktop-handoff-c765`
- Current project state: initial repo with `README.md` plus this transfer file.

## Fastest way to open this in Cursor Desktop

1. Open Cursor Desktop.
2. Choose **Clone Repo** or open a terminal.
3. Clone the repo:

   ```bash
   git clone https://github.com/clicktitan/prestigeelectric.git
   cd prestigeelectric
   ```

4. Fetch and switch to the handoff branch:

   ```bash
   git fetch origin cursor/desktop-handoff-c765
   git checkout cursor/desktop-handoff-c765
   ```

5. Open the folder in Cursor Desktop:

   ```bash
   cursor .
   ```

## If you already cloned the repo locally

From your local `prestigeelectric` folder:

```bash
git fetch origin cursor/desktop-handoff-c765
git checkout cursor/desktop-handoff-c765
git pull origin cursor/desktop-handoff-c765
```

Then open that folder in Cursor Desktop.

## What to tell Cursor Desktop

Paste this into Cursor Desktop if you want it to continue from here:

> Continue work on the `prestigeelectric` repo from branch `cursor/desktop-handoff-c765`. Read `CURSOR_DESKTOP_TRANSFER.md` first, then inspect the repository and help me continue development from the current state.

## Notes

- This repo is currently very minimal, so there are no app dependencies or setup commands yet.
- If more files are added in Cursor Cloud later, commit and push them, then run `git pull origin <branch-name>` in Cursor Desktop.
- If you want to work from `main` instead, switch with:

  ```bash
  git checkout main
  git pull origin main
  ```
