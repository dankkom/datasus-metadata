# datasus-metadata

This repository purpose is to automaticaly fetch DATASUS raw data files' metadata and save it in a JSON file, keeping track of the daily changes in these files on DATASUS' FTP servers for easy metadata retrieval for other systems.

The script is scheduled to run daily and save the metadata in JSON files in the `metadata` directory in this repository.

## Scheduling / Automation

The daily update is handled by a local `systemd` timer (instead of GitHub Actions) to prevent delays and improve reliability. 

To set up the automation on your local machine or server, run the setup script:

```bash
./cron-update.sh install
```

This script will automatically configure and enable a `systemd` user timer scheduled to run every day at **03:00 UTC**.

> **Note:** If running on a server, make sure to enable linger for your user so the timer continues to run even when you are logged out: `sudo loginctl enable-linger $USER`
