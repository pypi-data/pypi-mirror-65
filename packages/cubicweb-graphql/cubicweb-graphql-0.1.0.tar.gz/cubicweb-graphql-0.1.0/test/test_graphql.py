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

"""Unit tests for GraphQL"""
from cubicweb import Unauthorized, QueryError
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb_graphql.querier import GraphQLQuerier


class GraphQLBaseTC(CubicWebTC):
    """
    Base test cases for GraphQL security
    """

    def setup_database(self):
        super(GraphQLBaseTC, self).setup_database()
        with self.admin_access.client_cnx() as cnx:
            self.create_user(cnx, u"iaminusersgrouponly")
            self.affaire1 = cnx.execute("INSERT Affaire X: X sujet 'affaire1'")[0][0]
            self.affaire2 = cnx.execute("INSERT Affaire X: X sujet 'affaire2'")[0][0]
            cnx.commit()


class GraphQLSecurityTC(CubicWebTC):
    """
    Suite of security tests for GraphQL (adapted from RQL security test suite)
    """

    def gql_ok(self, connection, query, **kwargs):
        """
        Execute a GraphQL query and assert there was no error
        :param connection: The current connection
        :param query: The query
        :param kwargs: The arguments
        :return: The query's result
        """
        result = GraphQLQuerier.execute(connection, query, **kwargs)
        self.assertIsNotNone(result.data)
        self.assertIsNone(result.errors)
        return result

    def gql_nok(self, connection, query, **kwargs):
        """
        Execute a GraphQL query and assert there was an error
        :param connection: The current connection
        :param query: The query
        :param kwargs: The arguments
        :return: The query's result
        """
        result = GraphQLQuerier.execute(connection, query, **kwargs)
        self.assertIsNotNone(result.errors)
        self.assertTrue(len(result.errors) >= 1)
        return result

    def setUp(self):
        super(GraphQLSecurityTC, self).setUp()
        # implicitly test manager can add some entities
        with self.admin_access.repo_cnx() as cnx:
            self.create_user(cnx, u"iaminusersgrouponly")
            cnx.execute("INSERT Affaire X: X sujet 'cool'")
            cnx.execute("INSERT Societe X: X nom 'logilab'")
            cnx.execute("INSERT Personne X: X nom 'bidule'")
            cnx.execute('INSERT CWGroup X: X name "staff"')
            cnx.commit()

    def test_simple_read(self):
        query = "{ Personne { nom, prenom, sexe } }"
        with self.admin_access.repo_cnx() as cnx:
            result = self.gql_ok(cnx, query)
            self.assertEquals(len(result.data["Personne"]), 1)

    def test_empty_when_cannot_read_simple(self):
        query = "{ Affaire { sujet } }"
        sujet = self.repo.schema["Affaire"].rdef("sujet")
        with self.temporary_permissions((sujet, {'read': ('users', 'managers')})):
            with self.admin_access.repo_cnx() as cnx:
                # Reading is OK for the manager
                result = self.gql_ok(cnx, query)
                self.assertEquals(len(result.data["Affaire"]), 1)
            with self.new_access(u'anon').repo_cnx() as cnx:
                # Reading is not OK for anonymous
                result = self.gql_ok(cnx, query)
                self.assertEquals(len(result.data["Affaire"]), 0)

    def test_empty_when_cannot_read_with_args(self):
        query = "query getAffaire($sujet: String) { Affaire(sujet: $sujet) { sujet } }"
        sujet = self.repo.schema["Affaire"].rdef("sujet")
        with self.temporary_permissions((sujet, {'read': ('users', 'managers')})):
            with self.admin_access.repo_cnx() as cnx:
                # Reading is OK for the manager
                result = self.gql_ok(cnx, query, sujet="cool")
                self.assertEquals(len(result.data["Affaire"]), 1)
            with self.new_access(u'anon').repo_cnx() as cnx:
                # Reading is not OK for anonymous
                result = self.gql_nok(cnx, query, sujet="cool")
                self.assertIsNone(result.data["Affaire"])

    def test_upassword_not_selectable(self):
        query = "{ CWUser { login, upassword } }"
        with self.admin_access.repo_cnx() as cnx:
            result = self.gql_ok(cnx, query)
            self.assertEqual(len(result.data["CWUser"]), 3)
            for user in result.data["CWUser"]:
                self.assertIsNone(user["upassword"])
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            result = self.gql_ok(cnx, query)
            self.assertEqual(len(result.data["CWUser"]), 3)
            for user in result.data["CWUser"]:
                self.assertIsNone(user["upassword"])

    def test_read_erqlexpr(self):
        """
        Test the application of security constraints expressed with RQL expressions
        """
        with self.admin_access.repo_cnx() as cnx:
            aff1 = cnx.execute("INSERT Affaire X: X sujet 'cool'")[0][0]
            card1 = cnx.execute("INSERT Card X: X title 'cool'")[0][0]
            cnx.execute('SET X owned_by U WHERE X eid %(x)s, U login "iaminusersgrouponly"', {'x': card1})
            cnx.commit()
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            aff2 = cnx.execute("INSERT Affaire X: X sujet 'cool'")[0][0]
            soc1 = cnx.execute("INSERT Societe X: X nom 'chouette'")[0][0]
            cnx.execute("SET A concerne S WHERE A eid %(a)s, S eid %(s)s", {'a': aff2, 's': soc1})
            cnx.commit()
            result = self.gql_nok(cnx, "query getStuff($x: ID) { Affaire(eid: $x) {eid, sujet} }", x=aff1)
            self.assertIsNone(result.data["Affaire"])
            result = self.gql_ok(cnx, "query getStuff($x: ID) { Affaire(eid: $x) {eid, sujet} }", x=aff2)
            self.assertEquals(len(result.data["Affaire"]), 1)
            self.assertEquals(result.data["Affaire"][0]["eid"], str(aff2))
            result = self.gql_ok(cnx, "query getStuff($x: ID) { Card(eid: $x) {eid, title} }", x=card1)
            self.assertEquals(len(result.data["Card"]), 1)
            self.assertEquals(result.data["Card"][0]["eid"], str(card1))

    def test_insert_security(self):
        with self.new_access(u'anon').repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation m($nom: String) { createPersonne(nom: $nom) {  nom  } }", nom=u"bidule")
            self.assertRaises(Unauthorized, cnx.commit)
            self.assertEqual(len(self.gql_ok(cnx, "{ Personne { nom } }").data["Personne"]), 1)

    def test_insert_security_2(self):
        with self.new_access(u'anon').repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation m($nom: String) { createAffaire(sujet: $nom) {  sujet  } }", nom=u"bidule")
            self.assertRaises(Unauthorized, cnx.commit)
            # anon has no read permission on Affaire entities, so
            self.assertEqual(len(self.gql_ok(cnx, "{ Affaire { sujet } }").data["Affaire"]), 0)

    def test_insert_rql_permission(self):
        # test user can only add une affaire related to a societe he owns
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation m($nom: String) { createAffaire(sujet: $nom) {  sujet  } }", nom=u"bidule")
            self.assertRaises(Unauthorized, cnx.commit)
        # test nothing has actually been inserted
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(len(self.gql_ok(cnx, "{ Affaire { sujet } }").data["Affaire"]), 1)
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation m($nom: String) { createAffaire(sujet: $nom) {  sujet  } }", nom=u"cool")
            self.gql_ok(cnx, "mutation m($nom: String) { createSociete(nom: $nom) {  nom  } }", nom=u"chouette")
            self.gql_ok(cnx, "mutation m($affaire: String, $societe: String) { updateAffaire(old: {sujet: $affaire}, new: {concerne_as_Societe: {nom: $societe}}) { sujet } }", affaire=u"cool", societe=u"chouette")
            cnx.commit()

    def test_update_security_1(self):
        with self.new_access(u'anon').repo_cnx() as cnx:
            # local security check
            self.gql_ok(cnx, "mutation m($nom: String) { updatePersonne(old: {}, new: {nom: $nom}) { nom } }", nom=u"bidulechouette")
            self.assertRaises(Unauthorized, cnx.commit)
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(len(self.gql_ok(cnx, "query q($nom: String) { Personne(nom: $nom) { nom } }", nom=u"bidulechouette").data["Personne"]), 0)

    def test_update_security_2(self):
        with self.temporary_permissions(Personne={'read': ('users', 'managers'),
                                                  'add': ('guests', 'users', 'managers')}):
            with self.new_access(u'anon').repo_cnx() as cnx:
                self.gql_nok(cnx, "mutation m($nom: String) { updatePersonne(old: {}, new: {nom: $nom}) { nom } }", nom=u"bidulechouette")
        # test nothing has actually been inserted
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(len(self.gql_ok(cnx, "query q($nom: String) { Personne(nom: $nom) { nom } }", nom=u"bidulechouette").data["Personne"]), 0)

    def test_update_security_3(self):
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation m($nom: String) { createPersonne(nom: $nom) {  nom  } }", nom=u"biduuule")
            self.gql_ok(cnx, "mutation m($nom: String) { createSociete(nom: $nom) {  nom  } }", nom=u"looogilab")
            self.gql_ok(cnx, "mutation m($personne: String, $societe: String) { updatePersonne(old: {nom: $personne}, new: {travaille_as_Societe: {nom: $societe}}) { nom } }", personne=u"biduuule", societe=u"looogilab")

    def test_update_rql_permission(self):
        with self.admin_access.repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation { updateAffaire(old: {}, new: {concerne_as_Societe: {}}) {sujet} }")
            cnx.commit()
        # test user can only update une affaire related to a societe he owns
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation m($sujet:String) { updateAffaire(old: {}, new: {sujet: $sujet}) {sujet} }", sujet=u"pascool")
            # this won't actually do anything since the selection query won't return anything
            cnx.commit()
            # to actually get Unauthorized exception, try to update an entity we can read
            self.gql_ok(cnx, "mutation m($nom: String) { updateSociete(old: {}, new: {nom: $nom}) {nom} }", nom=u"toto")
            self.assertRaises(Unauthorized, cnx.commit)
            self.gql_ok(cnx, "mutation m($sujet: String) { createAffaire(sujet: $sujet) { sujet } }", sujet=u"pascool")
            self.gql_ok(cnx, "mutation m($nom: String) { createSociete(nom: $nom) { nom } }", nom=u"chouette")
            self.gql_ok(cnx, "mutation m($sujet:String, $nom:String) { updateAffaire(old: {sujet: $sujet}, new: {concerne_as_Societe: {nom: $nom}}) {sujet} }", sujet=u"pascool", nom=u"chouette")
            self.gql_ok(cnx, "mutation m($n1:String, $n2:String) { updateAffaire(old: {sujet: $n1}, new: {sujet: $n2}) {sujet} }", n1=u"pascool", n2=u"habahsicestcool")
            cnx.commit()

    def test_delete_security(self):
        # check local security
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            self.gql_nok(cnx, "mutation m($n:String) { deleteCWGroup(name: $n) }", n=u"staff")

    def test_delete_rql_permission(self):
        with self.admin_access.repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation { updateAffaire(old: {}, new: {concerne_as_Societe: {}}) {sujet} }")
            cnx.commit()
        # test user can only dele une affaire related to a societe he owns
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            # this won't actually do anything since the selection query won't return anything
            self.gql_ok(cnx, "mutation { deleteAffaire }")
            cnx.commit()
            # to actually get Unauthorized exception, try to delete an entity we can read
            self.gql_nok(cnx, "mutation { deleteSociete }")
            self.assertRaises(QueryError, cnx.commit)  # can't commit anymore
            cnx.rollback()
            self.gql_ok(cnx, "mutation m($sujet: String) { createAffaire(sujet: $sujet) { sujet } }", sujet=u"pascool")
            self.gql_ok(cnx, "mutation m($nom: String) { createSociete(nom: $nom) { nom } }", nom=u"chouette")
            self.gql_ok(cnx, "mutation m($sujet:String, $nom:String) { updateAffaire(old: {sujet: $sujet}, new: {concerne_as_Societe: {nom: $nom}}) {sujet} }", sujet=u"pascool", nom=u"chouette")
            cnx.commit()
            self.gql_ok(cnx, "mutation m($sujet: String) { deleteAffaire(sujet: $sujet) }", sujet=u"pascool")
            cnx.commit()

    def test_insert_relation_rql_permission(self):
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation { updateAffaire(old: {}, new: {concerne_as_Societe: {}}) {sujet} }")
            # should raise Unauthorized since user don't own S though this won't
            # actually do anything since the selection query won't return
            # anything
            cnx.commit()
            # to actually get Unauthorized exception, try to insert a relation
            # were we can read both entities
            rset = cnx.execute('Personne P')
            self.assertEqual(len(rset), 1)
            ent = rset.get_entity(0, 0)
            self.assertRaises(Unauthorized, ent.cw_check_perm, 'update')

            result = self.gql_ok(cnx, "{ Personne(travaille_as_Societe: {}) { eid } }")
            self.assertEquals(len(result.data["Personne"]), 0)
            self.gql_nok(cnx, "mutation { updatePersonne(old: {}, new: {travaille_as_Societe: {}}) { eid } }")
            self.assertRaises(QueryError, cnx.commit)  # can't commit anymore
            cnx.rollback()
            # test nothing has actually been inserted:
            result = self.gql_ok(cnx, "{ Personne(travaille_as_Societe: {}) { eid } }")
            self.assertEquals(len(result.data["Personne"]), 0)
            self.gql_ok(cnx, "mutation m($nom: String) { createSociete(nom: $nom) {nom} }", nom=u"chouette")
            self.gql_ok(cnx, "mutation m($nom: String) { updateAffaire(old: {}, new: {concerne_as_Societe: {nom: $nom}}) {sujet} }", nom=u"chouette")
            cnx.commit()

    def test_delete_relation_rql_permission(self):
        with self.admin_access.repo_cnx() as cnx:
            self.gql_ok(cnx, "mutation { updateAffaire(old: {}, new: {concerne_as_Societe: {}}) {sujet} }")
            cnx.commit()
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            # this won't actually do anything since the selection query won't return anything
            self.gql_ok(cnx, "mutation { deleteAffaire(concerne_as_Societe: {}) }")
            cnx.commit()
        with self.admin_access.repo_cnx() as cnx:
            # to actually get Unauthorized exception, try to delete a relation we can read
            result = self.gql_ok(cnx, "mutation m($sujet: String) { createAffaire(sujet: $sujet) { eid, sujet } }", sujet=u"pascool")
            eid = result.data["createAffaire"]["eid"]
            self.gql_ok(cnx, "mutation m($eid: ID, $login:String) { updateAffaire(old: {eid: $eid}, new: {owned_by: {login: $login}}) {sujet} }", eid=eid, login=u"iaminusersgrouponly")
            self.gql_ok(cnx, "mutation m($sujet: String) { updateAffaire(old: {sujet: $sujet}, new: {concerne_as_Societe: {}}) {sujet} }", sujet=u"pascool")
            cnx.commit()
        with self.new_access(u'iaminusersgrouponly').repo_cnx() as cnx:
            self.gql_nok(cnx, "mutation { deleteFromAffaire(from: {}, concerne_as_Societe: {}) }")
            self.assertRaises(QueryError, cnx.commit)  # can't commit anymore
            cnx.rollback()
            self.gql_ok(cnx, "mutation m($nom: String) { createSociete(nom: $nom) { nom } }", nom=u"chouette")
            self.gql_ok(cnx, "mutation m($nom: String) { updateAffaire(old: {}, new: {concerne_as_Societe: {nom: $nom}}) {sujet} }", nom=u"chouette")
            cnx.commit()
            self.gql_ok(cnx, "mutation m($nom: String) { deleteFromAffaire(from: {}, concerne_as_Societe: {nom: $nom}) }", nom=u"chouette")
            cnx.commit()


