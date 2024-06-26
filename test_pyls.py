import pytest
import subprocess
import os
import sys


@pytest.fixture(scope="module")
def structure_json_path():
    return os.path.abspath("structure.json")


def run_pyls(args, structure_json_path):
    """
    Wrapper fot pyls to be used in the following testcases

    """
    env = os.environ.copy()
    env["STRUCTURE_JSON"] = structure_json_path
    result = subprocess.run(
        [sys.executable, "-m", "pyls"] + args, env=env, capture_output=True, text=True
    )
    return result.stdout.strip()


def test_ls_basic(structure_json_path):
    """
    Testing output of pyls

    """
    output = run_pyls([], structure_json_path)
    expected = "LICENSE README.md ast go.mod lexer main.go parser token"
    assert output == expected


def test_ls_A(structure_json_path):
    """
    Testing output of pyls -A

    """
    output = run_pyls(["-A"], structure_json_path)
    expected = ".gitignore LICENSE README.md ast go.mod lexer main.go parser token"
    assert output == expected


# TODO: Reformat this long ugly test string into bits
def test_ls_l(structure_json_path):
    """
    Testing output of pyls -l

    """
    output = run_pyls(["-l"], structure_json_path)
    expected = "drwxr-xr-x   1071 Nov 14 11:27 LICENSE\ndrwxr-xr-x     83 Nov 14 11:27 README.md\n-rw-r--r--   4096 Nov 14 15:58 ast\ndrwxr-xr-x     60 Nov 14 13:51 go.mod\ndrwxr-xr-x   4096 Nov 14 15:21 lexer\n-rw-r--r--     74 Nov 14 13:57 main.go\ndrwxr-xr-x   4096 Nov 17 12:51 parser\n-rw-r--r--   4096 Nov 14 14:57 token"
    assert output == expected


def test_ls_r(structure_json_path):
    """
    Testing output of pyls -r

    """
    output = run_pyls(["-r"], structure_json_path)
    expected = "token parser main.go lexer go.mod ast README.md LICENSE"
    assert output == expected


def test_ls_filter_file(structure_json_path):
    """
    Testing output of pyls --filter=file

    """
    output = run_pyls(["--filter=file"], structure_json_path)
    expected = "LICENSE README.md go.mod main.go"
    assert output == expected


def test_ls_filter_dir(structure_json_path):
    """
    Testing output of pyls --filter=dir

    """
    output = run_pyls(["--filter=dir"], structure_json_path)
    expected = "ast lexer parser token"
    assert output == expected


def test_ls_invalid_filter(structure_json_path):
    """
    Testing output of pyls -filter=folder

    """
    output = run_pyls(["--filter=folder"], structure_json_path)
    expected = "error: 'folder' is not a valid filter criteria. Available filters are 'dir' and 'file'"
    assert output == expected


# TODO: Reformat this long ugly test string into bits
def test_ls_path(structure_json_path):
    """
    Testing output of pyls -l path

    """
    output = run_pyls(["-l", "parser"], structure_json_path)
    expected = "drwxr-xr-x    533 Nov 14 16:03 go.mod\n-rw-r--r--   1622 Nov 17 12:05 parser.go\ndrwxr-xr-x   1342 Nov 17 12:51 parser_test.go"
    assert output == expected


def test_ls_invalid_path(structure_json_path):
    """
    Testing output of pyls invalid path

    """
    output = run_pyls(["non_existent_path"], structure_json_path)
    expected = "error: cannot access 'non_existent_path': No such file or directory"
    assert output == expected
