#!/usr/bin/env python3
"""
GitHub Organizations Backup Script

This script backs up all repositories from specified GitHub organizations.
It clones new repositories and pulls updates for existing ones.
"""

import os
import sys
import logging
from pathlib import Path
from typing import List

from github import Github
from github.GithubException import GithubException
from git import Repo, GitCommandError
import yaml

# Constants
CONFIG_FILE = 'config.yaml'

def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file {config_path} not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file: {e}")
        sys.exit(1)

def setup_logging(log_file: str):
    """Configure logging for the script."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Also log to stdout
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

def get_organizations(github_client: Github, org_names: List[str]) -> List:
    """Retrieve organization objects from GitHub."""
    orgs = []
    for name in org_names:
        try:
            org = github_client.get_organization(name)
            orgs.append(org)
            logging.info(f"Accessed organization: {name}")
        except GithubException as e:
            logging.error(f"Failed to access organization '{name}': {e}")
    return orgs

def get_repositories(org) -> List:
    """Retrieve all repositories for a given organization."""
    try:
        repos = org.get_repos()
        repo_list = list(repos)
        logging.info(f"Retrieved {len(repo_list)} repositories from organization '{org.login}'.")
        return repo_list
    except GithubException as e:
        logging.error(f"Failed to retrieve repositories for organization '{org.login}': {e}")
        return []

def clone_or_pull_repo(repo_url: str, local_path: Path):
    """Clone the repository if not present; otherwise, pull the latest changes."""
    if not local_path.exists():
        try:
            logging.info(f"Cloning repository: {repo_url} into {local_path}")
            Repo.clone_from(repo_url, local_path)
            logging.info(f"Successfully cloned: {repo_url}")
        except GitCommandError as e:
            logging.error(f"Failed to clone {repo_url}: {e}")
    else:
        try:
            repo = Repo(local_path)
            logging.info(f"Pulling latest changes for repository: {repo_url}")
            origin = repo.remotes.origin
            origin.pull()
            logging.info(f"Successfully pulled updates for: {repo_url}")
        except GitCommandError as e:
            logging.error(f"Failed to pull updates for {repo_url}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error with {repo_url}: {e}")

def main():
    # Load configuration
    config = load_config(CONFIG_FILE)

    # Setup logging
    setup_logging(config['backup']['log_file'])

    # Initialize GitHub client
    github_token = config['github']['token']
    if not github_token:
        logging.error("GitHub token not provided in configuration.")
        sys.exit(1)
    github_client = Github(github_token, per_page=100)

    # Get organizations
    org_names = config['github']['organizations']
    organizations = get_organizations(github_client, org_names)
    if not organizations:
        logging.error("No valid organizations found. Exiting.")
        sys.exit(1)

    # Ensure backup destination exists
    backup_dir = Path(config['backup']['destination_path'])
    backup_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Backup directory set to: {backup_dir.resolve()}")

    # Iterate through organizations and their repositories
    for org in organizations:
        repos = get_repositories(org)
        for repo in repos:
            repo_name = repo.name
            repo_clone_url = repo.clone_url  # Use HTTPS URL
            org_dir = backup_dir / org.login
            org_dir.mkdir(parents=True, exist_ok=True)
            local_repo_path = org_dir / repo_name
            clone_or_pull_repo(repo_clone_url, local_repo_path)

    logging.info("Backup process completed successfully.")

if __name__ == "__main__":
    main()
