# tests/test_pyls.py

import pytest
import json
from io import StringIO
from contextlib import redirect_stdout
from pyls import list_directory, navigate_to_path, load_json


@pytest.fixture
def structure():
    return {
        "name": "interpreter",
        "size": 4096,
        "time_modified": 1699957865,
        "permissions": "-rw-r--r--",
        "contents": [
            {
                "name": ".gitignore",
                "size": 8911,
                "time_modified": 1699941437,
                "permissions": "drwxr-xr-x",
            },
            {
                "name": "LICENSE",
                "size": 1071,
                "time_modified": 1699941437,
                "permissions": "drwxr-xr-x",
            },
            {
                "name": "README.md",
                "size": 83,
                "time_modified": 1699941437,
                "permissions": "drwxr-xr-x",
            },
            {
                "name": "ast",
                "size": 4096,
                "time_modified": 1699957739,
                "permissions": "-rw-r--r--",
                "contents": [
                    {
                        "name": "go.mod",
                        "size": 225,
                        "time_modified": 1699957780,
                        "permissions": "-rw-r--r--",
                    },
                    {
                        "name": "ast.go",
                        "size": 837,
                        "time_modified": 1699957719,
                        "permissions": "drwxr-xr-x",
                    },
                ],
            },
            {
                "name": "go.mod",
                "size": 60,
                "time_modified": 1699950073,
                "permissions": "drwxr-xr-x",
            },
            {
                "name": "lexer",
                "size": 4096,
                "time_modified": 1699955487,
                "permissions": "drwxr-xr-x",
                "contents": [
                    {
                        "name": "lexer_test.go",
                        "size": 1729,
                        "time_modified": 1699955126,
                        "permissions": "drwxr-xr-x",
                    },
                    {
                        "name": "go.mod",
                        "size": 227,
                        "time_modified": 1699944819,
                        "permissions": "-rw-r--r--",
                    },
                    {
                        "name": "lexer.go",
                        "size": 2886,
                        "time_modified": 1699955487,
                        "permissions": "drwxr-xr-x",
                    },
                ],
            },
            {
                "name": "main.go",
                "size": 74,
                "time_modified": 1699950453,
                "permissions": "-rw-r--r--",
            },
            {
                "name": "parser",
                "size": 4096,
                "time_modified": 1700205662,
                "permissions": "drwxr-xr-x",
                "contents": [
                    {
                        "name": "parser_test.go",
                        "size": 1342,
                        "time_modified": 1700205662,
                        "permissions": "drwxr-xr-x",
                    },
                    {
                        "name": "parser.go",
                        "size": 1622,
                        "time_modified": 1700202950,
                        "permissions": "-rw-r--r--",
                    },
                    {
                        "name": "go.mod",
                        "size": 533,
                        "time_modified": 1699958000,
                        "permissions": "drwxr-xr-x",
                    },
                ],
            },
            {
                "name": "token",
                "size": 4096,
                "time_modified": 1699954070,
                "permissions": "-rw-r--r--",
                "contents": [
                    {
                        "name": "token.go",
                        "size": 910,
                        "time_modified": 1699954070,
                        "permissions": "-rw-r--r--",
                    },
                    {
                        "name": "go.mod",
                        "size": 66,
                        "time_modified": 1699944730,
                        "permissions": "drwxr-xr-x",
                    },
                ],
            },
        ],
    }


def test_ls_basic(structure):
    f = StringIO()
    with redirect_stdout(f):
        list_directory(structure)
    out = f.getvalue().strip()
    expected = "LICENSE README.md ast go.mod lexer main.go parser token"
    assert out == expected


def test_ls_A(structure):
    f = StringIO()
    with redirect_stdout(f):
        list_directory(structure, show_hidden=True)
    out = f.getvalue().strip()
    expected = ".gitignore LICENSE README.md ast go.mod lexer main.go parser token"
    assert out == expected


def test_ls_l(structure):
    f = StringIO()
    with redirect_stdout(f):
        list_directory(structure, long_format=True)
    out = f.getvalue().strip()
    expected = """-rw-r--r-- 1071 Nov 14 11:27 LICENSE
-rw-r--r-- 83 Nov 14 11:27 README.md
-rw-r--r-- 4096 Nov 14 15:58 ast
-rw-r--r-- 60 Nov 14 13:51 go.mod
-rw-r--r-- 4096 Nov 14 15:21 lexer
-rw-r--r-- 74 Nov 14 13:57 main.go
-rw-r--r-- 4096 Nov 17 12:51 parser
-rw-r--r-- 4096 Nov 14 14:57 token"""
    assert out == expected


def test_ls_r(structure):
    f = StringIO()
    with redirect_stdout(f):
        list_directory(structure, reverse=True)
    out = f.getvalue().strip()
    expected = "token parser main.go lexer go.mod ast README.md LICENSE"
    assert out == expected


def test_ls_filter_file(structure):
    f = StringIO()
    with redirect_stdout(f):
        list_directory(structure, filter_by="file")
    out = f.getvalue().strip()
    expected = "LICENSE README.md go.mod main.go"
    assert out == expected


def test_ls_filter_dir(structure):
    f = StringIO()
    with redirect_stdout(f):
        list_directory(structure, filter_by="dir")
    out = f.getvalue().strip()
    expected = "ast lexer parser token"
    assert out == expected


def test_ls_invalid_filter(structure):
    f = StringIO()
    with redirect_stdout(f):
        list_directory(structure, filter_by="folder")
    out = f.getvalue().strip()
    expected = "error: 'folder' is not a valid filter criteria. Available filters are 'dir' and 'file'"
    assert out == expected


def test_ls_path(structure):
    path = "parser"
    sub_directory = navigate_to_path(structure, path)
    f = StringIO()
    with redirect_stdout(f):
        list_directory(sub_directory, long_format=True)
    out = f.getvalue().strip()
    expected = """-rw-r--r-- 533 Nov 14 16:03 go.mod
-rw-r--r-- 1.6K Nov 17 12:05 parser.go
-rw-r--r-- 1.4K Nov 17 12:51 parser_test.go"""
    assert out == expected


def test_ls_invalid_path(structure):
    path = "non_existent_path"
    f = StringIO()
    with redirect_stdout(f):
        result = navigate_to_path(structure, path)
    out = f.getvalue().strip()
    expected = "error: cannot access 'non_existent_path': No such file or directory"
    assert out == expected
    assert result is None
