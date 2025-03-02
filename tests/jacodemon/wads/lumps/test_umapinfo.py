import unittest

from jacodemon.wads.lumps.umapinfo import parse_umapinfo

class TestCsv(unittest.TestCase):

    def test_parse_doom2_umapinfo(self):

        # nicked from Eternity II
        input = b'MAP MAP01\r\n{\r\n\tlevelname = "Elysium"\r\n\tnext = "MAP02"\r\n\tskytexture = "OSKY50"\r\n\tpartime = 105\r\n\tepisode = "M_EPI1", "Withered", "1"\r\n\tintertext = "As the Archangelus crumbled to dust",\r\n\t\t\t\t"Undone by pride, in fate\'s cruel thrust",\r\n\t\t\t\t" ",\r\n\t\t\t\t"His kingdom, once vibrant, paid the cost",\r\n\t\t\t\t"Withered away, now moribund, lost",\r\n\t\t\t\t" ",\r\n\t\t\t\t"But the scent of evil, the echo of fate",\r\n\t\t\t\t"Persisted, clung, refused to abate",\r\n\t\t\t\t" ",\r\n\t\t\t\t"An Astral sentinel, brooding presence",\r\n\t\t\t\t"The source of this unholy essence",\r\n\t\t\t\t" ",\r\n\t\t\t\t"So with teeth clenched, heart ablaze", \r\n\t\t\t\t"Striding forwards as the world decays",\r\n\t\t\t\t" ",\r\n\t\t\t\t"Once more thou ascends the fiery skies",\r\n\t\t\t\t"To wage the battle that never dies"\r\n\tinterbackdrop = "OMRBLF00"\r\n\tlevelpic = "CWILV00"\r\n}\r\n\r\n'
        actual = parse_umapinfo(input)
        self.assertEqual(actual['MAP01']['levelname'], "Elysium")
        self.assertEqual(actual['MAP01']['partime'], "105")
        self.assertEqual(actual['MAP01']['next'], "MAP02")

    def test_parse_doom1_umapinfo(self):
        input = b'MAP E1M1\r\n{\r\n\tlevelname = "Elysium"\r\n\tnext = "E1M2"\r\n\tskytexture = "OSKY50"\r\n\tpartime = 105\r\n\tepisode = "M_EPI1", "Withered", "1"\r\n\tintertext = "As the Archangelus crumbled to dust",\r\n\t\t\t\t"Undone by pride, in fate\'s cruel thrust",\r\n\t\t\t\t" ",\r\n\t\t\t\t"His kingdom, once vibrant, paid the cost",\r\n\t\t\t\t"Withered away, now moribund, lost",\r\n\t\t\t\t" ",\r\n\t\t\t\t"But the scent of evil, the echo of fate",\r\n\t\t\t\t"Persisted, clung, refused to abate",\r\n\t\t\t\t" ",\r\n\t\t\t\t"An Astral sentinel, brooding presence",\r\n\t\t\t\t"The source of this unholy essence",\r\n\t\t\t\t" ",\r\n\t\t\t\t"So with teeth clenched, heart ablaze", \r\n\t\t\t\t"Striding forwards as the world decays",\r\n\t\t\t\t" ",\r\n\t\t\t\t"Once more thou ascends the fiery skies",\r\n\t\t\t\t"To wage the battle that never dies"\r\n\tinterbackdrop = "OMRBLF00"\r\n\tlevelpic = "CWILV00"\r\n}\r\n\r\n'
        actual = parse_umapinfo(input)
        self.assertEqual(actual['E1M1']['levelname'], "Elysium")
        self.assertEqual(actual['E1M1']['partime'], "105")
        self.assertEqual(actual['E1M1']['next'], "E1M2")
