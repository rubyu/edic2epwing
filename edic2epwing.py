#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import csv
import html
import re


def list_func(func, iterator):
    for item in iterator:
        for res in func(item):
            yield res


def parse_key(key_str):
    if not key_str:
        return []
    en_phrases = parse_en_phrase(key_str)
    return list(set(en_phrases))


def parse_index(index_str):
    first_sep = index_str.index("|")
    en_index_str = index_str[:first_sep].strip()
    ja_index_str = index_str[first_sep+1:].strip()

    en_phrases = list_func(expand_en_optional_phrase, parse_en_phrase(en_index_str)) if en_index_str else []
    ja_phrases = parse_ja_phrase(ja_index_str) if ja_index_str else []
    return list(set(en_phrases)), list(set(ja_phrases))


def parse_en_phrase(index_str):
    yield index_str
    phrases = index_str.split(",")
    if len(phrases) > 1:
        for phrase in phrases:
            yield phrase.strip()


def expand_en_optional_phrase(index_str):
    match = re.search(r"(\([^)]+\)|\[[^\]]+\])", index_str)
    if match:
        p1 = index_str[:match.start()].strip()
        p2 = index_str[:match.start()] + index_str[match.start()+1:match.end()-1]
        left = index_str[match.end():]
        for phrase in expand_en_optional_phrase(left):
            yield p1 + phrase
            yield p2 + phrase
    else:
        yield index_str.strip()


def parse_ja_phrase(index_str):
    match = re.search("［[^］]+］$", index_str)
    if match:
        phrases = expand_ja_optional_phrase(index_str[:match.start()].strip())
        for phrase in phrases:
            yield phrase

        alternatives = index_str[match.start()+1:match.end()-1]
        for alternative in parse_ja_alternative(alternatives):
            yield alternative
    else:
        phrases = expand_ja_optional_phrase(index_str)
        for phrase in phrases:
            yield phrase


def expand_ja_optional_phrase(index_str):
    match = re.search("(（[^）]+）|［[^］]+］)", index_str)
    if match:
        p1 = index_str[:match.start()].strip()
        p2 = index_str[:match.start()] + index_str[match.start()+1:match.end()-1]
        left = index_str[match.end():]
        for phrase in expand_ja_optional_phrase(left):
            yield p1 + phrase
            yield p2 + phrase
    else:
        yield index_str.strip()


def parse_ja_alternative(index_str):
    phrases = index_str.split("｜")
    if len(phrases) > 1:
        for phrase in phrases:
            yield phrase.strip()
    else:
        yield index_str.strip()


def header():
    return """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja" xmlns:lexml="http://www.d-assist.com/lexml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title></title>
<link rel="stylesheet" type="text/css" href="" />
</head>
<body>
"""


def footer():
    return """</body>
</html>    
    """


def remove_duplicate(arr):
    return list(set(arr))


def to_html(row):
    if len(row) < 6:
        return
    id_ = row[0]
    subid = row[1]
    speech = row[2]
    key = row[3]
    index = row[4]
    comment = row[5]
    buffer = []
    if index:
        key_phrases = parse_key(key)
        en_phrases, ja_phrases = parse_index(index)

        buffer.append("<dl>")
        buffer.append(f"<dt id=\"{html.escape(id_)}\">{html.escape(index)}</dt>")
        for phrase in remove_duplicate(key_phrases + en_phrases + ja_phrases):
            buffer.append(f"<lexml:key type=\"headword\">{html.escape(phrase)}</lexml:key>")
        buffer.append(f"<dd><p>{html.escape(comment)}</p></dd>")
        buffer.append("</dl>")

    return "\n".join(buffer)


def convert():
    for path in Path("out").iterdir():
        if path.is_file() and path.suffix == ".csv":
            print(f"[{path.name}]")
            with open(path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                with open(f"{path.stem}.html", "w", encoding="utf-8") as html_file:
                    html_file.write(header())
                    for row in reader:
                        html_file.write(to_html(row))
                    html_file.write(footer())


if __name__ == "__main__":
    convert()
