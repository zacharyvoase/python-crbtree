README.rst: README.md
	pandoc -f markdown -t rst < README.md > README.rst

test:
	nosetests --with-coverage --cover-html --cover-html-dir htmlcov/

.PHONY: test
