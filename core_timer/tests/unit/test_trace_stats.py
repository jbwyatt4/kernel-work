import unittest

from analyze_trace import *

class TraceStatsTest(unittest.TestCase):

	def test_determine_time_deltas(self):
		test_input = [
			{
				"msg": "",
				"data": [True, 1000, 1100],
			},
			{
				"msg": "",
				"data": [True, 2000, 2100],
			},
		]