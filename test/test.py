import os
import re
import sys
import fnmatch
import shutil
import socketserver
import http.server
from time import gmtime, strftime
from git import Repo
from pyquery import PyQuery


static_path = os.path.join(os.getcwd(), "raw")


def bust():
    file_regex = re.compile(r".*?(\?.*)")
    # use _ to replace dirs
    for root, _, filenames in os.walk(static_path):
        for filename in filenames:
            if file_regex.match(filename):
                newname = re.sub(r"\?.*", "", filename)
                print("Rename", filename, "=>", newname)
                os.rename(os.path.join(root, filename), os.path.join(root, newname))

    # remove superfluous "index.html" from relative hyperlinks found in text
    abs_url_regex = re.compile(r"^(?:[a-z]+:)?//", flags=re.IGNORECASE)

    def fixLinks(text, parser):
        # JQuery translator
        d = PyQuery(bytes(bytearray(text, encoding="utf-8")), parser=parser)
        
        # fix a tag href property
        for element in d("a"):
            e = PyQuery(element)

            href = e.attr("href")
            if not abs_url_regex.search(href):
                # redirect rss file
                new_href = re.sub(r"rss/index\.html$", "rss/index.rss", href)
                # point index file to / as server location
                new_href = re.sub(r"/index\.html$", "/", new_href)
                e.attr("href", new_href)
                # print("\t", href, "=>", new_href)

        # fix wrong jpgpg case
        for element in d("img"):
            e = PyQuery(element)
            attr_name = "srcset"
            print("img:", e)
            attr = e.attr(attr_name)
            if attr:
                new_attr = re.sub(r"\.jpgg ", ".jpg ", attr)
                new_attr = re.sub(r"\.jpgpg ", ".jpg ", new_attr)
                new_attr = re.sub(r"\.jpgjpg ", ".jpg ", new_attr)
                # upsert element attribute
                e.attr(attr_name, new_attr)
                print("\t", attr, "=>", new_attr)

        if parser == "html":
            return d.html(method="html").encode("utf8")
        return d.__unicode__().encode("utf8")

    # Execute fix on every files !
    for root, _, filenames in os.walk(static_path):
        for filename in fnmatch.filter(filenames, "*.html"):
            filepath = os.path.join(root, filename)
            # default parser
            parser = "html"

            if root.endswith("/rss"):  # rename rss index.html to index.rss
                parser = "xml"
                newfilepath = os.path.join(root, os.path.splitext(filename)[0] + ".rss")
                os.rename(filepath, newfilepath)
                filepath = newfilepath

            with open(filepath, encoding="utf8") as f:
                filetext = f.read()

            print("fixing links in ", filepath)

            newtext = fixLinks(filetext, parser)

            # https://stackoverflow.com/questions/5512811/builtins-typeerror-must-be-str-not-bytes
            with open(filepath, "wb") as f:
                f.write(newtext)


if __name__ == "__main__":
    bust()
