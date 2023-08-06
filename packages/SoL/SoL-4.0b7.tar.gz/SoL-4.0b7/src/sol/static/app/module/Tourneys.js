// -*- coding: utf-8 -*-
// :Project:   SoL -- Tourneys window
// :Created:   dom 19 ott 2008 01:35:43 CEST
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2008, 2009, 2010, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare MP*/
/*jsl:declare SoL*/
/*jsl:declare _*/
/*jsl:declare window*/

Ext.define('SoL.module.Tourneys.Actions', {
    extend: 'MP.action.StoreAware',
    uses: [
        'Ext.Action',
        'MP.form.Panel',
        'MP.window.Notification'
    ],

    statics: {
        EDIT_TOURNEY_ACTION: 'edit_tourney',
        DOWNLOAD_TOURNEY_ACTION: 'download_tourney',
        REPLAY_TOURNEY_ACTION: 'duplicate_tourney',
        SHOW_TOURNEY_ACTION: 'show_tourney',
        SHOW_CHAMPIONSHIP_ACTION: 'show_championship',
        MANAGE_COMPETITORS_ACTION: 'manage_competitors',
        SHOW_LIT_PAGE_ACTION: 'show_lit'
    },

    initActions: function() {
        var me = this,
            ids = me.statics();

        me.callParent();

        me.editTourney = me.addAction(new Ext.Action({
            itemId: ids.EDIT_TOURNEY_ACTION,
            text: _('Modify'),
            tooltip: _('Edit selected tourney.'),
            iconCls: 'edit-record-icon',
            disabled: true,
            needsOneSelectedRow: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0];
                me.showEditTourneyWindow(record);
            }
        }));

        me.showTourney = me.addAction(new Ext.Action({
            itemId: ids.SHOW_TOURNEY_ACTION,
            text: _('Details'),
            tooltip: _('Show details of this tourney.'),
            iconCls: 'show-tourney-detail-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    module = me.module.app.getModule('tourney-win');

                module.createOrShowWindow(record);

                /* Since there is a chance that the tourney gets modified,
                 * close this window to avoid possible disalignments.
                 * This is the simplest thing to do to prevent any
                 * confusion to the user.
                 */

                var desktop = me.module.app.getDesktop(),
                    win = desktop.getWindow(me.module.id);

                if(win) {
                    win.destroy();
                }
            }
        }));

        me.showChampionship = me.addAction(new Ext.Action({
            itemId: ids.SHOW_CHAMPIONSHIP_ACTION,
            text: _('Championship'),
            tooltip: _('Show the championship this tourney belongs.'),
            iconCls: 'championships-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idchampionship = record.get('idchampionship'),
                    module = me.module.app.getModule('championships-win');
                module.createOrShowWindow('tourneys', idchampionship);
            }
        }));

        me.manageTourneyCompetitors = me.addAction(new Ext.Action({
            itemId: ids.MANAGE_COMPETITORS_ACTION,
            text: _('Competitors'),
            tooltip: _("Manage tourney competitors, allowing player substitutions, even after prize-giving.<br>Use with <b>caution</b> only when you <i>know what you're doing</i>!"),
            iconCls: 'edit-user-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idtourney = record.get('idtourney'),
                    tourney = record.get('description'),
                    championship = record.get('Championship'),
                    date = record.get('date'),
                    ppt = record.get('PlayersPerTeam'),
                    module = me.module.app.getModule('competitors-win');

                module.createOrShowWindow(idtourney, tourney, date, championship, ppt);
            }
        }));

        me.duplicateTourney = me.addAction(new Ext.Action({
            itemId: ids.REPLAY_TOURNEY_ACTION,
            text: _('Replay again'),
            tooltip: _('Duplicate selected tourney and its competitors on today.'),
            iconCls: 'replay-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idtourney = record.get('idtourney');

                Ext.Msg.confirm(
                    _('Confirm tourney duplication'),
                    _('The selected tourney, with its competitors but not the matches, will be replicated on the current day. Do you confirm?'),
                    function(response) {
                        if('yes' == response) {
                            Ext.create("MP.window.Notification", {
                                position: 'br',
                                html: _('Replicating selected tourney…'),
                                title: _('Please wait'),
                                iconCls: 'waiting-icon'
                            }).show();

                            Ext.Ajax.request({
                                url: 'tourney/replayToday',
                                params: { idtourney: idtourney },
                                success: function(result) {
                                    var res = Ext.decode(result.responseText),
                                        newid, store, prevOptions;
                                    if(res && res.success) {
                                        Ext.create("MP.window.Notification", {
                                            position: 'br',
                                            iconCls: 'done-icon',
                                            title: _('Done'),
                                            html: res.message
                                        }).show();
                                        newid = res.new_idtourney;
                                        store = me.component.store;
                                        prevOptions = Ext.apply({}, store.lastOptions);
                                        store.reload({
                                            callback: function(records) {
                                                for(var i=0; i<records.length; i++) {
                                                    if(records[i].getId() == newid) {
                                                        me.showEditTourneyWindow(records[i]);
                                                        break;
                                                    }
                                                }
                                                store.lastOptions = prevOptions;
                                            }
                                        });
                                    } else {
                                        Ext.create("MP.window.Notification", {
                                            position: 'br',
                                            iconCls: 'alert-icon',
                                            title: _('Error'),
                                            html: res
                                                ? res.message
                                                : _('Cannot decode JSON object')
                                        }).show();
                                    }
                                },
                                failure: function (result) {
                                    Ext.create("MP.window.Notification", {
                                        position: 'br',
                                        iconCls: 'alert-icon',
                                        title: _('Error'),
                                        html: result.statusText
                                    }).show();
                                }
                            });
                        }
                    }
                );
            }
        }));

        me.downloadTourney = me.addAction(new Ext.Action({
            itemId: ids.DOWNLOAD_TOURNEY_ACTION,
            text: _('Download'),
            tooltip: _('Download this tourney data.'),
            iconCls: 'download-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idtourney = record.get('idtourney'),
                    url = '/bio/dump?idtourney=' + idtourney;

                window.open(url, "_blank");
            }
        }));

        me.showLitPage = me.addAction(new Ext.Action({
            itemId: ids.SHOW_LIT_PAGE_ACTION,
            text: _('Lit page'),
            tooltip: _('Show the corresponding Lit page.'),
            iconCls: 'lit-icon',
            disabled: true,
            needsOneSelectedRow: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    guid = record.get('guid'),
                    url = '/lit/tourney/' + guid;

                window.open(url, "_blank");
            }
        }));
    },

    attachActions: function() {
        var me = this,
            args = [];

        me.callParent();

        var tbar = me.component.child('#ttoolbar');

        if(me.component.noAddAndDelete) {
            args.push(0);
        } else {
            args.push(2);
            args.push(' ');
        }
        args.push(me.editTourney,
                  me.showTourney,
                  me.manageTourneyCompetitors,
                  me.duplicateTourney,
                  me.showChampionship,
                  me.downloadTourney);

        tbar.add.apply(tbar, args);

        me.component.on({
            itemdblclick: function() {
                if(!me.editTourney.isDisabled())
                    me.editTourney.execute();
            }
        });

        me.component.store.on({
            add: function(store, records) {
                //jsl:unused store
                var record = records[0];
                me.showEditTourneyWindow(record);
            }
        });
    },

    shouldDisableAction: function(act) {
        var me = this,
            disable = me.component.shouldDisableAction(act),
            statics = me.statics(),
            currentuser = me.module.app.user;

        if(!disable && !currentuser.is_admin) {
            if(act.itemId == statics.EDIT_TOURNEY_ACTION ||
               act.itemId == statics.MANAGE_COMPETITORS_ACTION) {
                var record = me.component.getSelectionModel().getSelection()[0];

                if(record.get('idowner') !== null
                   && record.get('idowner') !== currentuser.user_id)
                    disable = true;
            }
        }

        return disable;
    },

    showEditTourneyWindow: function(record) {
        var me = this,
            desktop = me.module.app.getDesktop(),
            win = desktop.getWindow('edit-tourney-win');

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        var metadata = me.module.config.metadata,
            size = desktop.getReasonableWindowSize(800, 530),
            editors = metadata.editors({
                '*': {
                    editor: MP.form.Panel.getDefaultEditorSettingsFunction('100%')
                },
                Championship: {
                    editor: {
                        listeners: {
                            beforequery: function(queryPlan) {
                                var store = queryPlan.combo.store;
                                var idclub = me.module.idclub;

                                if(idclub) {
                                    store.addFilter({
                                        id: 'currentclub',
                                        property: 'idclub',
                                        value: idclub,
                                        operator: '='
                                    }, false);
                                }
                            },
                            select: function(combo, records) {
                                // Alter data directly, to avoid triggering data-changed
                                record.data['IDClub'] = records[0].get('idclub');
                            }
                        }
                    }
                },
                Rating: {
                    editor: {
                        // Force re-execution of the query, the championship (and
                        // thus the club id) may have changed
                        queryCaching: false,
                        listeners: {
                            beforequery: function(queryPlan) {
                                var store = queryPlan.combo.store;
                                var idclub = record.get('IDClub');

                                if(idclub) {
                                    store.addFilter({
                                        id: 'currentclub',
                                        property: 'idclub',
                                        value: "NULL," + idclub,
                                        operator: '='
                                    }, false);
                                }
                            }
                        }
                    }
                }
            }),
            form = Ext.create('MP.form.Panel', {
                autoScroll: true,
                fieldDefaults: {
                    labelWidth: 100,
                    margin: '15 10 0 10'
                },
                items: [{
                    xtype: 'container',
                    layout: 'hbox',
                    items: [{
                        xtype: 'container',
                        layout: 'anchor',
                        flex: 1,
                        items: [
                            editors.date,
                            editors.description,
                            editors.Championship,
                            editors.HostingClub,
                            editors.location,
                            editors.phantomscore,
                            editors.finals,
                            editors.finalkind
                        ]
                    }, {
                        xtype: 'container',
                        layout: 'anchor',
                        flex: 1,
                        items: [
                            editors.duration,
                            editors.prealarm,
                            editors.Rating,
                            editors.couplings,
                            editors.delaytoppairing,
                            editors.delaycompatriotpairing,
                            editors.retirements,
                            editors.Owner
                        ]
                    }]
                }],
                buttons: [{
                    text: _('Cancel'),
                    handler: function() {
                        if(record.phantom) {
                            record.store.deleteRecord(record);
                        }
                        win.close();
                    }
                }, {
                    text: _('Confirm'),
                    formBind: true,
                    handler: function() {
                        if(form.isValid()) {
                            form.updateRecord(record);
                            win.close();
                            Ext.create("MP.window.Notification", {
                                position: 't',
                                width: 260,
                                title: _('Changes have been applied…'),
                                html: _('Your changes have been applied <strong>locally</strong>.<br/><br/>To make them permanent you must click on the <blink>Save</blink> button.'),
                                iconCls: 'info-icon'
                            }).show();
                        }
                    }
                }]
            });

        win = desktop.createWindow({
            id: 'edit-tourney-win',
            title: _('Edit tourney'),
            iconCls: me.module.iconCls,
            width: size.width,
            height: size.height,
            modal: true,
            items: form,
            closable: false,
            minimizable: false,
            maximizable: false,
            resizable: false,
            tools: [{
                type: 'help',
                tooltip: _('Show user manual section.'),
                callback: function() {
                    var whsize = desktop.getReasonableWindowSize(800, 640),
                        wh = Ext.create('SoL.window.Help', {
                            width: whsize.width,
                            height: whsize.height,
                            // TRANSLATORS: this is the URL of the manual
                            // page explaining tourney insert/edit
                            help_url: _('/static/manual/en/tourneys.html#insert-and-edit'),
                            title: _('Help on tourney insert/edit')
                        });

                    wh.show();
                }
            }]
        });

        form.loadRecord(record);

        win.show();
    }
});


