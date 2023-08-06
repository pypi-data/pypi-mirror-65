## -*- coding: utf-8 -*-
## :Project:   SoL
## :Created:   gio 10 lug 2014 10:44:12 CEST
## :Author:    Lele Gaifax <lele@metapensiero.it>
## :License:   GNU General Public License version 3 or later
## :Copyright: © 2014, 2018, 2019, 2020 Lele Gaifax
##

<%inherit file="base.mako" />

<%def name="title()">
  ${entity.description}
</%def>

<% ranking = entity.ranking %>

<table class="ui compact definition table">
  <tbody>
    <tr>
      <% level = entity.__class__.__table__.c.level.info['dictionary'][entity.level] %>
      <td class="right aligned">${_('Level')}</td>
      <td>${_(level)}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Tau')}</td>
      <td>${entity.tau}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Default rate')}</td>
      <td>${entity.default_rate}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Default deviation')}</td>
      <td>${entity.default_deviation}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Default volatility')}</td>
      <td>${entity.default_volatility}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Rate range')}</td>
      <td>${entity.lower_rate}—${entity.higher_rate}</td>
    </tr>
    <tr>
      <% outcomes = entity.__class__.__table__.c.outcomes.info['dictionary'][entity.outcomes] %>
      <td class="right aligned">${_('Match outcomes')}</td>
      <td>${_(outcomes)}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Tourneys')}</td>
      <td>${ntourneys}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Players')}</td>
      <td>${len(ranking)}</td>
    </tr>
  </tbody>
</table>

<%def name="ranking_header()">
  <thead>
    <tr>
      <th class="center aligned rank-header">#</th>
      <th class="center aligned player-header">${_('Player')}</th>
      <th class="center aligned sortedby total-header">${_('Rate')}</th>
      <th class="center aligned event-header">${_('Deviation')}</th>
      <th class="center aligned event-header">${_('Volatility')}</th>
      <th class="center aligned event-header">${_('Tourneys')}</th>
    </tr>
  </thead>
</%def>

<%def name="ranking_body(ranking)">
  <tbody>
    % for i, (player, rate, deviation, volatility, nrates) in enumerate(ranking, 1):
    ${ranking_row(i, player, rate, deviation, volatility, nrates)}
    % endfor
  </tbody>
</%def>

<%def name="ranking_row(rank, player, rate, deviation, volatility, nrates)">
    <tr>
      <td class="right aligned rank">${rank}</td>
      <td class="center aligned player">
        <a href="${request.route_path('svg_ratingchart', id=entity.guid, _query=dict(player=player.guid)) | n}" title="${_('Show rates chart')}">
          ${player.caption(html=False)}
        </a>
      </td>
      <td class="right aligned sortedby total">${rate}</td>
      <td class="right aligned event">${deviation}</td>
      <td class="right aligned event">${'%.05f' % volatility}</td>
      <td class="right aligned event">${nrates}</td>
    </tr>
</%def>

<table class="ui stripped compact table ranking">
  <caption>
    ${_('Ranking')} (<a href="${request.route_path('pdf_ratingranking', id=entity.guid) | n}">pdf</a>)
  </caption>
  ${ranking_header()}
  ${ranking_body(ranking)}
</table>
