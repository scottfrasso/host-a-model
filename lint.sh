#!/bin/bash

/workspaces/host-a-model/server/venv/bin/python -m pylint $(git ls-files '*.py')