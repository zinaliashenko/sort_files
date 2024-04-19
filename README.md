# File Organizer Script

This Python script helps organize files in a specified folder by categorizing them into predefined folders based on their file extensions. It also renames files with Cyrillic characters to Latin characters and replaces special characters with underscores.

## Usage

1. **Prerequisites**:
   - Python 3 installed on your system.
   - Poetry installed. If not, you can install it by following the instructions [here](https://python-poetry.org/docs/#installation).

2. **Install Dependencies**:
   - Navigate to the directory containing `pyproject.toml` and run:
     ```
     poetry install
     ```

3. **Run the Script**:
   - Execute the script `main.py` in your terminal by providing the path to the folder you want to organize as a command-line argument:
     ```
     python main.py <path_to_folder>
     ```

## Features

- **Folder Creation**: Predefined folders such as "images", "videos", "documents", "music", "archives", and "unknowns" are created automatically if they don't exist in the specified folder.

- **File Sorting**: Files are sorted into respective folders based on their file extensions.

- **File Normalization**: Files with Cyrillic characters in their names are renamed to use Latin characters. Special characters are replaced with underscores.

- **Logging**: Detailed logs are generated both in the console and a log file (`app.log`). Logs include information about file movements, renaming, and any errors encountered during the process.

## Script Structure

- `main.py`: Main script that orchestrates the file organization process.
- `normalize.py`: Contains functions for normalizing file names.
- `my_logger.py`: Provides logging configuration and setup.

## Logging

The script uses a custom logger to log events at different severity levels:
- **INFO**: Informational messages about the progress of the file organization process.
- **WARNING**: Warnings for events such as file movements and empty directory deletions.
- **ERROR**: Errors encountered during file operations.

## Dependencies

- `os`: For file and directory operations.
- `shutil`: For moving and deleting files.
- `pathlib.Path`: For working with file paths.
- `re`: For regular expressions used in file name normalization.
- `logging`: For generating logs.

## Notes

- Ensure you have appropriate permissions to read, write, and modify files in the specified folder.
- Make sure to back up important files before running the script, especially if it's the first time organizing files in the specified folder.
- Review the logs (`app.log`) for any warnings or errors during the file organization process.

