__author__ = 'kohn'

import unittest
from mendeleycache.analyzer.unification import unify_document_title, unify_field_title, unify_profile_name


class TestUnification(unittest.TestCase):
    def test_unify_document_title(self):
        title = "Requirements Engineering for Scientific Computing: A Model-Based Approach"
        unified, real = unify_document_title(title)
        self.assertEqual(real, title)
        self.assertEqual(unified, "requirementsengineeringforscientificcomputingamodelbasedapproach")

        title = "Comparing state- and operation-based change tracking on models"
        unified, real = unify_document_title(title)
        self.assertEqual(real, title)
        self.assertEqual(unified, "comparingstateandoperationbasedchangetrackingonmodels")

        title = "Agile Factory - An Example of an Industry 4.0 Manufacturing Process"
        unified, real = unify_document_title(title)
        self.assertEqual(real, title)
        self.assertEqual(unified, "agilefactoryanexampleofanindustry40manufacturingprocess")

        title = "A Domain Specific Requirements Model for Scientific Computing (NIER Track)"
        unified, real = unify_document_title(title)
        self.assertEqual(real, title)
        self.assertEqual(unified, "adomainspecificrequirementsmodelforscientificcomputingniertrack")

        title = "SLPC++: Teaching software engineering project courses in industrial application landscapes - A tutorial"
        unified, real = unify_document_title(title)
        self.assertEqual(real, title)
        self.assertEqual(unified, "slpcteachingsoftwareengineeringprojectcoursesinindustrialapplicationlandscapesatutorial")

    def test_unify_field_title(self):
        title = "cyber-physical systems"
        unified, real = unify_field_title(title)
        self.assertEqual(unified, "cyberphysicalsystems")
        self.assertEqual(real, "Cyber-Physical Systems")

    def test_unify_profile_name(self):
        first_name = "Claudia"
        last_name = "Linnhoff-Popien"
        unified, real = unify_profile_name(first_name, last_name)
        self.assertEqual(unified, "claudialinnhoffpopien")
        self.assertEqual(real, "Claudia Linnhoff-Popien")

        first_name = ""
        last_name = "Juan Haladjian"
        unified, real = unify_profile_name(first_name, last_name)
        unified, real = unify_profile_name(first_name, last_name)
        self.assertEqual(unified, "juanhaladjian")
        self.assertEqual(real, "Juan Haladjian")

        first_name = "Juan"
        last_name = "Haladjian"
        unified, real = unify_profile_name(first_name, last_name)
        self.assertEqual(unified, "juanhaladjian")
        self.assertEqual(real, "Juan Haladjian")
