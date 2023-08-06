# Package for common utils of avatar ecosystem

#####Install setuptools and wheel
``pip install setuptools wheel``

#####Generate distribution package
``python setup.py sdist bdist_wheel``

#####Install twine
``pip install twine``

#####Upload package to index
``python -m twine upload dist/*``