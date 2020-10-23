#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from toast_yify.gateway.file import File as Db
from toast_yify.skeleton import parse_entries_from_html



__author__ = "Ryan Long"
__copyright__ = "Ryan Long"
__license__ = "mit"



@pytest.fixture
def db_file():
    global html_doc
    with open(
            "./../tests/fixtures/view-source_https___yts.lt_browse-movies.html") as html_file:
        html_doc = html_file.read()
        data = parse_entries_from_html(html_doc)
        db = Db("./TOAST_YIFY")
        db.add_entries(data)

def tear_down():
    if os.path.exists("./TOAST_YIFY") and os.path.isfile("./TOAST_YIFY"):
        os.remove("./TOAST_YIFY")


def test_fetch_latest_entries(db_file):
    db = Db("./TOAST_YIFY")
    for row in db.fetch_latest_entries():
        assert row == {
            'categories': 'Comedy, Family',
            'image_url': 'https://img.yts.lt/assets/images/movies/cecil_2019/medium-cover.jpg',
            'name': 'Cecil (2019)',
            'rating': '6.7 / 10',
        }
        break
    tear_down()

def test_add_entry(db_file):
    db = Db("./TOAST_YIFY")
    row = {
        'categories': 'Comedy, Family',
        'image_url': 'https://img.yts.lt/assets/images/movies/cecil_2019/medium-cover.jpg',
        'name': 'Test Film (2019)',
        'rating': '10 / 10',
    }
    db.add_entry(row)
    for entry in db.fetch_latest_entries():
        assert entry == row
    tear_down()

def test_add_entries(db_file):
    db = Db("./TOAST_YIFY")
    rows = [{
        'categories': 'Comedy, Family',
        'image_url': 'https://img.yts.lt/assets/images/movies/cecil_2019/medium-cover.jpg',
        'name': 'Test Comedy Film (2019)',
        'rating': '10 / 10',
    }, {
        'categories': 'Horror, Family',
        'image_url': 'https://anotherwebsite.yts.lt/assets/images/movies/cecil_2019/medium-cover.jpg',
        'name': 'Test Horror Film (2019)',
        'rating': '10 / 10',
    }]
    db.add_entries(rows)
    entries = []
    for entry in db.fetch_latest_entries():
        entries.append(entry)
    assert entries[0] == rows[0]
    assert entries[1] == rows[1]
    tear_down()

