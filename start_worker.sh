#!/usr/bin/env bash

celery -A task_queue worker -l info