class GraphQLFeatureTC(GraphQLBaseTC):
    """
    Suite of feature tests for GraphQL
    """

    def test_simple_query_no_arg(self):
        """
        Test simple querying without arguments
        """
        query = "{ Affaire { sujet } }"
        with self.admin_access.repo_cnx() as cnx:
            # Reading is OK for the manager
            result = GraphQLQuerier.execute(cnx, query)
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["Affaire"]), 2)

    def test_simple_query_with_eid_arg(self):
        """
        Test simple querying with argument
        """
        query = "query getAffaire($affaire_eid: ID) { Affaire(eid: $affaire_eid) { sujet } }"
        with self.admin_access.repo_cnx() as cnx:
            # Reading is OK for the manager
            result = GraphQLQuerier.execute(cnx, query, affaire_eid=self.affaire1)
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["Affaire"]), 1)
            self.assertEquals(result.data["Affaire"][0]["sujet"], "affaire1")
            result = GraphQLQuerier.execute(cnx, query, affaire_eid=self.affaire2)
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["Affaire"]), 1)
            self.assertEquals(result.data["Affaire"][0]["sujet"], "affaire2")

    def test_simple_query_with_eid_arg_double(self):
        """
        Test querying several times the same entities with different arguments
        """
        query = "query getAffaire($eid1: ID, $eid2: ID) { affaire1: Affaire(eid: $eid1) { sujet }, affaire2: Affaire(eid: $eid2) { sujet } }"
        with self.admin_access.repo_cnx() as cnx:
            # Reading is OK for the manager
            result = GraphQLQuerier.execute(cnx, query, eid1=self.affaire1, eid2=self.affaire2)
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(result.data["affaire1"][0]["sujet"], "affaire1")
            self.assertEquals(result.data["affaire2"][0]["sujet"], "affaire2")

    def test_nested_query_arguments(self):
        """
        Test querying with arguments on fields on more than one nesting levels
        """
        query = "query getPersonne($pn: String, $sn: String) { Personne(nom: $pn) { nom, travaille(nom: $sn) { ... on Societe { nom } } } }"
        with self.admin_access.repo_cnx() as cnx:
            cnx.execute("INSERT Personne X: X nom 'personne1'")
            cnx.execute("INSERT Personne X: X nom 'personne2'")
            cnx.execute("INSERT Societe X: X nom 'societe1'")
            cnx.execute("INSERT Societe X: X nom 'societe2'")
            cnx.execute("SET P travaille S WHERE P nom 'personne1', S nom 'societe1'")
            cnx.execute("SET P travaille S WHERE P nom 'personne1', S nom 'societe2'")
            result = GraphQLQuerier.execute(cnx, query, pn="personne1", sn="societe1")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["Personne"]), 1)
            self.assertEquals(result.data["Personne"][0]["nom"], "personne1")
            self.assertEquals(len(result.data["Personne"][0]["travaille"]), 1)
            self.assertEquals(result.data["Personne"][0]["travaille"][0]["nom"], "societe1")

    def test_complex_query_arguments(self):
        """
        Test querying with an object argument
        """
        query = "query getPersonne($nom: String) { Personne(travaille_as_Societe: {nom: $nom}) { nom, travaille { ... on Societe { nom } } } }"
        with self.admin_access.repo_cnx() as cnx:
            cnx.execute("INSERT Personne X: X nom 'personne1'")
            cnx.execute("INSERT Personne X: X nom 'personne2'")
            cnx.execute("INSERT Societe X: X nom 'societe1'")
            cnx.execute("INSERT Societe X: X nom 'societe2'")
            cnx.execute("SET P travaille S WHERE P nom 'personne1', S nom 'societe1'")
            cnx.execute("SET P travaille S WHERE P nom 'personne2', S nom 'societe2'")
            result = GraphQLQuerier.execute(cnx, query, nom="societe1")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["Personne"]), 1)
            self.assertEquals(result.data["Personne"][0]["nom"], "personne1")
            self.assertEquals(len(result.data["Personne"][0]["travaille"]), 1)
            self.assertEquals(result.data["Personne"][0]["travaille"][0]["nom"], "societe1")

    def test_argument_on_scalar_field(self):
        """
        Test querying with an argument in a scalar primitive field
        """
        query = "query getPersonne($title: String) { Personne { nom, fiche(title: $title) { title, content } } }"
        with self.admin_access.repo_cnx() as cnx:
            cnx.execute("INSERT Personne X: X nom 'personne1'")
            cnx.execute("INSERT Personne X: X nom 'personne2'")
            cnx.execute("INSERT Card X: X title 'fiche1', X content 'fiche1'")
            cnx.execute("INSERT Card X: X title 'fiche2', X content 'fiche2'")
            cnx.execute("SET P fiche C WHERE P nom 'personne1' AND C title 'fiche1'")
            cnx.execute("SET P fiche C WHERE P nom 'personne2' AND C title 'fiche2'")
            result = GraphQLQuerier.execute(cnx, query, title="fiche1")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["Personne"]), 2)
            self.assertEquals(result.data["Personne"][0]["nom"], "personne1")
            self.assertEquals(result.data["Personne"][0]["fiche"]["title"], "fiche1")
            self.assertEquals(result.data["Personne"][1]["nom"], "personne2")
            self.assertEquals(result.data["Personne"][1]["fiche"], None)

    def test_mutation_insert_simple(self):
        """
        Test simple insertion of a new entity with primitive fields
        """
        query = "mutation myMutation($sujet: String) { createAffaire(sujet: $sujet) {  eid, sujet  } }"
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, query, sujet=u"cool")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["createAffaire"]), 2)
            self.assertIsNotNone(result.data["createAffaire"]["eid"])
            self.assertEquals(result.data["createAffaire"]["sujet"], u"cool")

    def test_mutation_insert_with_where(self):
        """
        Test insertion of a new entity with a reference to a existing one looked-up based on its attributes
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) { eid } }", nom=u"societe1")
            societe1 = result.data["createSociete"]["eid"]
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($sujet: String, $societe: String) { "
                                                 "createAffaire(sujet: $sujet, concerne_as_Societe: {nom: $societe}) { "
                                                 "eid, sujet, concerne { ... on Societe { eid, nom } } } }",
                                            sujet=u"affaire1", societe=u"societe1")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["createAffaire"]), 3)
            self.assertEquals(result.data["createAffaire"]["sujet"], u"affaire1")
            self.assertEquals(len(result.data["createAffaire"]["concerne"]), 1)
            self.assertEquals(result.data["createAffaire"]["concerne"][0]["nom"], u"societe1")
            self.assertEquals(result.data["createAffaire"]["concerne"][0]["eid"], societe1)

    def test_mutation_update_simple(self):
        """
        Test simple update of an entity with primitive fields
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) {  eid  } }",
                                            nom=u"societe1")
            societe1 = result.data["createSociete"]["eid"]
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom_old: String, $nom_new: String) { updateSociete(old: {nom: $nom_old}, new: {nom: $nom_new}) { eid, nom } }",
                                            nom_old=u"societe1",
                                            nom_new=u"societe2")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["updateSociete"]), 1)
            self.assertEquals(len(result.data["updateSociete"][0]), 2)
            self.assertEquals(result.data["updateSociete"][0]["eid"], societe1)
            self.assertEquals(result.data["updateSociete"][0]["nom"], u"societe2")

    def test_mutation_update_object_field(self):
        """
        Test update of an entity with a new value for an object field
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) {  eid  } }",
                                            nom=u"societe1")
            societe1 = result.data["createSociete"]["eid"]
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) {  eid  } }",
                                            nom=u"societe2")
            societe2 = result.data["createSociete"]["eid"]

            result = GraphQLQuerier.execute(cnx, "mutation myMutation($sujet: String, $societe: String) { updateAffaire("
                                                 "old: {sujet: $sujet}"
                                                 ", new: {concerne_as_Societe: {nom: $societe}}) {"
                                                 "eid, sujet, concerne { ... on Societe {eid, nom} } } }",
                                            sujet=u"affaire1",
                                            societe=u"societe1")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["updateAffaire"]), 1)
            self.assertEquals(len(result.data["updateAffaire"][0]), 3)
            self.assertEquals(result.data["updateAffaire"][0]["eid"], str(self.affaire1))
            self.assertEquals(result.data["updateAffaire"][0]["sujet"], u"affaire1")
            self.assertEquals(len(result.data["updateAffaire"][0]["concerne"]), 1)
            self.assertEquals(result.data["updateAffaire"][0]["concerne"][0]["eid"], societe1)
            self.assertEquals(result.data["updateAffaire"][0]["concerne"][0]["nom"], u"societe1")

            result = GraphQLQuerier.execute(cnx, "mutation myMutation($sujet: String, $societe: String) { updateAffaire("
                                                 "old: {sujet: $sujet}"
                                                 ", new: {concerne_as_Societe: {nom: $societe}}) {"
                                                 "eid, sujet, concerne { ... on Societe {eid, nom} } } }",
                                            sujet=u"affaire2",
                                            societe=u"societe2")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["updateAffaire"]), 1)
            self.assertEquals(len(result.data["updateAffaire"][0]), 3)
            self.assertEquals(result.data["updateAffaire"][0]["eid"], str(self.affaire2))
            self.assertEquals(result.data["updateAffaire"][0]["sujet"], u"affaire2")
            self.assertEquals(len(result.data["updateAffaire"][0]["concerne"]), 1)
            self.assertEquals(result.data["updateAffaire"][0]["concerne"][0]["eid"], societe2)
            self.assertEquals(result.data["updateAffaire"][0]["concerne"][0]["nom"], u"societe2")

    def test_mutation_delete_simple_single(self):
        """
        Test delete a single entity on a simple query
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) {  eid  } }",
                                            nom=u"societe1")
            societe1 = result.data["createSociete"]["eid"]
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) {  eid  } }",
                                            nom=u"societe2")
            societe2 = result.data["createSociete"]["eid"]

            result = GraphQLQuerier.execute(cnx, "mutation myMutation($societe: String) { deleteSociete(nom: $societe) }",
                                            societe=u"societe1")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["deleteSociete"]), 1)
            self.assertEquals(result.data["deleteSociete"][0], societe1)

    def test_mutation_delete_simple_multiple(self):
        """
        Test delete a multiple entities on a simple query
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) {  eid  } }",
                                            nom=u"societe1")
            societe1 = result.data["createSociete"]["eid"]
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) {  eid  } }",
                                            nom=u"societe2")
            societe2 = result.data["createSociete"]["eid"]

            result = GraphQLQuerier.execute(cnx, "mutation myMutation { deleteSociete }")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["deleteSociete"]), 2)
            self.assertEquals(result.data["deleteSociete"][0], societe1)
            self.assertEquals(result.data["deleteSociete"][1], societe2)

    def test_mutation_delete_relation(self):
        """
        Test delete relations
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "mutation myMutation($nom: String) { createSociete(nom: $nom) {  eid  } }",
                                            nom=u"societe1")
            societe1 = result.data["createSociete"]["eid"]
            result = GraphQLQuerier.execute(cnx, "mutation m($s: ID, $a: ID) { updateAffaire(old: {eid: $a}, new: {concerne_as_Societe: {eid: $s}}) {eid, concerne {... on Societe {eid}}} }", s=societe1, a=self.affaire1)
            self.assertEquals(result.data["updateAffaire"][0]["eid"], str(self.affaire1))
            self.assertEquals(result.data["updateAffaire"][0]["concerne"][0]["eid"], str(societe1))
            result = GraphQLQuerier.execute(cnx, "{ Affaire { eid, concerne { ... on Societe { eid } } } }")
            self.assertEquals(result.data["Affaire"][0]["eid"], str(self.affaire1))
            self.assertEquals(result.data["Affaire"][0]["concerne"][0]["eid"], str(societe1))
            result = GraphQLQuerier.execute(cnx, "mutation m($s: ID, $a: ID) { deleteFromAffaire(from: {eid: $a}, concerne_as_Societe: {eid: $s}) }", s=societe1, a=self.affaire1)
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            result = GraphQLQuerier.execute(cnx, "{ Affaire { eid, concerne { ... on Societe { eid } } } }")
            self.assertEquals(result.data["Affaire"][0]["eid"], str(self.affaire1))
            self.assertEquals(len(result.data["Affaire"][0]["concerne"]), 0)
            pass


