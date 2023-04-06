SHELL := /bin/bash

.PHONY: run
run:
	python3 detector.py

.PHONY: req
req:
	pip3 freeze > requirements.txt


.PHONY: dependencies
dependencies:
	python3 -m pip install ImageHash && \
	python3 -m pip install art && \
	python3 -m pip install opencv_python  && \
	python3 -m pip install numpy && \
	python3 -m pip install Pillow

