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
	MILLSECOND_TOLERANCE = 0.01
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
	# We want to record multiple failed events to see if it produces a pattern
	# end_timestamp represents the
	conflicts_found = [] # [ [conflict_resolved: boolean, begin_timestamp, end_timestamp ] ]
	current_conflict = None # int to conflicts_found
	prev_event_msg = None

	# get the other cpu id of the pair
	def get_cpu_pair(self, cpu_id):
		return self.cpu_pairs[cpu_id]

	def check_events(self, **kwargs):
		timestamp = kwargs["timestamp"]
		# function: check/insert into tracked cases
		# we need to handle two cases

		# 1 where the current core selects a core
		# check if all have the same cookie when two conditions

		# 1) if they do not, do they get the same cookie in the desired time span?
		# 2) does another thread leave the coregroup state? (a core changes to something other 0 or the same coregroup-it actually should not change at all since it should be paused)

		# check when a next task is selected to be a core_group, are the others already's next selected for coregroup or has the time not expired?

		if self.do_cpu_cores_match():
			if int == type(self.current_conflict):

				# Check if within time limit
				diff = timestamp - self.conflicts_found[self.current_conflict][1]
				if self.TIME_TOLERANCE < diff:
					# Time difference greater than set time, set conflict time and move on
					print("B-CPU Cores Conflict Timed Out!")
				else:
					# Conflict within time, set resolved to true and move on
					self.conflicts_found[self.current_conflict][0] = True
					print("R-CPU Cores Conflict Resolved!")
				self.conflicts_found[self.current_conflict][2] = timestamp
				self.current_conflict = None
			else:
				print("S-CPU Cores Match!")
		else:
			if not self.current_conflict:
				self.current_conflict = len(self.conflicts_found)
				self.conflicts_found.append([False, timestamp, None])
				print("F-No Match!")
			else:
				print("F2-No Match Continues!")

	def do_cpu_cores_match(self) -> bool:
		tmp = -1
		for e in self.cpu_states.items():
			# We skip if nothing set before or task is at 0 which means idle thread
			if e[1][0] == -1 or e[1][1] == 0:
				continue
			else:
				# If no core cookie found yet, we keep track of it
				if tmp == -1:
					tmp = e[1][0]
				else:
					if tmp == e[1][0] or 0 == e[1][0]:
						continue
					else:
						return False
		return True

	def parse(self, msg_it):
		for msg in msg_it:
			if type(msg) is not bt2._EventMessageConst:
				self.ts.not_event_msg_count += 1
				continue

			event = msg.event
			timestamp = msg.default_clock_snapshot.ns_from_origin

			if "" == event.name:
				pass

			elif "sched:sched_core_thread_cookie" == event.name:
				#print(event.payload_field.keys)
				m1 = 'Flag: {} CPU: {} PID: {} Prev Cookie: {} Next Cookie: {} Reported Cookie: {} Timestamp: {}'
				print(m1.format(event.payload_field["report_type"], event["cpu_id"], event.payload_field["perf_tid"], event.payload_field["prev_cookie"], event.payload_field["next_cookie"], event.payload_field["core_group_cookie"], timestamp))

				self.cpu_states[event["cpu_id"]] = [event.payload_field["next_cookie"], event.payload_field["perf_tid"]]
				m2 = 'CPU States: {}'
				print("---")
				self.check_events(timestamp=timestamp)

			self.prev_event_msg = msg

	def print_report(self):
		pass

	def __init__(self):
		self.state = {
		}
		self.ts = TraceStats()

if __name__ == "__main__":
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