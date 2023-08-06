## -*- coding: utf-8 -*
## :Project:   SoL -- Top level application page
## :Created:   sab 14 lug 2018 11:34:50 CEST
## :Author:    Lele Gaifax <lele@metapensiero.it>
## :License:   GNU General Public License version 3 or later
## :Copyright: © 2018, 2020 Lele Gaifax
##

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="${locale}" lang="${locale}">
  <head profile="http://www.w3.org/2005/10/profile">
    <link rel="icon" type="image/png" href="/static/favicon.png" />
    % if debug:
      <link rel="stylesheet" type="text/css"
            href="/desktop/extjs/resources/css/ext-all-debug.css" />
      <link rel="stylesheet" type="text/css"
            href="/desktop/css/action.css" />
      <link rel="stylesheet" type="text/css"
            href="/desktop/css/desktop.css" />
      <link rel="stylesheet" type="text/css"
            href="/desktop/css/filterbar.css" />
      <link rel="stylesheet" type="text/css"
            href="/desktop/css/grid.css" />
      <link rel="stylesheet" type="text/css"
            href="/desktop/css/form.css" />
      <link rel="stylesheet" type="text/css"
            href="/desktop/css/upload.css" />
      <link rel="stylesheet" type="text/css"
            href="/static/css/app.css" />
    % else:
      <link rel="stylesheet" type="text/css"
            href="/static/all-styles.css?v=${app_version}" />
    % endif

    <script type="text/javascript">
     __title__ = "${app_title}";
     __version__ = "${app_version}";
     __csrf_token__ = "${get_csrf_token()}";
     __signin__ = ${'true' if signin_enabled else 'false'};
     __password_reset__ = ${'true' if password_reset_enabled else 'false'};
     __admin_email__ = "${admin_email}";
    </script>

    <script type="text/javascript" src="/catalog"></script>

    % if debug:
      <script type="text/javascript" src="/desktop/extjs/ext-dev.js">
      </script>

      <script type="text/javascript">
       Ext.Loader.setConfig({ enabled: true });
      </script>
    % else:
      <script type="text/javascript" src="/static/ext.js">
      </script>

      <script type="text/javascript">
       Ext.Loader.setConfig({ enabled: false });
      </script>

      <script type="text/javascript" src="/static/all-classes.js?v=${app_version}">
      </script>
    % endif

    <script type="text/javascript" src="/static/app.js?v=${app_version}"></script>

    <script type="text/javascript" src="/extjs-l10n"></script>

    <title>${app_title} (${app_version})</title>
  </head>

  <body></body>
</html>
