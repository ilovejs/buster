#!/bin/sh

rm -rf raw/*

wget --recursive \
--convert-links \
--page-requisites        \
--no-parent              \
--directory-prefix   raw    \
--no-host-directories    \
--restrict-file-name=unix \
http://localhost:2368/


# cd raw && python -m http.server --cgi 8001


