zo
rm dist/*; python setup.py check && python setup.py install && python setup.py sdist && twine upload dist/*
