## -*- coding: utf-8 -*-
## :Project:   SoL
## :Created:   sab 13 dic 2008 16:34:51 CET
## :Author:    Lele Gaifax <lele@metapensiero.it>
## :License:   GNU General Public License version 3 or later
## :Copyright: © 2008, 2009, 2010, 2013, 2014, 2016, 2018, 2019, 2020 Lele Gaifax
##

<%inherit file="base.mako" />

<%
from sol.models.utils import njoin
from sol.printouts.utils import ordinal, ordinalp
if entity.championship.playersperteam==1:
    subject = _('Player')
else:
    subject = _('Team')
%>

<%def name="title()">
  ${entity.description}
</%def>

<%def name="header()">
  ${parent.header()}
  <h2 class="subtitle centered">
    <a href="${request.route_path('lit_championship', guid=entity.championship.guid) | n}">
      ${entity.championship.description}
    </a>
  </h2>
</%def>

<%def name="club_emblem(url='', href='')">
  <%
     if entity.championship.club.emblem:
         parent.club_emblem(url="/lit/emblem/%s" % entity.championship.club.emblem,
                            href=entity.championship.club.siteurl,
                            title=entity.championship.club.description)
  %>
</%def>


## Body

<table class="ui compact definition table">
  <tbody>
    <tr>
      <td class="right aligned">${_('Club')}</td>
      <td>
        <a href="${request.route_path('lit_club', guid=entity.championship.club.guid) | n}">
          ${entity.championship.club.description}
        </a>
      </td>
    </tr>
    % if entity.hosting_club:
    <tr>
      <td class="right aligned">${_('Hosted by')}</td>
      <td>
        <a href="${request.route_path('lit_club', guid=entity.hosting_club.guid) | n}">
          ${entity.hosting_club.description}
        </a>
      </td>
    </tr>
    % endif
    <tr>
      <td class="right aligned">${_('Location')}</td>
      <td>${entity.location}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Date')}</td>
      <td>${entity.date.strftime(_('%m-%d-%Y'))}</td>
    </tr>
    <tr>
      <td class="right aligned">${_('Duration')}</td>
      <td>${ngettext('%d minute', '%d minutes', entity.duration) % entity.duration}</td>
    </tr>
    <tr>
      <% cmethod = entity.__class__.__table__.c.couplings.info['dictionary'][entity.couplings] %>
      <td class="right aligned">${_('Coupling method')}</td>
      <td>${_(cmethod)}</td>
    </tr>
    % if entity.delaytoppairing:
      <tr>
        <td class="right aligned">${_('Delay top players pairing')}</td>
        <td>${ngettext('%d turn', '%d turns', entity.delaytoppairing) % entity.delaytoppairing}</td>
      </tr>
    % endif
    <tr>
      <td class="right aligned">${_('Delay compatriots pairing')}</td>
      <td>${_('Yes') if entity.delaycompatriotpairing else _('No')}</td>
    </tr>
    % if entity.finals:
      <tr>
        <td class="right aligned">${ngettext('Final', 'Finals', entity.finals)}</td>
        <td>
          % if entity.finalturns:
            <% firstfinalturn = min(m.turn for m in entity.matches if m.final) %>
            <a href="${request.route_path('lit_tourney', guid=entity.guid, _query=dict(turn=firstfinalturn))}">
          % endif
          ${_('1st/2nd place') if entity.finals==1 else _('1st/2nd place and 3rd/4th place')},
          ${_('single match') if entity.finalkind == 'simple' else _('best of three matches')}
          % if entity.finalturns:
            </a>
          % endif
        </td>
      </tr>
    % endif
    <tr>
      <% pmethod = entity.championship.__class__.__table__.c.prizes.info['dictionary'][entity.championship.prizes] %>
      <td class="right aligned">${_('Prize-giving method')}</td>
      <td>${_(pmethod)}</td>
    </tr>
    % if entity.rating:
      <tr>
        <td class="right aligned">${_('Rating')}</td>
        <td>
          <a href="${request.route_path('lit_rating', guid=entity.rating.guid) | n}">
            ${entity.rating.description}
          </a>
        </td>
      </tr>
    % endif
    % if turn is None:
      <tr>
        <td class="right aligned">${_('Players')}</td>
        <td>${len(entity.ranking)}</td>
      </tr>
    % endif
    % if entity.currentturn:
      <tr>
        <td class="right aligned">${_('Rounds')}</td>
        <td>
          ${', '.join([('<strong>{1}</strong>' if turn==i else '<a href="{0}">{1}</a>').format(
                         request.route_path('lit_tourney', guid=entity.guid, _query=dict(turn=i)), i)
                       for i in range(1,entity.currentturn+1)]) | n}
          (<a href="${request.route_path('pdf_results', id=entity.guid, _query=dict(turn='all')) | n}">pdf</a>,
          <a href="${request.route_path('xlsx_tourney', id=entity.guid) | n}">xlsx</a>)
        </td>
      </tr>
      % if turn is not None:
        <tr>
          <td class="right aligned">${_('Ranked round')}</td>
          <td>
            <a href="${request.route_path('lit_tourney', guid=entity.guid) | n}">
              ${entity.rankedturn}
            </a>
          </td>
        </tr>
      % endif
    % endif
    % if not entity.prized and entity.countdownstarted:
      <tr>
        <td class="right aligned">${_('Currently playing %s round') % ordinal(entity.currentturn)}</td>
        <td>
          <a href="${request.route_path('countdown', _query={'idtourney': entity.idtourney}) | n}" target="_blank">
            ${_('Show countdown')}
          </a>
        </td>
      </tr>
    % endif
  </tbody>
