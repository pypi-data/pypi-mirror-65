rm -Rf ./dist/*
pip3 install twine
./build.sh
python3 -m twine upload dist/*