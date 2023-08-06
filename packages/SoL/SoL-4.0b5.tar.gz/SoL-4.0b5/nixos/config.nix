# -*- coding: utf-8 -*-
# :Project:   SoL -- NixOS configuration module
# :Created:   mar 07 ago 2018 11:14:30 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Alberto Berti
# :Copyright: © 2020 Lele Gaifax
#

{ config, lib, pkgs, ... }:

  with lib;
  let
    cfg = config.services.sol;
  in {
    options.services.sol = {
      enable = mkEnableOption "The SoL service for Carrom tournaments management.";
      user = mkOption {
        type = types.str;
        default = "sol";
        description = ''
          User under which the sol service runs.
        '';
      };

      group = mkOption {
        type = types.str;
        default = "sol";
        description = ''
          Group under which the sol service runs.
        '';
      };

      dataDir = mkOption {
        type = types.path;
        default = "/var/lib/sol";
        description = "State directory for the sol service.";
      };

      configPath = mkOption {
        type = types.path;
        example = literalExample ''
          pkgs.writeText "sol.ini" '''
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
          ''';
        '';
        description = ''
          Path to the SoL configuration file.
        '';
      };
      policy = mkOption {
        description = ''
          Policy about site home maintenance:
          none
          do nothing
          reset
          erase and reinit the home dir at each boot
          upgrade
          run the upgrade script at each (re)-boot
        '';
        default = "upgrade";
        type = with types; enum [
          "none"
          "reset"
          "upgrade"
        ];
      };
    };
    config =
      let
        py = pkgs.python3;
        pypkgs = py.pkgs;
        solpkg = (import ../release.nix {inherit pkgs;});
        pyenv = py.buildEnv.override {
          extraLibs = [ solpkg ];
          ignoreCollisions = true;
        };
        runEnv = {
          POLICY = cfg.policy;
          SITE_HOME = cfg.dataDir;
          SOL_CONFIG_INI = cfg.configPath;
          CURRENT_VERSION = solpkg.version;
          PYTHONUNBUFFERED = "1";
        };
      in mkIf cfg.enable {
        environment.systemPackages = [ pyenv ];
        fonts = {
          # this includes DejaVu fonts
          enableDefaultFonts = true;
          # creates a dir with links to the fonts in
          # /run/current-system/sw/share/X11-fonts
          enableFontDir = true;
        };
        users.groups.${cfg.group} = {};
        users.users.${cfg.user} = {
          description = "Sol service user";
          group = cfg.group;
          home = cfg.dataDir;
          createHome = true;
        };

        systemd.services = {
          manage_home = {
            enable = true;
            before = [ "sol.service" ];
            requiredBy = [ "sol.service" ];
            description = ''Handles the initialization and the maintenance of the website home directory.'';
            wantedBy = [
              "multi-user.target"
            ];
            script = (readFile ./sol-site-activation.sh);
            environment = runEnv;
            path = [ solpkg pkgs.gawk ];
            serviceConfig = {
              Group = cfg.group;
              Type = "oneshot";
              User = cfg.user;
              WorkingDirectory = "~";
            };
          };
          sol = {
            wantedBy = [ "multi-user.target" ];
            after = [ "network.target" ];
            unitConfig.RequiresMountsFor = "${cfg.dataDir}";
            serviceConfig = {
              ExecStart = "${pyenv}/bin/pserve ${cfg.dataDir}/config.ini";
              User = cfg.user;
              Group = cfg.group;
              UMask = "0077";
              NoNewPrivileges = true;
              Restart  = "always";
              WorkingDirectory = cfg.dataDir;
            };
          };
        };
      };
    }
