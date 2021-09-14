#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import bt2
import sys
from pprint import pprint

class EventRecord:
	def __init__(self, event_type, msg, cpu_pair_id):
		self.event_type = event_type
		self.msg = msg
		self.cpu_id = msg.event["cpu_id"]
		self.cpu_pair_id = cpu_pair_id
		self.time_stamp = msg.default_clock_snapshot.ns_from_origin # Nanoseconds from start of trace
		self.tracking_groups = []
		self.successful_groups = []
		self.failed_groups = []

class TraceStats:
	def __init__(self):
		self.not_event_msg_count = 0

class ParseTrace:
	CHECKED_EVENTS = ['irq:', 'sched:']
	PARSE_LIMIT = 250 # How many events must be iterated before parsing stops
	MILLSECOND_TOLERANCE = 100
	TIME_TOLERANCE = MILLSECOND_TOLERANCE * 1000000 # In Nanoseconds, a couple hundred microseconds, the amount recorded in the traces
	cpu_pairs = { # hardcoded, make dynamic later
		0: 1,
		1: 0,
		2: 3,
		3: 2
	}
	events_to_match = { # hardcoded, make dynamic later
		0: [],
		1: [],
		2: [],
		3: []
	}
	found_pairs = { # hardcoded, make dynamic later
		0: [],
		1: [],
		2: [],
		3: []
	}
	cpu_states = { # [cookie, pid]
		0: [-1, -1],
		1: [-1, -1],
		2: [-1, -1],
		3: [-1, -1]
	}

	# get the other cpu id of the pair
	def get_cpu_pair(self, cpu_id):
		return self.cpu_pairs[cpu_id]

	def find_events_to_match(self):
		pass

	def do_cpu_cores_match(cls, cpu_states: dict) -> bool:
		tmp = -1
		for e in cpu_states:
			if e[1] == -1 or e[1] == 0:
				next
			else:
				if tmp == -1:
					tmp = e[0]
				else:
					if tmp == e[0]:
						pass
					else:
						return False
		return True

	def parse(self, msg_it):
		for msg in msg_it:
			if type(msg) is not bt2._EventMessageConst:
				self.ts.not_event_msg_count += 1
				continue

			event = msg.event

			if "" == event.name:
				pass

			elif "sched:sched_core_thread_cookie" == event.name:
				#print(event.payload_field.keys)
				m1 = 'Flag: {} CPU: {} PID: {} Prev Cookie: {} Next Cookie: {} Reported Cookie: {} Timestamp: {}'
				print(m1.format(event.payload_field["report_type"], event["cpu_id"], event.payload_field["perf_tid"], event.payload_field["prev_cookie"], event.payload_field["next_cookie"], event.payload_field["core_group_cookie"], msg.default_clock_snapshot.ns_from_origin))

				self.cpu_states[event["cpu_id"]] = [event.payload_field["next_cookie"], event.payload_field["perf_tid"]]
				m2 = 'CPU States: {}'
				print("---")
				#print(m2.format(print(self.cpu_states)))

				# function: check/insert into tracked cases
				# we need to handle two cases
				# 1 where the current core selects a core

				# check if all have the same cookie when two conditions
				# 1) if they do not, do they get the same cookie in the desired time span?
				# 2) does another thread leave the coregroup state? (a core changes to something other 0 or the same coregroup-it actually should not change at all since it should be paused)
				# -
				# check when a next task is selected to be a core_group, are the others already's next selected for coregroup or has the time not expired
				if self.do_cpu_cores_match(self.cpu_states):
					print("S-CPU Cores Match!")
				else:
					print("F-NO MATCH!")

				# function: look at cases, see if they need to be ignored (under time), added to succeed, added to failed

			else:
				pass

	def print_report(self):
		pass

	def __init__(self):
		self.state = {
		}
		self.ts = TraceStats()

trace_file_path = sys.argv[1]

# Find the `ctf` plugin (shipped with Babeltrace 2).
ctf_plugin = bt2.find_plugin('ctf')

# Get the `source.ctf.fs` component class from the plugin.
fs_cc = ctf_plugin.source_component_classes['fs']

# Create a trace collection msg iterator from the first
# cmd-line arg
msg_it = bt2.TraceCollectionMessageIterator(bt2.ComponentSpec(fs_cc, {
	# Get the CTF trace path from the first command-line argument.
	'inputs': [trace_file_path],
}))

p = ParseTrace()
p.parse(msg_it)
p.print_report()