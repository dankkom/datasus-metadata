# datasus-metadados

This repository purpose is to automaticaly fetch DATASUS raw data files' metadata and save it in a JSON file, keeping track of the daily changes in these files on DATASUS' FTP servers for easy metadata retrieval for other systems.

It is a simple Python script that uses the `datasus-fetcher` package to connect to the DATASUS FTP servers and fetch the metadata of the files in the directories of interest.

The script is scheduled to run daily and save the metadata in a JSON file in this repository.
