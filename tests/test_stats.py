import unittest

from jacodemon.service.dsda.stats import *


class TestStats(unittest.TestCase):

    def test_ParseLevelStats(self):
        input1 = "E1M1 - 0:09.80 (0:09)  K: 2/2  I: 2/7  S: 1/1"
        input2 = "MAP03 - 0:22.17 (0:22)  K: 2/2  I: 6/7  S: 1/1"
        input3 = "E1M1 - 0:02.06 (0:02)  K: 0/2  I: 0/7  S: 0/1"
        input4 = "MAP09 - 59:05.09 (59:05)  K: 307/312  I: 53/57  S: 5/7"

        actual1 = ParseLevelStats(input1)
        actual2 = ParseLevelStats(input2)
        actual3 = ParseLevelStats(input3)
        actual4 = ParseLevelStats(input4)

        self.assertEqual(actual1["Time"], "0:09.80", f"Time was {actual1['Time']}")
        self.assertEqual(actual1["Kills"], "2/2", f"Kills was {actual1['Kills']}")
        self.assertEqual(actual1["Items"], "2/7", f"Items was {actual1['Items']}")
        self.assertEqual(actual1["Secrets"], "1/1", f"Secrets was {actual1['Secrets']}")

        self.assertEqual(actual2["Time"], "0:22.17", f"Time was {actual2['Time']}")
        self.assertEqual(actual2["Kills"], "2/2", f"Kills was {actual2['Kills']}")
        self.assertEqual(actual2["Items"], "6/7", f"Items was {actual2['Items']}")
        self.assertEqual(actual2["Secrets"], "1/1", f"Secrets was {actual2['Secrets']}")

        self.assertEqual(actual3["Time"], "0:02.06", f"Time was {actual3['Time']}")
        self.assertEqual(actual3["Kills"], "0/2", f"Kills was {actual3['Kills']}")
        self.assertEqual(actual3["Items"], "0/7", f"Items was {actual3['Items']}")
        self.assertEqual(actual3["Secrets"], "0/1", f"Secrets was {actual3['Secrets']}")

        self.assertEqual(actual4["Time"], "59:05.09", f"Time was {actual4['Time']}")
        self.assertEqual(actual4["Kills"], "307/312", f"Kills was {actual4['Kills']}")
        self.assertEqual(actual4["Items"], "53/57", f"Items was {actual4['Items']}")
        self.assertEqual(actual4["Secrets"], "5/7", f"Secrets was {actual4['Secrets']}")
