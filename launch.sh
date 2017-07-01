python setup.py install
python setup.py nosetests
sphinx-apidoc xiezhi -o doc -f -e
python setup.py build_sphinx
scrapyd-deploy