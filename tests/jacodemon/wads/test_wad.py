import unittest
import os

from jacodemon.wads.wad import GetInfoFromFiles, GetMapEntriesFromFiles

class TestD2ISO(unittest.TestCase):

    test_wad = "D2ISOv2.wad"
    test_file_root = "tests/data/thirdparty"
    test_file_path = os.path.join(test_file_root, test_wad)
    wad_link = "https://www.doomworld.com/idgames/levels/doom2/megawads/d2isov2"

    def test_GetInfoFromWad_D2ISO(self):

        if not os.path.exists(self.test_file_path):
            raise Exception(f"{self.test_wad} not found in {self.test_file_root}\nObtain from {self.wad_link}")

        gameinfo = GetInfoFromFiles([self.test_file_path])

        # D2ISO has no info lumps afaik
        self.assertEqual(gameinfo, {})

    def test_GetMapEntriesFromWad_D2ISO(self):

        if not os.path.exists(self.test_file_path):
            raise Exception(f"{self.test_wad} not found in {self.test_file_root}\nObtain from {self.wad_link}")

        mapentries = GetMapEntriesFromFiles([self.test_file_path])

        self.assertEqual(mapentries[0], {'MapId': 'MAP01'})

class TestEviternity2(unittest.TestCase):

    test_wad = "eviternity2.wad"
    test_file_root = "tests/data/thirdparty"
    test_file_path = os.path.join(test_file_root, test_wad)
    wad_link = "https://eviternity.dfdoom.com/"

    def test_GetInfoFromWad_Eviternity2(self):

        if not os.path.exists(self.test_file_path):
            raise Exception(f"{self.test_wad} not found in {self.test_file_root}\nObtain from {self.wad_link}")

        gameinfo = GetInfoFromFiles([self.test_file_path])

        self.assertEqual(gameinfo['Title'], "Eviternity II")
        self.assertEqual(gameinfo['IWAD'], "DOOM2.WAD")
        self.assertEqual(gameinfo['complevel'], "mbf21")

    def test_GetMapEntriesFromWad_Eviternity2(self):

        if not os.path.exists(self.test_file_path):
            raise Exception(f"{self.test_wad} not found in {self.test_file_root}\nObtain from {self.wad_link}")

        mapentries = GetMapEntriesFromFiles([self.test_file_path])

        # unlucky for some, but this has a secret exit
        mapentry = mapentries[13]
        self.assertEqual(mapentry['MapId'], 'MAP14')
        self.assertEqual(mapentry['MapName'], 'Equanimity')
        self.assertEqual(mapentry['ParTime'], '540')
        self.assertEqual(mapentry['NextSecretMap'], 'MAP33')
