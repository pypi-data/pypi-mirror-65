# -*- coding: utf-8 -*-
# :Project:   SoL -- load nix into the environment and install it if its necessary
# :Created:   dom 05 ago 2018 15:54:26 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Alberto Berti
#

if [ -z $(which nix) ]; then
    make install_nix
    . $HOME/.nix-profile/etc/profile.d/nix.sh
fi