</table>

% if turn is None and player is None:

<%def name="ranking_header()">
  <thead>
    <tr>
      <th class="center aligned rank-header">#</th>
      <th class="player-header">${subject}</th>
      % if entity.rankedturn:
        <th class="center aligned event-header">${_('Points')}</th>
        <th class="center aligned event-header">${_('Bucholz')}</th>
        <th class="center aligned event-header">${_('Net score')}</th>
        <th class="center aligned event-header">${_('Total score')}</th>
      % endif
      % if entity.prized and entity.championship.prizes != 'asis':
        <th class="center aligned sortedby total-header">${_('Final prize')}</th>
      % endif
    </tr>
  </thead>
</%def>

<%def name="ranking_body(ranking)">
  <tbody>
    % for i, row in enumerate(ranking, 1):
      ${ranking_row(i, row)}
    % endfor
  </tbody>
</%def>

<%def name="ranking_row(rank, row)">
  <tr>
    <td class="right aligned rank">${rank}</td>
    <% players = [getattr(row, 'player%d'%i) for i in range(1,5) if getattr(row, 'player%d'%i) is not None] %>
    <td class="player">${njoin(players, stringify=lambda p: '<a href="%s">%s</a>' % (request.route_path('lit_player', guid=p.guid), escape(p.caption(html=False)))) | n}</td>
    % if entity.rankedturn:
      <td class="right aligned event">${row.points}</td>
      <td class="right aligned event">${row.bucholz}</td>
      <td class="right aligned event">${row.netscore}</td>
      <td class="right aligned event">${row.totscore}</td>
    % endif
    % if entity.prized and entity.championship.prizes != 'asis':
      <td class="right aligned sortedby total">${format_prize(row.prize)}</td>
    % endif
  </tr>
</%def>

<% ranking = entity.ranking %>
<table class="ui striped compact table ranking">
  <caption>
    % if entity.prized or entity.date <= today:
      ${_('Ranking')} (<a href="${request.route_path('pdf_tourneyranking', id=entity.guid) | n}">pdf</a>)
    % endif
  </caption>
  ${ranking_header()}
  ${ranking_body(ranking)}
</table>

% else:

<%def name="matches_header()">
  <thead>
    <tr>
      <th class="center aligned rank-header">#</th>
      <th colspan="3" class="center aligned competitors-header">${_('Competitors')}</th>
      <th colspan="3" class="center aligned scores-header">${_('Score')}</th>
    </tr>
  </thead>
</%def>

<%def name="matches_body(matches)">
  <tbody>
    % for i, row in enumerate(matches, 1):
    ${matches_row(i, row)}
    % endfor
  </tbody>
