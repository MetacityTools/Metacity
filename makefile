all: build
.PHONY: build upload clean deploy

#for manual deploy, update the version in setup.py
#commit the changes
#run make build and make upload, you'll need your pypi account

#to automate this, update the version number and run make deploy

#environments
build: clean
	@-( \
		python setup.py sdist bdist_wheel \
	)

upload: 
	@-( \
		rm dist/metacity*; \
		python setup.py sdist; \
		python -m twine upload dist/*; \
	)

deploy: clean
	@-( \
		git add setup.py; \
		git commit -m "Deploying to Pypi.org"; \
		python setup.py sdist bdist_wheel; \
		rm dist/metacity*; \
		python setup.py sdist; \
		python -m twine upload dist/*; \
	)
	

clean:
	@-( \
		find . -type d -not -path "*/env/*" -wholename '*/build' -exec rm -r {} +;\
    	find . -type f -not -path "*/env/*" -name '*.so' -exec rm {} +;\
	)