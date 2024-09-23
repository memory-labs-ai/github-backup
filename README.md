# GitHub Backup Tool 🚀

**Safeguard your GitHub repositories effortlessly!** This Python-based tool allows you to back up all repositories from multiple GitHub organizations with ease. Whether you're a developer, a team lead, or just someone who loves their code, this tool ensures your projects are safe and sound.

## 📦 Features

- **Automated Backups:** Clone new repositories and update existing ones automatically.
- **Multi-Organization Support:** Backup repositories from multiple GitHub organizations.
- **Logging:** Keep track of all backup operations with detailed logs.
- **Easy Configuration:** Simple YAML configuration for quick setup.
- **Cross-Platform:** Works on Linux, macOS, and Windows.

## 🛠️ Installation

### 1. **Clone the Repository**

```bash
git clone https://github.com/memory-labs-ai/github-backup.git
cd github-backup
```

### 2. **Set Up a Virtual Environment (Optional but Recommended)**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. **Create a Configuration File**

   Copy the example configuration and customize it:

   ```bash
   cp config.yaml.example config.yaml
   ```

2. **Edit `config.yaml`**

   Open `config.yaml` in your favorite text editor and fill in the required details:

   ```yaml
   # GitHub Backup Configuration

   github:
     token: YOUR_PERSONAL_ACCESS_TOKEN  # Replace with your GitHub Personal Access Token
     organizations:
       - org_name_1
       - org_name_2

   backup:
     destination_path: /path/to/backup/directory  # Replace with your desired backup directory
     log_file: /path/to/backup.log  # Replace with your desired log file path
   ```

   **Generating a GitHub Personal Access Token:**

   1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens).
   2. Click on **"Generate new token"**.
   3. Select the following scopes:
      - `repo` (for accessing repositories)
      - `read:org` (for accessing organization data)
   4. Generate and **securely store** your token.

   **Security Tip:** Ensure that `config.yaml` is **not** committed to any public repository. The provided `.gitignore` handles this, but always double-check!

## 🚀 Usage

Run the backup script using Python:

```bash
python main.py
```

**Automate Backups with Cron (Linux/macOS):**

1. Open the crontab editor:

   ```bash
   crontab -e
   ```

2. Add a cron job for daily backups at 2 AM:

   ```cron
   0 2 * * * /usr/bin/env python3 /path/to/github_backup.py
   ```

   *Ensure that the paths to Python and the script are correct.*

**Automate Backups with Task Scheduler (Windows):**

1. Open **Task Scheduler**.
2. Create a new task:
   - **Trigger:** Set the schedule (e.g., daily at 2 AM).
   - **Action:** Start a program.
     - **Program/script:** `python`
     - **Add arguments:** `C:\path\to\main.py`
3. Save the task.

## 📚 Logging

All backup operations are logged to the file specified in `config.yaml` (e.g., `/path/to/backup.log`). Logs include timestamps, operations performed, and any errors encountered.

---

*Happy Coding and Backup! 🖥️💾*
