#!/usr/bin/make -f
 PE := pipenv run
 ST := $(PE) ./setup.py
 DNAME := dist/$(shell $(ST) --name)-$(shell $(ST) --version).tar.gz

test tests:
	@$(ST) test

prepare:
	@pipenv install --dev
update:
	@pipenv update --dev

docs:
	@$(ST) build_sphinx
checkdocs:
	@$(ST) checkdocs

dist: $(DNAME)
$(DNAME):
	@$(ST) sdist

upload: $(DNAME)
	@twine upload $(DNAME)

.PHONY: test tests dist docs
# End of file.
