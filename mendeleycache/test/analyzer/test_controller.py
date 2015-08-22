__author__ = 'kohn'

import unittest
from mendeleycache.analyzer.controller import AnalysisController
from mendeleycache.models import Profile, Document


class TestAnalysisController(unittest.TestCase):
    profile1 = Profile("id1", "Hans", "Mustermann", "Neuer besserer Hans Mustermann", "")
    profile4 = Profile("id4", "Hans", "Mustermann", "Alter Hans Mustermann", "")
    profile2 = Profile("id2", "Max", "Mustermann", "Max Mustermann", "")
    profile3 = Profile("id3", "Heinrich", "Mustermann", "Prof. Dr. Dr. Heinrich Mustermann", "")

    profiles = [profile1, profile2, profile3, profile4]

    def test_process_profiles(self):
        ctrl = AnalysisController(self.profiles, {}, [])
        ctrl.process_profiles()

        self.assertEqual(len(ctrl.unified_name_to_profiles), 3)

        # check that all unified names are stored as keys
        self.assertIn("hansmustermann", ctrl.unified_name_to_profiles)
        self.assertIn("maxmustermann", ctrl.unified_name_to_profiles)
        self.assertIn("heinrichmustermann", ctrl.unified_name_to_profiles)

        # check that the profiles are stored correctly
        self.assertEqual(ctrl.unified_name_to_profiles["hansmustermann"][0], self.profile1)
        self.assertEqual(ctrl.unified_name_to_profiles["hansmustermann"][1], self.profile4)
        self.assertEqual(ctrl.unified_name_to_profiles["maxmustermann"][0], self.profile2)
        self.assertEqual(ctrl.unified_name_to_profiles["heinrichmustermann"][0], self.profile3)

        # check that the real names are set && updated correctly
        self.assertEqual(ctrl.unified_name_to_real_name["hansmustermann"], "Hans Mustermann")
        self.assertEqual(ctrl.unified_name_to_real_name["maxmustermann"], "Max Mustermann")
        self.assertEqual(ctrl.unified_name_to_real_name["heinrichmustermann"], "Heinrich Mustermann")

        # check that the document sets are created
        self.assertIn("hansmustermann", ctrl.unified_name_to_authored_documents)
        self.assertIn("hansmustermann", ctrl.unified_name_to_participated_documents)
        self.assertIn("maxmustermann", ctrl.unified_name_to_authored_documents)
        self.assertIn("maxmustermann", ctrl.unified_name_to_participated_documents)
        self.assertIn("heinrichmustermann", ctrl.unified_name_to_authored_documents)
        self.assertIn("heinrichmustermann", ctrl.unified_name_to_participated_documents)

    def test_analyze_author(self):
        pass

    def test_analyze_field_tag(self):
        pass

    def test_process_profile_documents(self):
        pass

    def test_process_group_documents(self):
        pass

    def test_process_all(self):
        pass

    def test_integrate_process_profile_documents(self):
        pass
