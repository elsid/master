#!/usr/bin/env bash

pylint $(git ls-files | fgrep .py) | tee pylint.$(date +%s).log
