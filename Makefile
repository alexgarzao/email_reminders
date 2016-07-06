# Email reminders
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# Makefile

setup:
	virtualenv .env
	. .env/bin/activate
	pip install -r requirements.txt

tdd:	clean
	nosetests

run:	clean
	python email_reminders/main.py

tests:	clean tdd

checkcode:	lint pep8

lint:
	pylint *.py email_reminders/*.py tests/*.py

pep8:
	pep8 *.py email_reminders/*.py tests/*.py

clean:
	rm -f email_reminders/*.pyc
	rm -f tests/*.pyc
