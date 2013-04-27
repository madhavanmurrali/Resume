# Dronir's resume builder

Yeah so I needed to write a resume, but couln't find proper tools, 
so of course I made my own tool.

This package includes a python script that reads a resume in 
[TOML](https://github.com/mojombo/toml) and converts it to Markdown,
and a Bash script that calls [Pandoc](http://johnmacfarlane.net/pandoc/)
to convert the Markdown to other formats.

It's very quick and dirty work, and subject to further work or
abandonment as my whims go.

## Requirements

- `pytoml`
- [Pandoc](http://johnmacfarlane.net/pandoc/) for converting Markdown
  to other formats.

## Usage

Currently only generation of a CSS-styled HTML resume is implemented.

Write your own resume in TOML, following example provided. The example
file has comments to explain the features supported.

## To do

- Implement proper LaTeX output.
- More features for the resume.
- Better comments in example
- Fix Unicode strings (this seems to be a `pytoml` issue?)
