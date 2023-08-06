# -*- coding: utf-8 -*-
# :Project:   SoL -- Tests /lit/* views
# :Created:   sab 07 lug 2018 22:51:56 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018, 2019, 2020 Lele Gaifax
#

import pytest

from itsdangerous import Signer
from sqlalchemy import and_, select
from webtest.app import AppError

from sol.models import Competitor, Match, MergedPlayer, Player


@pytest.fixture
def mergedplayer_fatta(session):
    return session.query(MergedPlayer).filter_by(firstname='Fatta').one()


def test_index(app):
    app.get_route('lit')


def test_latest(app):
    app.get_route('lit_latest')
    app.get_route('lit_latest', _query={'n': 10})
    with pytest.raises(AppError) as e:
        app.get_route('lit_latest', _query={'n': 'x'})
    assert '400' in str(e.value)


def test_championship(app, championship_current):
    app.get_route('lit_championship', guid=championship_current.guid)


def test_tourney(app, tourney_first):
    app.get_route('lit_tourney', guid=tourney_first.guid)
    app.get_route('lit_tourney', guid=tourney_first.guid, _query={'turn': 1})
    app.get_route('lit_tourney', guid=tourney_first.guid,
                  _query={'player': tourney_first.competitors[0].player1.guid})
    app.get_route('lit_tourney', guid=tourney_first.guid,
                  _query={'player': tourney_first.competitors[0].player1.guid,
                          'turn': 1})
    with pytest.raises(AppError) as e:
        app.get_route('lit_tourney', guid=tourney_first.guid,
                      _query={'player': tourney_first.competitors[0].player1.guid,
                              'turn': 'x'})
    assert '400' in str(e.value)


def test_player(anonymous_user, lele_user, player_lele, player_lorenzoh):
    r = anonymous_user.get_route('lit_player', guid=player_lele.guid)
    assert b'Emanuele' in r.body
    r = anonymous_user.get_route('lit_player', guid=player_lorenzoh.guid)
    assert b'Lorenzo' not in r.body
    r = lele_user.get_route('lit_player', guid=player_lorenzoh.guid)
    assert b'Lorenzo' in r.body


def test_merged_player(app, mergedplayer_fatta):
    app.get_route('lit_player', guid=mergedplayer_fatta.guid)


def test_player_matches(app, player_lele, mergedplayer_fatta):
    app.get_route('lit_player_matches', guid=player_lele.guid)
    app.get_route('lit_player_matches', guid=mergedplayer_fatta.guid)


def test_players(app):
    app.get_route('lit_players')


def test_players_listing(app, player_lele):
    app.get_route('lit_players_list', country=player_lele.nationality,
                  _query={'letter': player_lele.lastname[0]})
    app.get_route('lit_players_list', country='None', _query={'letter': 'A'})
    app.get_route('lit_players_list', country='eur', _query={'letter': 'A'})
    app.get_route('lit_players_list', country='ITA')


def test_rating(app, rating_european):
    app.get_route('lit_rating', guid=rating_european.guid)


def test_club(app, club_scr):
    app.get_route('lit_club', guid=club_scr.guid)
    with pytest.raises(AppError) as e:
        app.get_route('lit_club', guid='foo')
    assert '404' in str(e.value)


def test_club_players(app, club_scr):
    app.get_route('lit_club_players', guid=club_scr.guid)


def test_emblem(app):
    response = app.get('/lit/emblem/emblem.png')
    assert response.headers['content-type'].startswith('image')

    with pytest.raises(AppError) as e:
        app.get('/lit/emblem')
    assert '404' in str(e.value)

    with pytest.raises(AppError) as e:
        app.get('/lit/emblem/foo')
    assert '404' in str(e.value)


def test_portrait(app):
    response = app.get('/lit/portrait/portrait.png')
    assert response.headers['content-type'].startswith('image')

    with pytest.raises(AppError) as e:
        app.get('/lit/portrait')
    assert '404' in str(e.value)

    with pytest.raises(AppError) as e:
        app.get('/lit/portrait/foo')
    assert '404' in str(e.value)


