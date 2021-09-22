#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import unittest

from analyze_trace import *

class ParseTraceTest(unittest.TestCase):
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
		]
		solution = [
			True,
			True,
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

# test = {0: [1, 100], 1: [2, 101], 2: [-1, -1], 3: [-1, -1]}
# ret = pt.do_cpu_cores_match(test)
# print("True") if ret else print("False")

# test = {0: [1, 100], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
# ret = pt.do_cpu_cores_match(test)
# print("True") if ret else print("False")

# test = {0: [1, 100], 1: [0, 101], 2: [-1, -1], 3: [-1, -1]}
# ret = pt.do_cpu_cores_match(test)
# print("True") if ret else print("False")

# # Check for Conflict Started
# pt.cpu_states = {0: [0, 100], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
# pt.current_conflict = None
# pt.conflicts_found = []
# event_arr = [10]
# ret = pt.check_events(event_arr)
# # need to print out the state
# print(pt.conflicts_found, pt.current_conflict)

# # Check for Conflict Resolved In Time
# pt.cpu_states = {0: [0, 0], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
# pt.current_conflict = 0
# pt.conflicts_found = [
# 	[False, 10, None]
# ]
# event_arr = [20]
# ret = pt.check_events(event_arr)