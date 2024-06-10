# /bin/sh
# build the docs
sphinx-build -M html docs/source/ docs/build/

# brew install pandoc first
pandoc --from markdown --to rst --no-highlight --embed-resources --standalone  README.md > docs/source/README.rst

# make all diagrams
python3 docs/diagram.py

# make paths to images relative to `README.rst`'s location
python3 docs/replace_readme_dirs.py

