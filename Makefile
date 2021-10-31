ifndef tests
tests="test"
endif


all: docs test lint coverage

venv: venv/bin/activate venv/lib/.deps

venv/bin/activate:
	python3 -m venv venv

.PHONY: deps
deps: venv/lib/.deps

venv/lib/.deps: venv/bin/activate sttp/pkg_meta.py
	. venv/bin/activate \
		&& pip install $$(python3 sttp/pkg_meta.py install_requires)
	touch venv/lib/.deps

.PHONY: dev_deps
dev_deps: venv/lib/.dev_deps

venv/lib/.dev_deps: venv/bin/activate sttp/pkg_meta.py
	. venv/bin/activate \
		&& pip install $$(python3 sttp/pkg_meta.py extras_require dev)
	touch venv/lib/.dev_deps

.PHONY: test
test: venv venv/lib/.dev_deps
	. venv/bin/activate \
		&& python3 -m pytest $(pytest_args) -m "$(mark)" $(tests)

.PHONY: test_watch
test_watch: venv venv/lib/.dev_deps
	. venv/bin/activate \
		&& ptw -- $(pytest_args) -m "$(mark)" $(tests)

.PHONY: coverage
coverage: venv venv/lib/.dev_deps
	. venv/bin/activate \
		&& coverage run --branch --source=sttp -m pytest $(pytest_args) -m "not soak" $(tests) \
		&& coverage report \
		&& coverage html \
		&& coverage xml

.PHONY: docs
docs: venv venv/lib/.dev_deps doctest
	. venv/bin/activate \
		&& make -C docs clean html

.PHONY: doctest
doctest: venv venv/lib/.dev_deps
	. venv/bin/activate \
		&& python3 -m doctest -f $$(find docs/source -type f -name '*.rst')

.PHONY: lint
lint: venv venv/lib/.dev_deps
	. venv/bin/activate \
		&& black --check --line-length 120 --skip-string-normalization sttp test

.PHONY: clean
clean:
	rm -rf ./venv ./*.egg-info ./build ./pip_dist ./htmlcov ./coverage.xml \
		$$(find sttp -name __pycache__) $$(find sttp -name '*.pyc') \
		$$(find test -name __pycache__) $$(find test -name '*.pyc')
	make -C docs clean

.PHONY: dist
dist: venv
	. venv/bin/activate \
		&& pip install setuptools wheel \
		&& python3 setup.py sdist bdist_wheel
