# Redsaver

Redsaver is a Python based tool used for archiving text posts in Subreddits.

## Features

- Archives all the text posts in a Subreddit.
- Saves the archive as an editable and viewable JSON file.
- Updates the archive when rerunning the tool for a successfully archived Subreddit.

## Installation

After cloning the repo on your local system, cd into the directory and install the dependencies by using pip.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 redsaver.py -s <subreddit>
```

Replace <subreddit> with the name of the Subreddit you wish to archive. For example, in order to archive the Subreddit /r/python use the following

```bash
python3 redsaver.py -s python
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)