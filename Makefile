.PHONY: inventory gee-submit gee-status test privacy all

inventory:
	python -m src.data.build_inventory

gee-submit:
	python -m src.features.gee_submit

gee-status:
	python scripts/gee_task_status.py

privacy:
	python scripts/privacy_scan.py

test:
	pytest -q

all:
	bash scripts/run_all.sh

