#!/bin/sh
pre-commit run -a autoflake
pre-commit run -a seed-isort-config
pre-commit run -a isort
pre-commit run -a black
pre-commit run -a flake8
