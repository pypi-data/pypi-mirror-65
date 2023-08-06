# -*- coding: utf-8 -*-
# :Project:   SoL -- Nix derivation
# :Created:   sab 04 ago 2018 22:57:25 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Alberto Berti
#
{ pkgs ? import <nixpkgs> {},
  py ? pkgs.python3 }:

  let
    deps = import ./dependencies.nix {
      inherit pkgs;
      pypkgs = py.pkgs;
    };
    pySA13 = py.override {
      packageOverrides = self: super: {
        sqlalchemy = deps.sqlalchemy13;
      };
    };
  in
    pySA13.pkgs.buildPythonPackage rec {
      version = builtins.readFile ./version.txt;
      name = "SoL-${version}";
      src = ./.;
      nativeBuildInputs = (with pkgs; [
        yuicompressor
        gnumake
        which
      ]) ++ (with deps; [
        pySA13.pkgs.Babel
        mp_extjs_desktop
        py.pkgs.sphinx
      ]);
      propagatedBuildInputs = with deps; local_deps ++ system_deps;
      pythonPath = propagatedBuildInputs;
      checkInputs = deps.test_deps;
      checkPhase = ''
        export PATH=$out/bin:$PATH
        # this code runs without locale settings thus Python will use ascii
        # codec to read/write files. This will render loading files containing the
        # '©' simbol impossible
        for pysrc in $(find -name '*.cfg' -or -name '*.ini' -or -name '*.py' -type f)
          do
            substituteInPlace $pysrc --replace © '(c)'
          done
        # avoid pytest's ImportMismatchError
        pytest $NIX_BUILD_TOP
      '';
      doCheck = false;
      medsrc = deps.mp_extjs_desktop + "/lib/${pySA13.libPrefix}/site-packages/metapensiero/extjs/desktop";
      patches = [
        ./nixos/fix_medsrc.patch
        ./nixos/use_nix_yuicompressor.patch
      ];
      preBuild = ''
        substituteAllInPlace Makefile.release
        make compile-catalogs manual minimize
      '';
    }
