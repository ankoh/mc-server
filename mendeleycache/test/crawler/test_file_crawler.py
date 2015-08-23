# -*- coding: utf-8 -*-

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
        self.assertEqual(19, len(members))

        # valid but not existing id
        members = crwler.get_group_members('notexisting-ad37-3b47-ab70-9feac35557cc')
        self.assertIsNotNone(members)
        self.assertEqual(0, len(members))

    def test_get_profile_by_id(self):
        crwler = FileCrawler()

        # invalid id
        profile = crwler.get_profile_by_id('1bb8291f)-f619-35cf-9d43-b26e44fba327')
        self.assertIsNone(profile)

        # valid but not existing id
        profile = crwler.get_profile_by_id('notexisting-f619-35cf-9d43-b26e44fba327')
        self.assertIsNone(profile)

        tuples = [
            ('1bb8291f-f619-35cf-9d43-b26e44fba327', 'Helmut', 'Naughton',
             'Dipl. Math. (Univ.), M. Appl. Inf. Helmut Naughton', 'https://www.mendeley.com/profiles/helmut-naughton/'),
            ('10a89b23-6366-32a0-a224-64ad4d5c859a', 'Hoda', 'Naguib',
             'Hoda Naguib, M.Sc in Information Systems', 'https://www.mendeley.com/profiles/hoda-naguib/'),
            ('253c5e1d-6d25-35f4-a586-adde07dfcd82', 'Emitzá', 'Guzmán',
             'Emitzá Guzmán', 'https://www.mendeley.com/profiles/emitza-guzman/'),
            ('26f3b2ae-61d5-3f70-a5d1-4dd75cc56e2b', 'Tobias', 'Roehm',
             'Tobias Roehm', 'https://www.mendeley.com/profiles/tobias-roehm/'),
            ('2f513deb-7b71-3428-9782-9b10f3c6cc9b', 'Yang', 'Li',
             'Yang Li', 'https://www.mendeley.com/profiles/yang-li11/'),
            ('3662b634-8adb-3bc9-ac56-0d85c76e872c', 'Oliver', 'Creighton',
             'Oliver Creighton', 'https://www.mendeley.com/profiles/oliver-creighton/'),
            ('3d32488b-2c4b-3fc6-843b-397139d0b42a', 'Han', 'Xu',
             'Han Xu', 'https://www.mendeley.com/profiles/han-xu3/'),
            ('49732bcf-b75a-386e-83b6-6a720bb0e882', 'Miriam', 'Schmidberger',
             'Miriam Schmidberger', 'https://www.mendeley.com/profiles/miriam-schmidberger/'),
            ('6820e59e-1c4c-3ca3-a497-e8ee45f2a489', 'Constantin', 'Scheuermann',
             'Constantin Scheuermann', 'https://www.mendeley.com/profiles/constantin-scheuermann/'),
            ('6fe24a7a-8eb8-3005-8d6a-71cdf48ce92d', 'Juan', 'Haladjian',
             'Juan Haladjian, M.Sc', 'https://www.mendeley.com/profiles/juan-haladjian/'),
            ('8d63c54a-df02-3760-bd39-1e13e71999ef', 'Stefan', 'Nosovic',
             'Stefan Nosovic', 'https://www.mendeley.com/profiles/stefan-nosovic/'),
            ('a43c2a50-e164-3114-adb1-34d792c09268', 'Zardosht', 'Hodaie',
             'Zardosht Hodaie', 'https://www.mendeley.com/profiles/zardosht-hodaie/'),
            ('a9ae8d2b-8af6-3e58-82bc-c39148b042ce', 'Stephan', 'Krusche',
             'Stephan Krusche', 'https://www.mendeley.com/profiles/stephan-krusche/'),
            ('b16de8ea-39a8-385f-8a2a-049b14f50ee1', 'Sebastian', 'Peters',
             'Sebastian Peters', 'https://www.mendeley.com/profiles/sebastian-peters1/'),
            ('d9a796cc-5142-3cd9-b1f6-21cc3c394f5a', 'Nitesh', 'Narayan',
             'Nitesh Narayan', 'https://www.mendeley.com/profiles/nitesh-narayan/'),
            ('e9f58b91-98db-3e14-9fb7-61ee0e9878e4', 'Damir', 'Ismailović',
             'Dr. Damir Ismailović', 'https://www.mendeley.com/profiles/damir-ismailovic/'),
            ('f27c682d-30e4-3f9a-a280-010f74808936', 'Barbara', 'Reichart',
             'Barbara Reichart', 'https://www.mendeley.com/profiles/barbara-reichart/'),
            ('f78cf5fc-db4c-3755-ae40-c022266496b6', 'Bernd', 'Bruegge',
             'Bernd Bruegge', 'https://www.mendeley.com/profiles/bernd-bruegge1/')
        ]

        for t in tuples:
            profile = crwler.get_profile_by_id(t[0])
            self.assertEqual(t[0], profile.identifier)
            self.assertEqual(t[1], profile.first_name)
            self.assertEqual(t[2], profile.last_name)
            self.assertEqual(t[3], profile.display_name)
            self.assertEqual(t[4], profile.link)

    def test_get_documents_by_profile_id(self):
        crwler = FileCrawler()

        # invalid id
        documents = crwler.get_documents_by_profile_id('1bb8291f)-f619-35cf-9d43-b26e44fba327')
        self.assertIsNone(documents)

        # valid but not existing id
        documents = crwler.get_documents_by_profile_id('notexisting-f619-35cf-9d43-b26e44fba327')
        self.assertIsNotNone(documents)
        self.assertEqual(0, len(documents))

        documents = crwler.get_documents_by_profile_id('6fe24a7a-8eb8-3005-8d6a-71cdf48ce92d')
        self.assertIsNotNone(documents)
        self.assertEqual(4, len(documents))

        # check first document (eb4a3fe7-f756-3112-8a12-6cdf0d16a9ad)
        document = documents[0]
        self.assertEqual(document.core_title, "A quick prototyping tool for serious games with real time physics")
        self.assertEqual(document.core_profile_id, "6fe24a7a-8eb8-3005-8d6a-71cdf48ce92d")
        self.assertEqual(document.core_id, "eb4a3fe7-f756-3112-8a12-6cdf0d16a9ad")
        self.assertEqual(document.core_type, "thesis")
        self.assertEqual(document.core_abstract, "")
        self.assertEqual(document.core_source, "")
        self.assertEqual(document.core_year, 2011)
        self.assertIsNotNone(document.core_authors)
        self.assertEqual(len(document.core_authors), 1)
        self.assertIsNotNone(document.core_keywords)
        self.assertEqual(len(document.core_keywords), 0)
        self.assertIsNotNone(document.tags)
        self.assertEqual(len(document.tags), 3)

        # check second document (d782c4cd-ed24-3b2d-9816-8ba0580ea704)
        document = documents[1]
        self.assertEqual(document.core_title, "A quick prototyping framework for adaptive serious games with 2D physics on mobile touch devices")
        self.assertEqual(document.core_profile_id, "6fe24a7a-8eb8-3005-8d6a-71cdf48ce92d")
        self.assertEqual(document.core_id, "d782c4cd-ed24-3b2d-9816-8ba0580ea704")
        self.assertEqual(document.core_type, "conference_proceedings")
        self.assertEqual(document.core_abstract, "In recent years mobile devices like the iPhone (and Android devices) became even more powerful than netbooks. This computational power can be used for complex simulations and games that were until now just possible on desktop computers. We propose adaptive games with 2D physics on mobile devices that can be used for learning purposes. We argue that even young children can understand and apply physical laws in such games. Because of the touch displays, abstract physical concepts can be made more tangible as one can directly touch the objects on the screen. Furthermore, digital games can provide an individualized learning and playing experience for each child with the integrated Adaptivity. In this work we show the problems that arise when developing serious games featuring adaptivity and physics and we propose a solution to them: a quick prototyping framework called TangoPhysics. TangoPhysics suggests a new way of prototyping mobile games: The prototypes are constructed directly on the mobile device, and can be tested at any moment. We show that the development time of a serious game can be dramatically reduced with our framework. At the same time the development is simplified dramatically allowing not only programmers, but also teachers and in the long run maybe even students to develop their own serious games,")
        self.assertEqual(document.core_source, "IADIS Mobile Learning 2012 ML 2012")
        self.assertEqual(document.core_year, 2012)
        self.assertIsNotNone(document.core_authors)
        self.assertEqual(len(document.core_authors), 4)
        self.assertIsNotNone(document.core_keywords)
        self.assertEqual(len(document.core_keywords), 4)
        self.assertIsNotNone(document.tags)
        self.assertEqual(len(document.tags), 0)

        # check third document (b8912127-4443-304f-8599-779ec5c515a9)
        document = documents[2]
        self.assertEqual(document.core_title, "A framework for game tuning")
        self.assertEqual(document.core_profile_id, "6fe24a7a-8eb8-3005-8d6a-71cdf48ce92d")
        self.assertEqual(document.core_id, "b8912127-4443-304f-8599-779ec5c515a9")
        self.assertEqual(document.core_type, "conference_proceedings")
        self.assertEqual(document.core_abstract, "")
        self.assertEqual(document.core_source, "Proceedings of the IADIS International Conference Game and Entertainment Technologies 2012")
        self.assertEqual(document.core_year, 2012)
        self.assertIsNotNone(document.core_authors)
        self.assertEqual(len(document.core_authors), 7)
        self.assertIsNotNone(document.core_keywords)
        self.assertEqual(len(document.core_keywords), 0)
        self.assertIsNotNone(document.tags)
        self.assertEqual(len(document.tags), 0)

         # check fourth document (97a6fc9e-70b3-321a-b1c6-477c1946cf3d)
        document = documents[3]
        self.assertEqual(document.core_title, "A framework for the creation of mobile games targeting dyslexic children")
        self.assertEqual(document.core_profile_id, "6fe24a7a-8eb8-3005-8d6a-71cdf48ce92d")
        self.assertEqual(document.core_id, "97a6fc9e-70b3-321a-b1c6-477c1946cf3d")
        self.assertEqual(document.core_type, "conference_proceedings")
        self.assertEqual(document.core_abstract, "")
        self.assertEqual(document.core_source, "IADIS Mobile Learning 2013")
        self.assertEqual(document.core_year, 2013)
        self.assertIsNotNone(document.core_authors)
        self.assertEqual(len(document.core_authors), 5)
        self.assertIsNotNone(document.core_keywords)
        self.assertEqual(len(document.core_keywords), 0)
        self.assertIsNotNone(document.tags)
        self.assertEqual(len(document.tags), 0)

    def test_get_documents_by_group_id(self):
        crwler = FileCrawler()

        # invalid id
        documents = crwler.get_documents_by_group_id('1bb8291f)-f619-35cf-9d43-b26e44fba327')
        self.assertIsNone(documents)

        # valid but not existing id
        documents = crwler.get_documents_by_group_id('notexisting-f619-35cf-9d43-b26e44fba327')
        self.assertIsNotNone(documents)
        self.assertEqual(0, len(documents))

        documents = crwler.get_documents_by_group_id('d0b7f41f-ad37-3b47-ab70-9feac35557cc')
        self.assertIsNotNone(documents)
        self.assertEqual(20, len(documents))