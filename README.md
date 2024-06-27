# pyls

`pyls` is a Python script that emulates the `ls` command-line utility to list directory contents from a JSON file representing a nested directory structure.

## Features

- Basic listing of directory contents.
- Option to include hidden files.
- Detailed listing format.
- Reverse order listing.
- Sorting by modification time.
- Filtering by files or directories.
- Handling relative paths within the JSON structure.
- Human-readable file sizes.
- Help message for usage instructions.

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` package manager

### Steps

1.  Clone the repository:

        git clone https://github.com/yourusername/pyls.git
        cd pyls

2.  Install the project using `pip`:

        pip install .

## Usage

### Basic Usage

To list the contents of the top-level directory:

    pyls

### Options

- `-A`: Do not ignore entries starting with `.`

      pyls -A

- `-l`: Use a long listing format

      pyls -l

- `-r`: Reverse order while sorting

      pyls -r

- `-t`: Sort by modification time, newest first

      pyls -t

- `--filter=<option>`: Filter output (`dir` or `file`)

      pyls --filter=dir

- `-h`: Show human-readable sizes

      pyls -h

- `--help`: Display help and exit

      pyls --help

### Handling Paths

To list the contents of a subdirectory:

    pyls <subdirectory_path>

To list the details of a specific file:

    pyls -l <file_path>

## Development

### Running Tests

To run the tests, use `pytest`:

    pytest
