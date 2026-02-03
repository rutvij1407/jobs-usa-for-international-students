# Push to a new Git remote (e.g. GitHub)

Your local repo is initialized and the initial commit is done. To create a **new** remote repo and push:

## 1. Create a new repository on GitHub

1. Go to [https://github.com/new](https://github.com/new).
2. **Repository name:** e.g. `jobs-usa-for-international-students` (no spaces).
3. **Description:** optional (e.g. "F1 Job Dashboard backend and data analytics").
4. Choose **Public** (or Private).
5. **Do not** check "Add a README" or "Add .gitignore" — you already have them.
6. Click **Create repository**.

## 2. Add remote and push

Replace `YOUR_USERNAME` with your GitHub username and `REPO_NAME` with the repo name you used:

```bash
cd "/Users/vakatirutvijreddy/Projects/jobs-usa-for -international-students"

git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
# Or with SSH:
# git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

git branch -M main
git push -u origin main
```

Example (username `rutvij1407`, repo `jobs-usa-for-international-students`):

```bash
git remote add origin https://github.com/rutvij1407/jobs-usa-for-international-students.git
git branch -M main
git push -u origin main
```

After this, your code will be on GitHub. For future pushes: `git push`.
