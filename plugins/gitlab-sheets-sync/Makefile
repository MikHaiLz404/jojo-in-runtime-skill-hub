.PHONY: help install sync setup clean

SERVICE_ACCOUNT_FILE = api/claude-service-account.json
CONFIG_FILE = data/sync_config.json

help:
	@echo "GitLab → Google Sheets Sync Plugin"
	@echo "=================================="
	@echo "make sync      - Sync GitLab issues to spreadsheet"
	@echo "make setup    - Run interactive setup"
	@echo "make install  - Install dependencies"
	@echo "make clean    - Clean cached data"

install:
	pip install -r requirements.txt

sync:
	python3 sync_gitlab_to_sheets.py

setup:
	python3 sync_gitlab_to_sheets.py --setup

clean:
	rm -f $(CONFIG_FILE)
	rm -f api/token.pickle
	@echo "Cleaned plugin data"

copy-creds:
	@if [ -f "$(SERVICE_ACCOUNT_FILE)" ]; then \
		echo "Service account already exists"; \
	else \
		echo "Place your service account JSON at $(SERVICE_ACCOUNT_FILE)"; \
	fi
