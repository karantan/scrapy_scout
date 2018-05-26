# convenience makefile

.DEFAULT_GOAL := setup


help:
	@echo "Usage:"
	@echo "    make help        		show this message"
	@echo "    make setup       		create virtual environment and install dependencies"
	@echo "    make activate    		enter virtual environment"
	@echo "    make lint    		    run autopep8 and isort"
	@echo "    exit             		leave virtual environment"

setup:
	@pipenv install --dev

activate:
	@pipenv shell

lint:
	@pipenv run isort -rc -fas -sl scrapy_scout
	@pipenv run autopep8 -i -r scrapy_scout

.PHONY: help setup activate lint
