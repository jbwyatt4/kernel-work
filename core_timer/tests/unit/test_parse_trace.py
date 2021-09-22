#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import unittest

from analyze_trace import *

class ParseTraceTest(unittest.TestCase):
	def test_check_events(self):
		test_input = [
			[
				"Check for Core Conflict Started",
				{0: [0, 100], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]},
				None,
				[],
				[1000]
			],
			[
				"Check for Core Conflict Resolved In Time",
				{0: [0, 0], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]},
				0,
				[
					[False, 1000, None],
				],
				[2000]
			],
		]
		solution = [
			"",
			"",
		]
		i = 0
		while i < len(test_input):
			msg = "\nBroken Test: {}\nMessage: {}".format(i, test_input[i][0])
			pt = ParseTrace()
			pt.cpu_states = test_input[i][1]
			pt.current_conflict = test_input[i][2]
			pt.conflicts_found = test_input[i][3]
			event_arr = test_input[i][4]
			ret = pt.check_events(event_arr)
			self.assertEqual(ret, solution[i], msg)
			i += 1
			print(pt.conflicts_found, pt.current_conflict)

	def test_do_cpu_cores_match(self):
		test_input = [
			[
				"Initial state",
				{0: [-1, -1], 1: [-1, -1], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"Task w/o core cookie + rest as initial state",
				{0: [0, 100], 1: [-1, -1], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"Second task w/o core cookie + rest as initial state",
				{0: [0, 100], 1: [0, 101], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"Task with a core cookie + Rest as initial state",
				{0: [1, 100], 1: [-1, -1], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"Task with a core cookie and task w/o: an invalid state + Rest as initial state",
				{0: [0, 100], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"Task with a core cookie and w/o, but as idle (PID: 0): a valid state + Rest as initial state",
				{0: [0, 0], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"2 Tasks with different cookies",
				{0: [1, 100], 1: [2, 101], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"Two tasks with the same cookie",
				{0: [1, 100], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"One task with cookie, the other at idle",
				{0: [1, 100], 1: [0, 101], 2: [-1, -1], 3: [-1, -1]}
			],
			[
				"Four tasks each with different cookies",
				{0: [1, 100], 1: [2, 101], 2: [3, 102], 3: [4, 103]}
			],
			[
				"Four tasks with the same cookie",
				{0: [1, 100], 1: [1, 101], 2: [1, 102], 3: [1, 103]}
			],
		]
		solution = [
			True,
			True,
			True,
			True,
			False,
			True,
			False,
			True,
			True,
			False,
			True,
		]
		i = 0
		while i < len(test_input):
			msg = "\nBroken Test: {}\nMessage: {}".format(i, test_input[i][0])
			pt = ParseTrace()
			pt.cpu_states = test_input[i][1]
			ret = pt.do_cpu_cores_match()
			self.assertEqual(ret, solution[i], msg)
			i += 1

if __name__ == '__main__':
	unittest.main()