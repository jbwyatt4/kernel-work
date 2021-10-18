import unittest

from analyze_trace import *

class TraceStatsTest(unittest.TestCase):

	def test_determine_time_deltas(self):
		pt = ParseTrace()
		test_input = [
			{
				"msg": "",
				"data": pt.ntr(
					conflict_resolved=True,
					begin_timestamp=1000,
					end_timestamp=1100,
				),
			},
			{
				"msg": "",
				"data": pt.ntr(
					conflict_resolved=True,
					begin_timestamp=2000,
					end_timestamp=2100,
				),
			},
		]