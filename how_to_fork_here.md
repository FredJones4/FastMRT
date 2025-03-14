You can still create a fork of the repository and move your changes there without losing any work. Follow these steps:

---

### **1. Fork the Repository on GitHub**
1. Go to the **original repository** on GitHub.
2. Click the **Fork** button (top-right corner).
3. This creates a new fork under your GitHub account.

---

### **2. Add the New Fork as a Remote**
Now, go to your local repository and add your fork as a new remote.

#### **Check Your Current Remotes**
Run:
```sh
git remote -v
```
This shows the original repository (likely named `origin`).

#### **Add Your Fork as a New Remote**
Replace `<your-github-username>` and `<repo-name>` with your actual GitHub details:
```sh
git remote add myfork https://github.com/<your-github-username>/<repo-name>.git
```
Now, `myfork` points to your forked repository.

---

### **3. Push Your Changes to Your Fork**
#### **Push Your Current Branch**
```sh
git push myfork <your-branch-name>
```
Replace `<your-branch-name>` with the branch you’ve been working on (if unsure, run `git branch` to check).

#### **If You Haven't Created a Branch Yet**
If you've been working on the `main` branch (or whatever the default is), it's better to create a new branch before pushing:
```sh
git checkout -b my-new-branch
git push myfork my-new-branch
```

---

### **4. Create a Pull Request (Optional)**
- If you want to merge your changes back into the original repository, go to your fork on GitHub and click **"Compare & pull request"**.
- If you just want to keep your changes in your fork, you're done!

---

### **Summary**
1. Fork the repo on GitHub.
2. Add your fork as a new remote (`myfork`).
3. Push your changes to your fork.
4. Optionally, create a pull request to merge back into the original repo.

Let me know if you need help with any step! 🚀