Ext.define('SoL.module.Tourneys', {
    extend: 'MP.desktop.Module',
    requires: [
        'MP.grid.Panel'
    ],
    uses: [
        'SoL.module.Tourneys.Actions',
        'SoL.module.Users',
        'SoL.window.Help'
    ],

    statics: {
        dateToISO: function(date) {
            var year = '' + date.getFullYear(),
                month = '' + (date.getMonth() + 1),
                day = '' + date.getDate();
            if(month.length < 2) {
                month = '0' + month;
            }
            if(day.length < 2) {
                day = '0' + day;
            }
            return year + '-' + month + '-' + day;
        }
    },

    id: 'tourneys-win',
    iconCls: 'tourneys-icon',
    launcherText: function() {
        return _('Tourneys');
    },
    launcherTooltip: function() {
        return _('<b>Tourneys</b><br />Basic tourneys management.');
    },

    config: {
        xtype: 'editable-grid',
        pageSize: 14,
        autoShowAllEditors: false,
        clicksToEdit: 0,
        dataURL: '/data/tourneys',
        saveChangesURL: '/bio/saveChanges',
        sorters: [{property: 'date', direction: 'DESC'}],
        stripeRows: true,
        selModel: {
            mode: 'MULTI'
        }
    },

    getConfig: function(callback) {
        var me = this,
            cfg = me.config;

        if(!cfg.metadata) {
            MP.data.MetaData.fetch(cfg.dataURL, me, function(metadata) {
                var overrides = {
                    Owner: { filter: false }
                };

                Ext.apply(cfg, {
                    metadata: metadata,
                    fields: metadata.fields(overrides),
                    columns: metadata.columns(overrides, false),
                    idProperty: metadata.primary_key,
                    totalProperty: metadata.count_slot,
                    successProperty: metadata.success_slot,
                    rootProperty: metadata.root_slot,
                    plugins: [
                        Ext.create('SoL.module.Tourneys.Actions',
                                   { module: me }),
                        Ext.create('SoL.module.Users.AssignOwnership',
                                   { module: me })
                    ]
                });
                callback(cfg);
                me.app.on('logout', function() { delete cfg.metadata; }, me, { single: true });
            });
        } else {
            callback(cfg);
        }
    },

    createOrShowWindow: function(caller, id, description, idclub, club, couplings, closed,
                          idrating, rating) {
        var me = this,
            config = me.config,
            desktop = me.app.getDesktop(),
            win = desktop.getWindow(me.id);

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        me.idclub = idclub;

        me.configure(
            [me.getConfig],
            function(done) {
                var size = desktop.getReasonableWindowSize(920, 421, "NE"),
                    filteredOn;

                if(club) {
                    filteredOn = ' (' + Ext.String.format(
                        // TRANSLATORS: this is the explanation on the window title when the
                        // filter is a championship, with its club
                        _('in championship {0}, organized by {1}'),
                        description, club) + ')';
                } else if(description) {
                    var explanation;

                    switch(caller) {
                        case 'championships':
                            // TRANSLATORS: this is the explanation on the window title when
                            // the filter is a championship
                            explanation = _('in championship');
                            break;

                        case 'clubs':
                            // TRANSLATORS: this is the explanation on the window title when
                            // the filter is a club
                            explanation = _('hosted by');
                            break;

                        case 'players':
                            // TRANSLATORS: this is the explanation on the window title when
                            // the filter is a player
                            explanation = _('played by');
                            break;

                        case 'ratings':
                            // TRANSLATORS: this is the explanation on the window title when
                            // the filter is a rating
                            explanation = _('related with');
                            break;

                        case 'users':
                            // TRANSLATORS: this is the explanation on the window title when
                            // the filter is a user
                            explanation = _('owned by');
                            break;

                        default:
                            explanation = '';
                            break;
                    }
                    if(explanation !== '') {
                        explanation += ' ';
                    }
                    filteredOn = ' (' + explanation + description + ')';
                } else {
                    filteredOn = '';
                }

                config = Ext.apply({
                    newRecordData: {
                        date: new Date(),
                        currentturn: 0,
                        rankedturn: 0,
                        prized: false,
                        duration: 45,
                        prealarm: 5,
                        phantomscore: 25,
                        finals: 0,
                        delaytoppairing: 1,
                        delaycompatriotpairing: false,
                        couplings: couplings || 'serial',
                        retirements: 'none'
                    },
                    filters: [{
                        property: 'date',
                        value: SoL.module.Tourneys.dateToISO(new Date()),
                        operator: '<='
                    }]
                }, config);

                if(caller == 'championships') {
                    Ext.apply(config.newRecordData, {
                        idchampionship: id,
                        Championship: description,
                        idrating: idrating,
                        Rating: rating
                    });

                    Ext.apply(config, {
                        noAddAndDelete: closed,
                        stickyFilters: [{
                            property: 'idchampionship',
                            value: id,
                            operator: '='
                        }]
                    });
                } else if(caller == 'ratings') {
                    Ext.apply(config.newRecordData, {
                        idrating: id,
                        Rating: description
                    });

                    Ext.apply(config, {
                        stickyFilters: [{
                            property: 'idrating',
                            value: id,
                            operator: '='
                        }]
                    });
                } else if(caller == 'players') {
                    Ext.apply(config, {
                        noAddAndDelete: true,
                        extraParams: { idplayer: id }
                    });
                } else if(caller == 'users') {
                    Ext.apply(config, {
                        stickyFilters: [{
                            property: 'idowner',
                            value: id,
                            operator: '='
                        }]
                    });
                } else if(caller == 'clubs') {
                    Ext.apply(config, {
                        stickyFilters: [{
                            property: 'idhostingclub',
                            value: id,
                            operator: '='
                        }]
                    });
                }

                win = desktop.createWindow({
                    id: me.id,
                    title: (me.windowTitle || me.getLauncherText()) + filteredOn,
                    taskbuttonTooltip: me.getLauncherTooltip(),
                    iconCls: me.iconCls,
                    items: [config],
                    x: size.x,
                    y: size.y,
                    width: size.width,
                    height: size.height,
                    tools: [{
                        type: 'help',
                        tooltip: _('Show user manual section.'),
                        callback: function() {
                            var whsize = desktop.getReasonableWindowSize(800, 640);
                            var wh = Ext.create('SoL.window.Help', {
                                width: whsize.width,
                                height: whsize.height,
                                // TRANSLATORS: this is the URL of the manual
                                // page explaining tourneys management
                                help_url: _('/static/manual/en/tourneys.html'),
                                title: _('Help on tourneys management')
                            });
                            wh.show();
                        }
                    }]
                });

                var grid = win.child('editable-grid');

                // Fetch the first page of records, and when done show
                // the window
                grid.store.load({
                    params: {start: 0, limit: me.pageSize},
                    callback: function() {
                        win.on({show: done, single: true});
                        win.show();
                    }
                });

                var da = grid.findActionById('delete');
                if(da)
                    da.shouldBeDisabled = me.shouldDisableDeleteAction.bind(grid);
            }
        );
    },

    shouldDisableDeleteAction: function() {
        var grid = this,
            sm = grid.getSelectionModel(),
            currentuser = grid.up().up().app.user;

        if(sm.getCount() > 0) {
            var selrecs = sm.getSelection(),
                disable = false;

            for(var i=selrecs.length-1; i>=0; i--) {
                var record = selrecs[i];

                if(!currentuser.is_admin
                   && record.get('idowner') !== null
                   && currentuser.user_id !== record.get('idowner')) {
                    disable = true;
                    break;
                }
            }
            return disable;
        } else {
            return true;
        }
    }
});


Ext.define('SoL.module.MyTourneys', {
    extend: 'SoL.module.Tourneys',

    id: 'my-tourneys-win',
    iconCls: 'tourneys-icon',
    launcherText: null, // don't show an entry in the start menu

    init: function() {
        var me = this,
            user = me.app.user;

        if(!me.config.orig_dataURL) me.config.orig_dataURL = me.config.dataURL;
        me.config.dataURL = Ext.String.urlAppend(me.config.orig_dataURL,
                                                 'filter_by_idowner=' + (user.is_admin
                                                                         ? 'NULL'
                                                                         : user.user_id));
        me.windowTitle = Ext.String.format(_('Tourneys managed by {0}'), user.fullname);
        me.callParent();
    }
});
