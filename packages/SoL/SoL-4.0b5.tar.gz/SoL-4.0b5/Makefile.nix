# -*- coding: utf-8; mode: makefile-gmake -*-
# :Project:   SoL -- Nix targets
# :Created:   sab 21 set 2019 00:01:21 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2019 Alberto Berti
#

NIX := $(shell which nix || echo "$(HOME)/.nix-profile/bin/nix")
RUNVM_TOKEN := .runvm-created
NREBUILD := nixos-rebuild


.PHONY: install_nix
install_nix: $(NIX)

$(NIX):
	@echo "Installing nix..."
	@curl https://nixos.org/nix/install | sh

$(RUNVM_TOKEN): $(PWD)/nixos/vmtest.nix
	NIXOS_CONFIG=$< ${NREBUILD} build-vm
	touch $(@)

.PHONY: run-vm
run-vm: $(RUNVM_TOKEN)
	result/bin/run-vmhost-vm

.PHONY: nix-clean
nix-clean:
	rm -f $(RUNVM_TOKEN)
	rm -rf result*
	rm -f vmhost.qcow2

.PHONY: nix-release
nix-release:
	nix-build release.nix

.PHONY: nix-build-pygal
nix-build-pygal:
	nix-build --keep-failed -A pygal dependencies.nix
