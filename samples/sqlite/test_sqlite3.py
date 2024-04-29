from __future__ import annotations

import sqlite3

# examples from python documentation

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.executescript(
    """
    create table person(
        firstname,
        lastname,
        age
    );

    create table book(
        title,
        author,
        published
    );

    insert into book(title, author, published)
    values (
        'Dirk Gently''s Holistic Detective Agency',
        'Douglas Adams',
        1987
    );
    """
)
with open("dump.sql", "w") as f:
    for line in con.iterdump():
        f.write(f"{line}\n")

print("dump.sql created")
con.close()
