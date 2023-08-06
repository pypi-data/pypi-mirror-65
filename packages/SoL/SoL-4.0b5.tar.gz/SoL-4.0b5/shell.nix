# -*- coding: utf-8 -*-
# :Project:   SoL -- nix environment
# :Created:   sab 04 ago 2018 22:57:25 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Alberto Berti
# :Copyright: © 2020 Lele Gaifax
#

let
  inherit (import <nixpkgs> {}) mkShell;
  sol = import ./release.nix {};
  deps = import ./dependencies.nix {};
in
  mkShell {
    inputsFrom = [ sol ];
    buildInputs = deps.all_deps;
    shellHook = "";
}
