#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

pt = ParseTrace()

# Initial state
test = {0: [-1, -1], 1: [-1, -1], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

# Task w/o core cookie + Rest as initial state
test = {0: [0, 100], 1: [-1, -1], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

# Second task w/o core cookie + Rest as initial state
test = {0: [0, 100], 1: [0, 101], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

# Task with a core cookie + Rest as initial state
test = {0: [1, 100], 1: [-1, -1], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

# Task with a core cookie and w/o: an invalid state + Rest as initial state
test = {0: [0, 100], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

# Task with a core cookie and w/o, but as idle (PID: 0): a valid state + Rest as initial state
test = {0: [0, 0], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

test = {0: [1, 100], 1: [2, 101], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

test = {0: [1, 100], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

test = {0: [1, 100], 1: [0, 101], 2: [-1, -1], 3: [-1, -1]}
ret = pt.do_cpu_cores_match(test)
print("True") if ret else print("False")

# Check for Conflict Started
pt.cpu_states = {0: [0, 100], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
pt.current_conflict = None
pt.conflicts_found = []
event_arr = [10]
ret = pt.check_events(event_arr)
# need to print out the state
print(pt.conflicts_found, pt.current_conflict)

# Check for Conflict Resolved In Time
pt.cpu_states = {0: [0, 0], 1: [1, 101], 2: [-1, -1], 3: [-1, -1]}
pt.current_conflict = 0
pt.conflicts_found = [
	[False, 10, None]
]
event_arr = [20]
ret = pt.check_events(event_arr)