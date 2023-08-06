# -*- coding: utf-8 -*-
# :Project:   SoL -- Main makefile
# :Created:   sab 08 nov 2008 21:16:39 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2013, 2014, 2015, 2016, 2018, 2019, 2020 Lele Gaifax
#

export TOPDIR := $(CURDIR)
VENVDIR := $(TOPDIR)/env
PYTHON := $(shell which python)
SYS_PYTHON := $(shell which python3.7 || which python3)
SOLSRC := $(TOPDIR)/src/sol
SOLADMIN := $(shell which soladmin)
ALEMBIC = $(shell which alembic) -n app:main -c development.ini
PYTEST := $(shell which pytest)
PIP := $(VENVDIR)/bin/pip
REQUIREMENTS := requirements/*.txt
REQUIREMENTS_TIMESTAMP := $(VENVDIR)/requirements.timestamp


.PHONY: default
default: virtualenv

.PHONY: virtualenv
virtualenv: $(VENVDIR) requirements

$(VENVDIR):
	@$(SYS_PYTHON) -m venv --prompt $(notdir $(TOPDIR)) $@

.PHONY: requirements
requirements: $(REQUIREMENTS_TIMESTAMP)

$(REQUIREMENTS_TIMESTAMP): $(VENVDIR) $(REQUIREMENTS)
	@$(PIP) install -r requirements/development.txt
	@touch $@

.PHONY: clean
clean:
	$(MAKE) -C docs clean
	rm -rf build $(SOLSRC)/static/manual
	rm -f $(PACKED_CSS) $(PACKED_JS)
	-@find docs src -name '*~' -print0 | xargs -r0 rm

.PHONY: distclean
distclean: clean
	rm -f development.db
	rm -f $(VENVDIR)

development.db:
	$(SOLADMIN) initialize-db development.ini
	$(SOLADMIN) restore development.ini

.PHONY: generate-db-migration
generate-db-migration:
	read -p "Enter migration description: " MDESC && \
	  $(ALEMBIC) revision --autogenerate -m "$$MDESC"

.PHONY: upgrade-db
upgrade-db:
	$(SOLADMIN) upgrade-db development.ini

.PHONY: serve
serve: development.db compile-catalogs
	pserve --reload development.ini

.PHONY: test
test: compile-catalogs
	@$(PYTEST)

.PHONY: test-slow
test-slow: compile-catalogs
	@$(PYTEST) --runslow

.PHONY: test-fail-soon
test-fail-soon: compile-catalogs
	@$(PYTEST) -x


include Makefile.i18n
include Makefile.manual
include Makefile.release
include Makefile.docker
include Makefile.nix
