# stackedit-extract

https://stackedit.io/ is an online markdown editor I use to take some of my notes. I have workspaces synced to Google Drive. Unfortunately this does not show up as folders and markdown files in Google Drive. Instead it's stored in some key-value storage hidden to the normal UI. Okay maybe I'm wrong on that but ¯\\\_(ツ)\_/¯; I just want a quick way to convert my existing notes collection to, guess what, **plain old folders and markdown files**, so that I can try out one of these Zettelkasten editors out there (like https://zettlr.com).

## Usage

1.  Install python and poetry: https://python-poetry.org/

2.  In StackEdit, find the "export workspace backup" feature; it will give you a single JSON file with all your notes.

3.  Clone this repo, and:
    ```sh
    poetry install
    poetry run stackedit-extract "$workspace_backup_json_file" -o $output_dir
    ```
