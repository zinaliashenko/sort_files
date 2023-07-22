# clean_folder

clean_folder is a Python package sorting files.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install clean_folder.

```bash
pip install clean_folder
python setup.py install clean_folder
```

## Usage

```python
import clean_folder

# renames files and folders
change_the_name(path)

# creates new folders
create_folders(path)

# deletes empty folders
delete_empty_folders(path)

# prints extensions and files info
get_the_info(path)

# returns new_file_name
normalize(file_name)

# sorts files to a proper folder
sort_the_files(list_folders_and_files)

# unpackes archives
unpack_archives(path)

# returns list_folders_and_files
walk_the_directory(path)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