def test_opponent(app, session, mergedplayer_fatta):
    mt = Match.__table__
    ct1 = Competitor.__table__.alias('c1')
    ct2 = Competitor.__table__.alias('c2')
    pt1 = Player.__table__.alias('p1')
    pt2 = Player.__table__.alias('p2')
    q = select([pt1.c.guid, pt2.c.guid],
               and_(ct1.c.idplayer1 == pt1.c.idplayer,
                    ct2.c.idplayer1 == pt2.c.idplayer,
                    mt.c.idcompetitor1 == ct1.c.idcompetitor,
                    mt.c.idcompetitor2 == ct2.c.idcompetitor))
    r = session.execute(q).first()
    app.get_route('lit_player_opponent', guid=r[0], opponent=r[1])
    with pytest.raises(AppError) as e:
        app.get_route('lit_player_opponent', guid=r[0], opponent='badc0de')
    assert '404' in str(e.value)

    app.get_route('lit_player_opponent', guid=r[0], opponent=mergedplayer_fatta.guid)
    app.get_route('lit_player_opponent', guid=mergedplayer_fatta.guid, opponent=r[0])


def test_country(app):
    app.get_route('lit_country', country='None')
    app.get_route('lit_country', country='ITA')
    app.get_route('lit_country', country='eur')


def test_training_match(app, session, tourney_corona):
    s = Signer(app.app.registry.settings['sol.signer_secret_key'])

    url = app.route_url('training_match', match=s.sign('0-1').decode('ascii'))
    app.get(url, status=404)
    app.post(url, (('errors', 1),), status=404)

    m1, m2 = tourney_corona.matches

    m1id = m1.idmatch
    m2id = m2.idmatch

    signed_m1_c1 = s.sign('%d-%d' % (m1id, 1)).decode('ascii')
    signed_m1_c2 = s.sign('%d-%d' % (m1id, 2)).decode('ascii')
    signed_m2_c1 = s.sign('%d-%d' % (m2id, 1)).decode('ascii')
    signed_m2_c2 = s.sign('%d-%d' % (m2id, 2)).decode('ascii')

    url = app.route_url('training_match', match=signed_m1_c1 + 'foo')
    app.get(url, status=400)
    app.post(url, (('errors', 1),), status=400)

    app.get_route('training_match', match=signed_m1_c1)
    app.get_route('training_match', match=signed_m1_c2)

    url = app.route_url('training_match', match=signed_m1_c1)
    result = app.post(url, (('errors', 1),), status=200)
    assert 'All boards must be entered' in result.text
    app.post(url, (('errors', 1), ('errors', -1)), status=200)
    assert 'All boards must be entered' in result.text

    app.post(url, (('errors', 1), ('errors', 11)), status=302)

    session.expunge_all()
    m1 = session.query(Match).get(m1id)
    assert m1.score1 == 0
    assert m1.score2 == 0
    assert m1.misses1_1 == 1
    assert m1.misses1_2 == 11
    assert m1.misses1_3 is None
    assert m1.misses2_1 is None

    app.get(url, status=302)

    url = app.route_url('training_match', match=signed_m1_c2)
    app.post(url, (('errors', 21), ('errors', 11)), status=302)

    session.expunge_all()
    m1 = session.query(Match).get(m1id)
    assert m1.score1 == 16
    assert m1.score2 == 6
    assert m1.misses1_1 == 1
    assert m1.misses1_2 == 11
    assert m1.misses1_3 is None
    assert m1.misses2_1 == 21
    assert m1.misses2_2 == 11
    assert m1.misses2_3 is None

    url = app.route_url('training_match', match=signed_m2_c1)
    app.post(url, (('errors', 33), ('errors', 32)), status=302)

    url = app.route_url('training_match', match=signed_m2_c2)
    app.post(url, (('errors', 21), ('errors', 11)), status=302)

    session.expunge_all()
    m2 = session.query(Match).get(m2id)
    assert m2.score1 == 16
    assert m2.score2 == 25
    assert m2.misses1_1 == 33
    assert m2.misses1_2 == 32
    assert m2.misses1_3 is None
    assert m2.misses2_1 == 21
    assert m2.misses2_2 == 11
    assert m2.misses2_3 is None
