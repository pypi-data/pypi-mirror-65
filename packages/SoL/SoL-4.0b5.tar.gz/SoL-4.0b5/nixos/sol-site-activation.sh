# -*- coding: utf-8 -*-
# :Project:   SoL -- site home dir manage script
# :Created:   dom 05 gen 2020 16:07:02 CET
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2020 Alberto Berti
#

echo "Running home manage script..."
echo "Policy is \"$POLICY\""

LAST_VERSION=$(cat .last_version || printf "0")

echo "Last version is \"$LAST_VERSION\""
echo "Current version is \"$CURRENT_VERSION\""

# set the home world readable to let nginx serve the files
chmod go+rx .

if [[ $POLICY == "reset" ]]; then
    rm -rf *
    echo "Data erased."
fi

if [[ -z $(ls) ]]; then
    cp $SOL_CONFIG_INI config.ini
    sed -i 's/#mail_host/mail_host/' config.ini
    sed -i 's/#mail_port/mail_port/' config.ini
    sed -i "s:%(here)s:$PWD:" config.ini
    mkdir portraits emblems backups logs
    soladmin initialize-db --use-default-alembic-dir config.ini
    # See https://github.com/MrBitBucket/reportlab-mirror/blob/master/src/reportlab/rl_settings.py#L192
    ln -sf /run/current-system/sw/share/X11-fonts $PWD/fonts
    echo -n $CURRENT_VERSION > .last_version
    echo "Data initialized"
fi

function version {
    echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }';
}

if [[ ($POLICY == "upgrade") && \
          (( $(version $CURRENT_VERSION) > $(version ${LAST_VERSION:-0}) )) ]]; then
    soladmin upgrade-db --use-default-alembic-dir config.ini
    echo -n $CURRENT_VERSION > .last_version
    echo "Data upgraded."
fi
