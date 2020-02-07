SHELL := /bin/bash

help:
	@echo " ap8             AutoPEP8 for app"
	@echo " clean           remove unwanted files like .pyc's"
	@echo " git_oneline     Extract the git log to git.log"
	@echo " req_save		Save pip export to requirements.txt"

ap8:
	# . ./venv/bin/activate && \
	autopep8 ./*.py --recursive --in-place --pep8-passes 2000 --max-line-length 90 --verbose --aggressive --aggressive --aggressive
	autopep8 ./simple_base/ --recursive --in-place --pep8-passes 2000 --max-line-length 90 --verbose --aggressive --aggressive --aggressive --ignore E711
	# autopep8 ./app/ --recursive --in-place --pep8-passes 2000 --verbose --aggressive --ignore E402

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;
	find . -name '__pycache__' -exec rmdir --ignore-fail-on-non-empty {} \;

git_oneline:
	git log --pretty=format:"-   %s" > git.log

req_save:
	pip list --format=freeze | tee requirements/all.txt

req_upgrade:
	# pip list --outdated --format=freeze | tee requirements/before_upgrade.txt | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
	pip list --outdated --format=freeze | tee requirements/before_upgrade.txt | egrep -v '^(\-e|#)' | cut -d = -f 1  | xargs -n1 pip install -U
