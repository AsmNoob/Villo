#!/bin/bash

rm sql/villo.db
sqlite3 sql/villo.db < sql/create.sql
python3 sql/userFileParser.py data/users.xml sql/villo.db
sqlite3 sql/villo.db < sql/import.sql