</%def>

<%def name="matches_row(rank, row)">
  <tr>
    <td class="right aligned rank">${rank}</td>
    <%
    ctor = row.competitor1
    players = [ctor.player1, ctor.player2, ctor.player3, ctor.player4]
    %>

    <td class="center aligned competitor1${row.score1>row.score2 and ' winner' or ''}">
      ${njoin(players, stringify=lambda p: '<a href="%s" title="%s">%s</a>' % (
          request.route_path('lit_tourney', guid=row.tourney.guid, _query=dict(player=p.guid)),
          escape(_('Show matches played by %s') % p.caption(html=False)),
          escape(p.caption(html=False)))) | n}
    </td>
    <td class="separator"></td>
    % if row.idcompetitor2:
      <%
      ctor = row.competitor2
      players = [ctor.player1, ctor.player2, ctor.player3, ctor.player4]
      %>
      <td class="center aligned competitor2${row.score1<row.score2 and ' winner' or ''}">
        ${njoin(players, stringify=lambda p: '<a href="%s" title="%s">%s</a>' % (
            request.route_path('lit_tourney', guid=row.tourney.guid, _query=dict(player=p.guid)),
            escape(_('Show matches played by %s') % p.caption(html=False)),
            escape(p.caption(html=False)))) | n}
      </td>
    % else:
      <td class="center aligned phantom">${_('Phantom')}</td>
    % endif
    % if row.score1 == row.score2 == 0 and row.tourney.championship.trainingboards:
      <td class="right aligned" title="${_('Average errors')}">
        ${row.misses1 / row.tourney.championship.trainingboards if row.misses1 else ''}
      </td>
      <td class="separator"></td>
      <td class="right aligned" title="${_('Average errors')}">
        ${row.misses2 / row.tourney.championship.trainingboards if row.misses2 else ''}
      </td>
    % else:
      <td class="right aligned score1${row.score1>row.score2 and ' winner' or ''}">
        ${row.score1 if row.score1 != 0 or row.score2 != 0 else ''}
      </td>
      <td class="separator"></td>
      <td class="right aligned score2${row.score1<row.score2 and ' winner' or ''}">
        ${row.score2 if row.score1 != 0 or row.score2 != 0 else ''}
      </td>
    % endif
  </tr>
</%def>

<%
   if player:
       matches = [m for m in entity.matches
                  if (m.competitor1.player1.guid == player or
                      m.competitor1.player2 and m.competitor1.player2.guid == player or
                      m.competitor1.player3 and m.competitor1.player3.guid == player or
                      m.competitor1.player4 and m.competitor1.player4.guid == player or
                      (m.competitor2 and (m.competitor2.player1.guid == player or
                                          m.competitor2.player2 and m.competitor2.player2.guid == player or
                                          m.competitor2.player3 and m.competitor2.player3.guid == player or
                                          m.competitor2.player4 and m.competitor2.player4.guid == player)))]
       if matches:
           m0 = matches[0]
           if (m0.competitor1.player1.guid == player or
               m0.competitor1.player2 and m0.competitor1.player2.guid == player or
               m0.competitor1.player3 and m0.competitor1.player3.guid == player or
               m0.competitor1.player4 and m0.competitor1.player4.guid == player):
               cname = m0.competitor1.caption(html=False)
           else:
               cname = m0.competitor2.caption(html=False)
           caption = _('Matches played by %s') % (
               '<a href="%s">%s</a>' % (request.route_path('lit_player', guid=player), escape(cname)))
       else:
           caption = _('No matches for this player')
   else:
       matches = [m for m in entity.matches if m.turn == turn]
       if matches:
           caption = (_('Results %s final round (%s)') if matches[0].final else _('Results %s round (%s)')) % (
               ordinalp(turn), '<a href="%s">pdf</a>' % (request.route_path('pdf_results', id=entity.guid,
                                                                  _query=dict(turn=turn))))
       else:
           caption = _('No matches for this turn')
%>

<table class="ui striped compact table matches">
  <caption>${caption | n}</caption>
  ${matches_header()}
  ${matches_body(matches)}
</table>

% endif
