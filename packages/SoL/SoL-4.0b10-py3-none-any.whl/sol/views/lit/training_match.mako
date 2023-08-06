## -*- coding: utf-8 -*-
## :Project:   SoL
## :Created:   sab 4 apr 2020, 15:55:04
## :Author:    Lele Gaifax <lele@metapensiero.it>
## :License:   GNU General Public License version 3 or later
## :Copyright: © 2020 Lele Gaifax
##

<%inherit file="base.mako" />

<%def name="title()">
  ${player.caption(html=False)}
</%def>

<%def name="club_emblem(url='', href='')">
  <%
  if championship.club.emblem:
      parent.club_emblem(url="/lit/emblem/%s" % championship.club.emblem,
                         href=championship.club.siteurl,
                         title=championship.club.description)
  %>
</%def>

<%def name="fui_css()">
  ${parent.fui_css()}
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-form.css" />
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-message.css" />
</%def>

## Body

<table class="ui compact definition table">
  <tbody>
    <tr>
      <td class="right aligned">${_('Tourney')}</td>
      <td>
        <a href="${request.route_path('lit_tourney', guid=tourney.guid) | n}" target="_blank">
          ${tourney.description}
        </a>
      </td>
    </tr>
    <tr>
      <td class="right aligned">${_('Turn')}</td>
      <td>${currentturn}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Opponent')}</td>
      <td>
        <a href="${request.route_path('lit_player', guid=opponent.guid) | n}">
          ${opponent.caption(html=False)}
        </a>
        % if player.opponentMatches(opponent):
          (<a href="${request.route_path('lit_player_opponent', guid=player.guid, opponent=opponent.guid)}" target="_blank">${_('previous matches')}</a>)
        % endif
      </td>
    </tr>
  </tbody>
</table>

<div class="ui container">
  <form class="ui centered form${' error' if error else ''}" method="POST">
    % if error:
      <div class="ui error message">
        <div class="header">${_('Error, please correct and retry!')}</div>
        <p>${error}</p>
      </div>
    % endif
    % for board in range(1, championship.trainingboards+1):
      <div class="inline field">
        <label>${_('Board #$number', mapping=dict(number=board))}</label>
        <input type="number" name="errors" min="0" max="99" placeholder="${_('Errors')}">
      </div>
    % endfor
    <button class="ui button" type="submit">${_('Submit')}</button>
  </form>
</div>
