# Copyright (C) 2002 - 2018 John Goerzen & contributors.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

# Warning: VERSION, ABBREV and TARGZ are used in docs/build-uploads.sh.
VERSION=$(shell ./offlineimap.py --version)
ABBREV=$(shell git log --format='%h' HEAD~1..)
TARGZ=offlineimap-v$(VERSION)-$(ABBREV)
SHELL=/bin/bash
RST2HTML=`type rst2html >/dev/null 2>&1 && echo rst2html || echo rst2html.py`

all: build

build:
	python2 setup.py build
	@echo
	@echo "Build process finished, run 'python2 setup.py install' to install" \
		"or 'python2 setup.py --help' for more information".

clean:
	-python2 setup.py clean --all
	-rm -f bin/offlineimapc 2>/dev/null
	-find . -name '*.pyc' -exec rm -f {} \;
	-find . -name '*.pygc' -exec rm -f {} \;
	-find . -name '*.class' -exec rm -f {} \;
	-find . -name '.cache*' -exec rm -f {} \;
	-find . -type d -name '__pycache__' -exec rm -rf {} \;
	-rm -f manpage.links manpage.refs 2>/dev/null
	-find . -name auth -exec rm -vf {}/password {}/username \;
	-$(MAKE) -C docs clean

.PHONY: docs
docs:
	@$(MAKE) -C docs

websitedoc:
	@$(MAKE) -C websitedoc

targz: ../$(TARGZ)
../$(TARGZ):
	cd .. && tar -zhcv --transform s,^offlineimap,offlineimap-v$(VERSION), -f $(TARGZ).tar.gz --exclude '.*.swp' --exclude '.*.swo' --exclude '*.pyc' --exclude '__pycache__' offlineimap/{bin,Changelog.md,Changelog.maint.md,contrib,CONTRIBUTING.rst,COPYING,docs,MAINTAINERS.rst,Makefile,MANIFEST.in,offlineimap,offlineimap.conf,offlineimap.conf.minimal,offlineimap.py,README.md,requirements.txt,scripts,setup.cfg,setup.py,snapcraft.yaml,test,tests,TODO.rst}

rpm: targz
	cd .. && sudo rpmbuild -ta $(TARGZ)