class GraphQLReflectionTC(GraphQLBaseTC):
    """
    Test suite for GraphQL reflection features
    """

    def test_graphql_based_reflection_list_entities(self):
        """
        Test listing entity types using GraphQL-based reflection
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "{ __schema { queryType { fields { name } } } }")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["__schema"]["queryType"]["fields"]), 45)
            found_affaire = False
            for t in result.data["__schema"]["queryType"]["fields"]:
                if t["name"] == "Affaire":
                    found_affaire = True
            self.assertTrue(found_affaire)

    def test_cw_based_reflection_list_entities(self):
        """
        Test listing entity types using CubicWeb-based reflection
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "{ CWEType(final: false) { name } }")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["CWEType"]), 45)
            found_affaire = False
            for t in result.data["CWEType"]:
                if t["name"] == "Affaire":
                    found_affaire = True
            self.assertTrue(found_affaire)

    def test_graphql_based_reflection_list_fields_of_entity(self):
        """
        Test listing the fields of an entity using GraphQL-based reflection
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "query q($name: String!) { __type(name: $name) { name, fields { name, type { name, kind } } } }", name="Affaire")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["__type"]["fields"]), 28)
            found = False
            for f in result.data["__type"]["fields"]:
                if f["name"] == "todo_by":
                    found = True
            self.assertTrue(found)

    def test_cw_based_reflection_list_fields_of_entity(self):
        """
        Test listing the fields of an entity using CubicWeb-based reflection
        """
        with self.admin_access.repo_cnx() as cnx:
            result = GraphQLQuerier.execute(cnx, "query q($name: String!) { CWRelation(from_entity: {name: $name}) { relation_type { name }, to_entity { name } } }", name="Affaire")
            self.assertIsNone(result.errors)
            self.assertIsNotNone(result.data)
            self.assertEquals(len(result.data["CWRelation"]), 16)
            found = False
            for f in result.data["CWRelation"]:
                if f["relation_type"][0]["name"] == "todo_by":
                    found = True
            self.assertTrue(found)


if __name__ == '__main__':
    from unittest import main

    main()
