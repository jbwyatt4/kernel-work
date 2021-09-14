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

class ParseTrace:
	cpu_states = { # [core_id, pid]
		1: [],
		2: [],
		3: [],
		4: []
	}
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

	def process_main_state(cls):
		pass

	def process_sswitch_state(cls):
		pass

	def is_main_state(self):
		return self.state["CURRENT_STATE"] == self.state["STATES"]["MAIN_STATE"]

	def is_sswitch_state(self):
		return self.state["CURRENT_STATE"] == self.state["STATES"]["SSWITCH_STATE"]

	# get the other cpu id of the pair
	def get_cpu_pair(self, cpu_id):
		return self.cpu_pairs[cpu_id]

	# check if a pair event already exists
	# if so, remove the paired events and store in a matched value
	# if not, add the event to a list to compare future events against
	def check_cpu_pair(self, msg, cpu_id):
		event = msg.event
		pair_id = self.get_cpu_pair(cpu_id)
		e = EventRecord(event.name, msg, pair_id)
		if 0 < len(self.events_to_match[pair_id]):
			matched = self.events_to_match[pair_id].pop(0)
			self.found_pairs[pair_id].append([e, matched])
		else:
			self.events_to_match[pair_id].append(e)

	def find_events_to_match():
		pass

	def parse(msg_it):
		
		pass

	def __init__(self):
		state = {
			"STATES": {"MAIN_STATE": 0, "SSWITCH_STATE": 1},
			"CURRENT_STATE": 0
		}

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

irq_count = 0
sched_count = 0
unrelated_event_count = 0
not_event_msg_count = 0
p = ParseTrace()
i = 0

for msg in msg_it:

	if p.PARSE_LIMIT > i:
		i += 1
	else:
		break

	if type(msg) is not bt2._EventMessageConst:
		not_event_msg_count = not_event_msg_count + 1
		continue

	event = msg.event

	# Check if substring s is in event.name
	# we are looking for 'sched:...', etc
	if not any(s in event.name for s in p.CHECKED_EVENTS):
		unrelated_event_count = unrelated_event_count + 1
		m = 'Error: Unallowed Event: {}'
		print(m.format(event.name))
		exit(1)

	if p.CHECKED_EVENTS[0] in event.name:
		irq_count = irq_count + 1

	if p.CHECKED_EVENTS[1] in event.name:
		sched_count = sched_count + 1

	#if "sched:sched_switch" == event.name:
	if "sched:sched_core_thread_cookie" == event.name:
		#print(event.payload_field.keys)
		n = 'Flag: {} CPU: {} PID: {} Next Cookie: {} Reported Cookie: {}'
		print(n.format(event.payload_field["report_type"], event["cpu_id"], event.payload_field["perf_tid"], event.payload_field["next_cookie"], event.payload_field["core_group_cookie"]))
		p.check_cpu_pair(msg, event["cpu_id"])

#matched_events = p.find_events_to_match()

print("---------------------")
print("---------------------")
print("---------------------")
#print(matched_events)
print(p.events_to_match)
print(p.found_pairs)


m = """
Unrelated Event Count: {}
Not Event MSG Count: {}
IRQ + Sched Event Count: {}
"""
print (m.format(unrelated_event_count, not_event_msg_count, irq_count + sched_count))