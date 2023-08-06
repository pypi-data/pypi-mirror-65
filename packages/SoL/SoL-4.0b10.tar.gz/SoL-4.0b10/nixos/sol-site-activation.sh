# -*- coding: utf-8 -*-
# :Project:   SoL -- site home dir manage script
# :Created:   dom 05 gen 2020 16:07:02 CET
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2020 Alberto Berti
# :Copyright: © 2020 Lele Gaifax
#

echo "Running home manage script..."
echo "Policy is \"$POLICY\""

LAST_VERSION=$(cat .last_version || printf "0")

echo "Last version is \"$LAST_VERSION\""
echo "Current version is \"$CURRENT_VERSION\""

# set the home world readable to let nginx serve the files
chmod go+rx .

if [ "$POLICY" = "reset" ]
then
    rm -rf * .last_version
    echo "Data erased obeying reset policy."
fi

cp $SOL_CONFIG_INI config.ini
sed -i 's/#mail_host/mail_host/' config.ini
sed -i 's/#mail_port/mail_port/' config.ini
sed -i "s:%(here)s:$PWD:" config.ini

if [ ! -e  .last_version ]
then
    mkdir portraits emblems backups logs
    # See https://github.com/MrBitBucket/reportlab-mirror/blob/master/src/reportlab/rl_settings.py#L192
    ln -sf /run/current-system/sw/share/X11-fonts $PWD/fonts
    soladmin initialize-db --use-default-alembic-dir config.ini
    echo "Data initialized."
elif [ "$POLICY" = "upgrade" ]
then
    soladmin upgrade-db --use-default-alembic-dir config.ini
    echo "Data upgraded."
fi

echo -n $CURRENT_VERSION > .last_version
