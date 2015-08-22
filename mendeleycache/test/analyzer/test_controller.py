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

    def test_analyze_field_tag(self):
        ctrl = AnalysisController([], {}, [])
        ctrl.analyze_field_tag("docid1", "t ag-1")

        # Check if CacheField for tag1 was created
        self.assertTrue(len(ctrl.unified_field_title_to_field), 1)
        self.assertEqual("Tag 1", ctrl.unified_field_title_to_field["tag1"].title)
        self.assertEqual("tag1", ctrl.unified_field_title_to_field["tag1"].unified_title)
        # Check if document docid1 has been added to tag1
        self.assertTrue(len(ctrl.unified_field_title_to_documents), 1)
        self.assertTrue(len(ctrl.unified_field_title_to_documents["tag1"]), 1)
        self.assertIn("docid1", ctrl.unified_field_title_to_documents["tag1"])

        # Now add the same tag for the same document (written slightly different)
        ctrl.analyze_field_tag("docid1", "t ag - 1")
        self.assertTrue(len(ctrl.unified_field_title_to_field), 1)
        self.assertEqual("Tag 1", ctrl.unified_field_title_to_field["tag1"].title)
        self.assertEqual("tag1", ctrl.unified_field_title_to_field["tag1"].unified_title)
        # Check if document docid1 is still the only doc
        self.assertTrue(len(ctrl.unified_field_title_to_documents), 1)
        self.assertTrue(len(ctrl.unified_field_title_to_documents["tag1"]), 1)
        self.assertIn("docid1", ctrl.unified_field_title_to_documents["tag1"])

        # Now add a new document for the same tag
        ctrl.analyze_field_tag("docid2", "t ag - 1")
        self.assertTrue(len(ctrl.unified_field_title_to_field), 1)
        self.assertEqual("Tag 1", ctrl.unified_field_title_to_field["tag1"].title)
        self.assertEqual("tag1", ctrl.unified_field_title_to_field["tag1"].unified_title)
        # Check if document docid2 is now linked with tag 1
        self.assertTrue(len(ctrl.unified_field_title_to_documents), 1)
        self.assertTrue(len(ctrl.unified_field_title_to_documents["tag1"]), 2)
        self.assertIn("docid1", ctrl.unified_field_title_to_documents["tag1"])
        self.assertIn("docid2", ctrl.unified_field_title_to_documents["tag1"])

        # Now add an old document with a new tag
        ctrl.analyze_field_tag("docid2", "t ag - 2")
        self.assertTrue(len(ctrl.unified_field_title_to_field), 2)
        self.assertEqual("Tag 2", ctrl.unified_field_title_to_field["tag2"].title)
        self.assertEqual("tag2", ctrl.unified_field_title_to_field["tag2"].unified_title)
        # Check if document docid2 is now linked with tag 2
        self.assertTrue(len(ctrl.unified_field_title_to_documents), 2)
        self.assertTrue(len(ctrl.unified_field_title_to_documents["tag2"]), 1)
        self.assertIn("docid2", ctrl.unified_field_title_to_documents["tag2"])

        # Now add a new document with a new tag
        ctrl.analyze_field_tag("docid3", "t ag - 3")
        self.assertTrue(len(ctrl.unified_field_title_to_field), 3)
        self.assertEqual("Tag 3", ctrl.unified_field_title_to_field["tag3"].title)
        self.assertEqual("tag3", ctrl.unified_field_title_to_field["tag3"].unified_title)
        # Check if document docid3 is now linked with tag 3
        self.assertTrue(len(ctrl.unified_field_title_to_documents), 3)
        self.assertTrue(len(ctrl.unified_field_title_to_documents["tag3"]), 1)
        self.assertIn("docid3", ctrl.unified_field_title_to_documents["tag3"])

    def test_analyze_author(self):
        ctrl = AnalysisController(self.profiles, {}, [])
        ctrl.process_profiles()

        # Find an existing profile as author of a doc
        self.assertEqual(len(ctrl.unified_name_to_participated_documents["hansmustermann"]), 0)
        ctrl.analyze_author("doc1", ("Hans", "Mustermann"))
        self.assertEqual(len(ctrl.unified_name_to_participated_documents["hansmustermann"]), 1)
        self.assertIn("doc1", ctrl.unified_name_to_participated_documents["hansmustermann"])

        # Find the same profile in another doc
        ctrl.analyze_author("doc2", ("Hans", "Mustermann"))
        self.assertEqual(len(ctrl.unified_name_to_participated_documents["hansmustermann"]), 2)
        self.assertIn("doc2", ctrl.unified_name_to_participated_documents["hansmustermann"])

        # Authored docs are still 0
        self.assertEqual(len(ctrl.unified_name_to_authored_documents["hansmustermann"]), 0)

        # Find an unknown profile as author of a doc
        self.assertNotIn("nichtexistent", ctrl.unified_name_to_participated_documents)
        ctrl.analyze_author("doc1", ("Nicht", "Existent"))
        self.assertEqual(len(ctrl.unified_name_to_participated_documents["nichtexistent"]), 1)
        self.assertIn("nichtexistent", ctrl.unified_name_to_unknown_profile)
        self.assertEqual(ctrl.unified_name_to_unknown_profile["nichtexistent"].name, "Nicht Existent")
        self.assertEqual(ctrl.unified_name_to_unknown_profile["nichtexistent"].unified_name, "nichtexistent")


    def test_process_profile_documents(self):
        pass

    def test_process_group_documents(self):
        pass

    def test_process_all(self):
        pass

    def test_integrate_process_profile_documents(self):
        pass
