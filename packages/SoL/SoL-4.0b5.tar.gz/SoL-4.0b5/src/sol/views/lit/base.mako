## -*- coding: utf-8 -*-
## :Project:   SoL
## :Created:   sab 13 dic 2008 16:33:31 CET
## :Author:    Lele Gaifax <lele@metapensiero.it>
## :License:   GNU General Public License version 3 or later
## :Copyright: © 2008, 2010, 2013, 2014, 2018, 2020 Lele Gaifax
##

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<%!
from datetime import datetime
%>

<html xmlns="http://www.w3.org/1999/xhtml">
  ${self.head()}

  <body>
    <div class="header">
      ${self.header()}
    </div>

    ${self.body()}

    <div class="footer">
      ${self.footer()}
    </div>
  </body>
</html>

<%def name="fui_css()">
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-card.css" />
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-image.css" />
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-statistic.css" />
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-table.css" />
  <link rel="stylesheet" type="text/css" href="/static/css/lit.css" />
</%def>

<%def name="head()">
  <head profile="http://www.w3.org/2005/10/profile">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <base href="/lit/" />
    <title>${self.title()}</title>
    <link rel="icon" type="image/png" href="/static/favicon.png" />
    ${self.fui_css()}
  </head>
</%def>

<%def name="header()">
  ${self.logo()}
  <h1 class="title centered">${self.title()}</h1>
  ${self.club_emblem()}
</%def>

<%def name="logo(url='/static/images/logo.png', href='../lit')">
  <div id="sol_logo">
    <a href="${href}">
      <img class="logo" src="${url}" title="${_('Summary')}"/>
    </a>
  </div>
</%def>

<%def name="club_emblem(url='', href='', title='', target='_blank')">
  % if url:
    <div id="club_emblem">
      <a href="${href or ''}" target="${target}">
        <img id="emblem" src="${url}" title="${title}" />
      </a>
    </div>
  % endif
</%def>

<%def name="footer()">
  <hr />
  <span id="producer">
    <a href="https://gitlab.com/metapensiero/SoL">
      ${_('Scarry On Line')} ${_('version')} ${version}
    </a>
  </span>
  <span id="generated">
    ${datetime.now().strftime(_('%m-%d-%Y %I:%M %p'))}
  </span>
</%def>
