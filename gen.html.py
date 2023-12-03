#!/bin/python3

import json
from operator import itemgetter
import locale

"""
https://lehrerfortbildung-bw.de/u_sprachlit/deutsch/gym/bp2016/fb13/index.html
gedicht // interpretation
"""

filename = 'input.json'
ranks = ["LF", "BF", "10"]
# url_prefix = "../../u_sprachlit/deutsch/gym/bp2016/fb13/2_alle/"
url_prefix = "../../2_alle/"


def print_book_year(book):
    output = f"<p><a class=\"intern\" href=\"{url_prefix}{book['url']}\">{book['year']} {book['first_name']} {book['last_name']} \"{book['title']}\"</a></p>\n"
    return output


def print_book_author(book):
    output = f"<p><a class=\"intern\" href=\"{url_prefix}{book['url']}\">{book['last_name']}, {book['first_name']} ({book['year']}) \"{book['title']}\"</a></p>\n"
    return output


# TODO: maybe not needed at all, could probably just use print_book_year as well for tag view
def print_book_tag(book):
    output = f"<li><a href=\"{url_prefix}{book['url']}\" class=\"intern\">{book['year']} {book['first_name']} {book['last_name']} \"{book['title']}\"</a></li>\n"
    return output


def print_tag_header(tag):
    output = f"<h4 id={tag.replace(' ','_')}>{tag}</h4>\n<ul class=\"linkList\">\n"
    return output


with open(filename) as json_file:
    data = json.load(json_file)

# put all tags in list for each level
all_10_tags = []
all_BF_tags = []
all_LF_tags = []
for book in data:
    taglist = book['tags'].split(', ')
    for tag in taglist:
        if "10" in book['level'] and tag != "":
            all_10_tags.append(tag.strip())
        if "BF" in book['level'] and tag != "":
            all_BF_tags.append(tag.strip())
        if "LF" in book['level'] and tag != "":
            all_LF_tags.append(tag.strip())

# uniquify
all_10_tags = sorted(list(set(all_10_tags)))
all_BF_tags = sorted(list(set(all_BF_tags)))
all_LF_tags = sorted(list(set(all_LF_tags)))

print(f"all_10_tags: {len(all_10_tags)}\n{all_10_tags}")
print(f"all_BF_tags: {len(all_BF_tags)}\n{all_BF_tags}")
print(f"all_LF_tags: {len(all_LF_tags)}\n{all_LF_tags}")

print("sorted:")
# sort (Post-)-Kolonialismus at P and Österreich at O
locale.setlocale(locale.LC_ALL, 'de_DE')
all_10_tags.sort(key=locale.strxfrm)
all_BF_tags.sort(key=locale.strxfrm)
all_LF_tags.sort(key=locale.strxfrm)
print(f"all_10_tags: {len(all_10_tags)}\n{all_10_tags}")
print(f"all_BF_tags: {len(all_BF_tags)}\n{all_BF_tags}")
print(f"all_LF_tags: {len(all_LF_tags)}\n{all_LF_tags}")

"""
print(f"all_10_tags: {len(all_10_tags)}")
print(all_10_tags)
print(f"all_BF_tags: {len(all_BF_tags)}")
print(all_BF_tags)
print(f"all_LF_tags: {len(all_LF_tags)}")
print(all_LF_tags)
"""


# sort list of books by year
# https://stackoverflow.com/questions/72899/how-to-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
data = sorted(data, key=itemgetter('year'))
for book in data:
    # 10, BF, LF
    for rank in ranks:
        if rank in book['level'] and book['url']:
            with open(f"{rank}_nach_jahren.html", 'a') as file_object:
                file_object.write(print_book_year(book))

# sort list of books by author
data = sorted(data, key=itemgetter('last_name'))
for book in data:
    # 10, BF, LF
    for rank in ranks:
        if rank in book['level'] and book['url']:
            with open(f"{rank}_nach_autoren.html", 'a') as file_object:
                file_object.write(print_book_author(book))

# sort list of books by tag
data = sorted(data, key=itemgetter('year'))

# TODO: code duplication starting here

# level 10: overview of all tags
output = "10_nach_schlagwoertern.html"
with open(output, 'a') as file_object:
    file_object.write("<ul class=\"linkList col-count-2\">\n")
for tag in all_10_tags:
    with open(output, 'a') as file_object:
        file_object.write(f"<li><a href=\"#{tag.replace(' ','_')}\">{tag}</a></li>\n")
with open(output, 'a') as file_object:
    file_object.write("</ul>\n")

# level 10: books for each tag
for tag in all_10_tags:
    with open(output, 'a') as file_object:
        file_object.write(print_tag_header(tag))
    for book in data:
        if "10" in book['level'] and tag in book['tags']:
            with open(output, 'a') as file_object:
                file_object.write(print_book_tag(book))
    with open(output, 'a') as file_object:
        file_object.write(f"</ul>\n")


# level BF: overview of all tags
output = "BF_nach_schlagwoertern.html"
with open(output, 'a') as file_object:
    file_object.write("<ul class=\"linkList col-count-2\">\n")
for tag in all_BF_tags:
    with open(output, 'a') as file_object:
        file_object.write(f"<li><a href=\"#{tag.replace(' ','_')}\">{tag}</a></li>\n")
with open(output, 'a') as file_object:
    file_object.write("</ul>\n")

# level BF: books for each tag
for tag in all_BF_tags:
    with open(output, 'a') as file_object:
        file_object.write(print_tag_header(tag))
    for book in data:
        if "BF" in book['level'] and tag in book['tags']:
            with open(output, 'a') as file_object:
                file_object.write(print_book_tag(book))
    with open(output, 'a') as file_object:
        file_object.write(f"</ul>\n")


# level LF: overview of all tags
output = "LF_nach_schlagwoertern.html"
with open(output, 'a') as file_object:
    file_object.write("<ul class=\"linkList col-count-2\">\n")
for tag in all_LF_tags:
    with open(output, 'a') as file_object:
        file_object.write(f"<li><a href=\"#{tag.replace(' ','_')}\">{tag}</a></li>\n")
with open(output, 'a') as file_object:
    file_object.write("</ul>\n")

# level LF: books for each tag
for tag in all_LF_tags:
    with open(output, 'a') as file_object:
        file_object.write(print_tag_header(tag))
    for book in data:
        if "LF" in book['level'] and tag in book['tags']:
            with open(output, 'a') as file_object:
                file_object.write(print_book_tag(book))
    with open(output, 'a') as file_object:
        file_object.write(f"</ul>\n")
