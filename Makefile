clean:
	@echo Cleaning...
	@-rm -rf ./build
	@-rm -rf ./dist
	@-rm -rf ./__pycache__
	@-rm -rf ./any2micronconverter/__pycache__
	@-rm -rf ./*.egg-info
	@echo Done

cleanall: clean

preparewheel:
	pyclean .

build_wheel:
	python3 setup.py sdist bdist_wheel

release: build_wheel

upload:
	@echo Ready to publish release, hit enter to continue
	@read VOID
	@echo Uploading to PyPi...
	twine upload dist/*
	@echo Release published