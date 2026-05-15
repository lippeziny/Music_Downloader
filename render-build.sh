#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Instala ffmpeg se não existir (Render usa Ubuntu)
if ! command -v ffmpeg &> /dev/null
then
    apt-get update && apt-get install -y ffmpeg
fi
