# Package for common utils of avatar ecosystem

#####Install setuptools and wheel
``python -m pip install --user --upgrade setuptools wheel``

#####Generate distribution package
``python setup.py sdist bdist_wheel``

#####Install twine
``python -m pip install --user --upgrade twine``

#####Upload package to index
``python -m twine upload dist/*``