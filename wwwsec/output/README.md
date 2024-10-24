# Output Directory

This directory is used for temporary output files and queue management in the SR_Data visualization system.

## Purpose

- Temporary storage for visualization requests
- Queue management files
- Output logging

## Structure

- `queue.txt`: Active visualization request queue
- Temporary output files (*.txt)
- Log files (automatically cleaned up)

## Usage

The main program monitors this directory for visualization requests and stores temporary output here. Files in this directory are typically temporary and should not be committed to the repository (except for this README).

Note: Most files in this directory are ignored via .gitignore patterns. Only configuration and documentation files should be committed.
