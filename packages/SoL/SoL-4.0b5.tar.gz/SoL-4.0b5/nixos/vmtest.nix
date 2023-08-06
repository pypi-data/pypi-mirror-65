# -*- coding: utf-8 -*-
# :Project:   SoL -- NixOS test VM configuration
# :Created:   dom 29 lug 2018 15:56:32 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   All rights reserved
# :Copyright: © 2018 Alberto Berti
#

{config, pkgs, ...}:

  {
    imports = [
      ./config.nix
    ];

    services.sol.enable = true;
    services.sol.configPath = pkgs.writeText "sol.ini" ''
      [app:main]
      use = egg:sol

      desktop.title = SoL
      desktop.version = dev
      desktop.debug = true
      desktop.domain = sol-client
      desktop.manifest = /var/lib/sol/manifest.json

      available_languages = it fr en en_US

      mako.directories = sol:views

      pyramid.reload_templates = true
      pyramid.debug_authorization = false
      pyramid.debug_notfound = false
      pyramid.debug_routematch = false
      pyramid.default_locale_name = en_GB
      pyramid.includes =
          pyramid_tm
          pyramid_mailer.debug
          metapensiero.sqlalchemy.proxy.pyramid

      session.secret = AmbarabaCiciCoco

      sqlalchemy.url = sqlite:///var/lib/sol/data.db

      # Authentication
      sol.admin.user = admin
      sol.admin.password = admin
      sol.guest.user = guest
      sol.guest.password = guest
      sol.enable_signin = true
      sol.enable_password_reset = true
      sol.signer_secret_key = AbracaDabra

      # For backup/restore manual tests
      sol.portraits_dir = /var/lib/sol/portraits
      sol.emblems_dir = /var/lib/sol/emblems
      sol.backups_dir = /tmp/solbcks

      # Alembic

      # Path to migration scripts
      script_location = alembic

      # Template used to generate migration files
      # file_template = %%(rev)s_%%(slug)s

      # Max length of characters to apply to the
      # "slug" field
      #truncate_slug_length = 40

      # Set to 'true' to run the environment during
      # the 'revision' command, regardless of autogenerate
      # revision_environment = false

      [server:main]
      use = egg:waitress#main
      host = 0.0.0.0
      port = 6996

      ###
      # logging configuration
      # http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/logging.html
      ###

      [loggers]
      keys = root, sol, sqlalchemy, ratings

      [handlers]
      keys = console, ratings

      [formatters]
      keys = generic, simple

      [logger_root]
      level = INFO
      handlers = console

      [logger_sol]
      level = DEBUG
      handlers =
      qualname = sol

      [logger_sqlalchemy]
      level = INFO
      handlers =
      qualname = sqlalchemy.engine
      # "level = INFO" logs SQL queries.
      # "level = DEBUG" logs SQL queries and results.
      # "level = WARN" logs neither.  (Recommended for production systems.)

      [logger_ratings]
      level = DEBUG
      handlers = ratings
      qualname = sol.models.rating

      [handler_console]
      class = StreamHandler
      args = (sys.stderr,)
      level = NOTSET
      formatter = generic

      [handler_ratings]
      class = FileHandler
      args = ('ratings.log',)
      level = DEBUG
      formatter = simple

      [formatter_generic]
      format = %(asctime)s [%(levelname).1s] %(name)s: %(message)s
      datefmt = %H:%M:%S

      [formatter_simple]
      [%(levelname).1s] %(name)s: %(message)s
    '';

    # You need to configure a root filesytem
    fileSystems."/".label = "vmdisk";

    # The test vm name is based on the hostname, so it's nice to set
    # one
    networking = rec {
      hostName = "vmhost";
      domain = "test";
      hosts = {
        "127.0.0.1" = [ "${hostName}.${domain}" "${hostName}" "localhost" ];
      };
      firewall.enable = true;
      # kube-dns needs a dns configured
      nameservers = [ "8.8.8.8 " ];
    };
    # Add a test user who can sudo to the root account for debugging
    users.extraUsers.vm = {
      password = "vm";
      group = "wheel";
      isNormalUser = true;
      createHome = true;
    };
    security.sudo = {
      enable = true;
      wheelNeedsPassword = false;
    };

    i18n = {
      consoleKeyMap = "it";
      defaultLocale = "it_IT.UTF-8";
    };

    # Set your time zone.
    time.timeZone = "Europe/Rome";

    virtualisation = {
      memorySize = 1024;
      diskSize = 1024;
    };
  }
