## Deployment
python3 setup.py sdist
pip3 install twine
twine upload dist/*
rm -r dist

