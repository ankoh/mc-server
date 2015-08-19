__author__ = 'kohn'

import unittest
from mendeleycache.crawler.file_crawler import FileCrawler


class TestFileCrawler(unittest.TestCase):

    def test_get_group_members(self):
        crwler = FileCrawler()

        # invalid id
        members = crwler.get_group_members('d0b7f41f)-ad37-3b47-ab70-9feac35557cc')
        self.assertIsNotNone(members)
        self.assertEqual(0, len(members))

        # valid id
        members = crwler.get_group_members('d0b7f41f-ad37-3b47-ab70-9feac35557cc')
        self.assertIsNotNone(members)
        self.assertNotEqual(0, len(members))