# -*- coding: utf-8 -*-
# copyright 2018 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-graphql views/forms/actions/components for web ui"""

import functools

from cubicweb.web.views.ajaxcontroller import ajaxfunc
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.view import view_config

from querier import GraphQLQuerier, format_execution_result


@ajaxfunc(output_type='json')
def graphql(self):
    query = self._cw.form.get('query')
    cnx = self._cw.cnx
    results = GraphQLQuerier.execute(cnx, query)
    results = format_execution_result(results)
    return results


def authenticated(func):
    @functools.wraps(func)
    def wrapped(request, *args):
        if request.authenticated_userid is None:
            raise HTTPUnauthorized()
        return func(request, *args)

    return wrapped


@view_config(
    route_name='graphql',
    request_method='GET',
    renderer='json',
)
@authenticated
def graphql_pview(request):
    query = request.params.get('query', '')
    results = GraphQLQuerier.execute(request.cw_cnx, query)
    results = format_execution_result(results)
    return results
