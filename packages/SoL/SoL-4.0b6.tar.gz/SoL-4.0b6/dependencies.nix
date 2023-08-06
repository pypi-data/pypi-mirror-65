# -*- coding: utf-8 -*-
# :Project:   SoL -- Derivations for some non packaged dependencies
# :Created:   sab 04 ago 2018 22:57:25 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Alberto Berti
# :Copyright: © 2020 Lele Gaifax
#

{ pkgs ? import <nixpkgs> {},
  pypkgs ? pkgs.python3Packages }: rec {

  calmjs_parse = pypkgs.buildPythonPackage rec {
    pname = "calmjs.parse";
    version = "1.2.4";
    format = "wheel";
    src = pypkgs.fetchPypi {
      inherit pname version format;
      python = "py3";
      sha256 = "708e8952d5cb49a40dbad02db46a8294e9a09c17cb1d37282c7cfe9e1a81c68b";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      ply
    ];
  };

  alembic = pypkgs.buildPythonPackage rec {
    pname = "alembic";
    version = "1.4.2";

    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "035ab00497217628bf5d0be82d664d8713ab13d37b630084da8e1f98facf4dbf";
    };

    buildInputs = with pypkgs; [ pytest pytestcov mock coverage ];
    propagatedBuildInputs = with pypkgs; [
      Mako sqlalchemy13 python-editor
      dateutil setuptools
    ];

    # no traditional test suite
    doCheck = false;

    meta = with pkgs.lib; {
      homepage = https://bitbucket.org/zzzeek/alembic;
      description = "A database migration tool for SQLAlchemy";
      license = licenses.mit;
    };
  };

  mp_extjs_desktop =
    let
      extjs = pkgs.fetchzip {
        url = "http://cdn.sencha.com/ext/gpl/ext-4.2.1-gpl.zip";
        sha256 = "0lp9yrl4ply0xkfi0dx1vy381aj3l758vmfx2vpmfa90d7h7vgbd";
      };
    in
      pypkgs.buildPythonPackage rec {
        inherit extjs;
        pname = "metapensiero.extjs.desktop";
        version = "1.42";
        src = pypkgs.fetchPypi {
          inherit pname version;
          sha256 = "93e069a9f67f87aa81d30f3e6c9a5212092983e496a8417687d0694c7a821c9d";
        };
        doCheck = false;
        buildInputs = with pypkgs; [
          setuptools
        ];
        patches = [
          ./nixos/fix_desktop_compressor_cmd.patch
        ];
        preBuild = ''
          mkdir -p src/metapensiero/extjs/desktop/assets/extjs
          cp -a $extjs/resources $extjs/src $extjs/ext-dev.js src/metapensiero/extjs/desktop/assets/extjs
          substituteInPlace MANIFEST.in --replace "prune src/metapensiero/extjs/desktop/assets/extjs" "recursive-include src/metapensiero/extjs/desktop/assets/extjs *.gif *.png *.jpg *.js *.css"
          substituteAllInPlace src/metapensiero/extjs/desktop/scripts/minifier.py
        '';
        propagatedBuildInputs = [
          pkgs.yuicompressor
          pypkgs.ply
        ];
        yuicompressorBin = pkgs.yuicompressor + "/bin/yuicompressor";
      };

  mp_sa_dbloady = pypkgs.buildPythonPackage rec {
    pname = "metapensiero.sqlalchemy.dbloady";
    version = "2.10";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "c02f79f242bd196b20f24edf4d8150e05a461934e9dd6fd0c7d95cda007bbf64";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      sqlalchemy13 progressbar2 ruamel_yaml
    ];
  };

  mp_sa_proxy = pypkgs.buildPythonPackage rec {
    pname = "metapensiero.sqlalchemy.proxy";
    version = "5.13";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "b97c342d065ab1260dc22da03ae805a62b4ad7e5050f9a3be83620314ac8b73e";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      sqlalchemy13
    ];
  };

  pycountry = pypkgs.buildPythonPackage rec {
    pname = "pycountry";
    version = "19.8.18";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "3c57aa40adcf293d59bebaffbe60d8c39976fba78d846a018dc0c2ec9c6cb3cb";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
    ];
  };

  pygal = let
    cairocffi = pypkgs.cairocffi.overridePythonAttrs (old: {
      doCheck = false;
      buildInputs = [ pypkgs.pytestrunner ];
    });
    cairosvg = pypkgs.cairosvg.overridePythonAttrs (old: {
      doCheck = false;
      buildInputs = [ pypkgs.pytestrunner ];
       propagatedBuildInputs = [ cairocffi ] ++
        (with pypkgs; [ cssselect2 defusedxml pillow tinycss2 ]);
    });
    in pypkgs.pygal.overridePythonAttrs (old: {
      patches = [ ./nixos/py3.7fixes.patch ];
      doCheck = false;
     propagatedBuildInputs = [ cairosvg ] ++
        (with pypkgs; [ tinycss cssselect lxml ]);
    });

  pygal_maps_world = pypkgs.buildPythonPackage rec {
    pname = "pygal_maps_world";
    version = "1.0.2";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "8987fcf7f067b56f40f2f83b4f87baf9456164bbff0995715377020fc533db0f";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pygal
    ];
  };

  python_rapidjson = pypkgs.buildPythonPackage rec {
    pname = "python_rapidjson";
    version = "0.9.1";
    src = pypkgs.fetchPypi {
      inherit version;
      pname = "python-rapidjson";
      sha256 = "ad80bd7e4bb15d9705227630037a433e2e2a7982b54b51de2ebabdd1611394a1";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      pkgs.rapidjson
    ];
  };

  pyramid_tm = pypkgs.buildPythonPackage rec {
    pname = "pyramid_tm";
    version = "2.4";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "5fd6d4ac9181a65ec54e5b280229ed6d8b3ed6a8f5a0bcff05c572751f086533";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pyramid transaction
    ];
  };

  pyramid_mailer = pypkgs.buildPythonPackage rec {
    pname = "pyramid_mailer";
    version = "0.15.1";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "ec0aff54d9179b2aa2922ff82c2016a4dc8d1da5dc3408d6594f0e2096446f9b";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pyramid transaction repoze_sendmail
    ];
  };

  repoze_sendmail = pypkgs.buildPythonPackage rec {
    pname = "repoze.sendmail";
    version = "4.4.1";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "096ln02jr2afk7ab9j2czxqv2ryqq7m86ah572nqplx52iws73ks";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      transaction zope_interface
    ];
  };

  # This is disabled as of 19.09 because of compilation issues brought
  # in by the dependency of sphinx on SQLAlchemy (and the dependency
  # of pyramid on sphinx). This has to be re-evaluated for 20.03.
  #
  # See also:
  # - https://github.com/NixOS/nixpkgs/issues/76593
  # - https://github.com/NixOS/nixpkgs/issues/76602
  #
  # sqlalchemy13 = pypkgs.buildPythonPackage rec {
  #   pname = "SQLAlchemy";
  #   version = "1.3.8";
  #   src = pypkgs.fetchPypi {
  #     inherit pname version;
  #     sha256 = "2f8ff566a4d3a92246d367f2e9cd6ed3edeef670dcd6dda6dfdc9efed88bcd80";
  #   };
  #   doCheck = false;
  # };

  sqlalchemy13 = pypkgs.sqlalchemy;

  zope_sqlalchemy = pypkgs.buildPythonPackage rec {
    pname = "zope.sqlalchemy";
    version = "1.3";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "b9c689d39d83856b5a81ac45dbd3317762bf6a2b576c5dd13aaa2c56e0168154";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      sqlalchemy13
      transaction
      zope_interface
    ];
  };

  system_deps = with pypkgs; [
    Babel
    # TODO: remove the following when switching to Python 3.8
    importlib-metadata
    itsdangerous
    pillow
    pynacl
    pyramid
    pyramid_mako
    reportlab
    ruamel_yaml
    setuptools
    transaction
    waitress
    XlsxWriter
 ];
  local_deps = [
    alembic
    calmjs_parse
    mp_extjs_desktop
    mp_sa_proxy
    pycountry
    pygal_maps_world
    pyramid_mailer
    pyramid_tm
    python_rapidjson
    sqlalchemy13
    zope_sqlalchemy
  ];
  test_deps = [
    mp_sa_dbloady
    pypkgs.pytest
    pypkgs.pytestcov
    pypkgs.webtest
  ];
  all_deps = local_deps ++ system_deps ++ test_deps;
}
