#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import bt2
import sys
from pprint import pprint

class EventRecord:
	def __init__(self, event_type, cpu_core, time_stamp):
		self.event_type = event_type
		self.cpu_core = cpu_core
		self.time_stamp = time_stamp

class ParseTrace:
	CHECKED_EVENTS = ['irq:', 'sched:']
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
		2: [],
		4: []
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
	def get_cpu_pair(self, event, cpu_id):
		return self.cpu_pairs[cpu_id]

	# check if a pair event already exists
	# if so, remove the paired events and store in a matched value
	# if not, add the event to a list to compare future events against
	def check_cpu_pair(self, msg, cpu_id):
		event = msg.event
		pair_id = self.get_cpu_pair(event, cpu_id)
		e = EventRecord(event.name, cpu_id, msg.default_clock_snapshot.ns_from_origin)
		if 0 < len(self.events_to_match[pair_id]):
			matched = self.events_to_match[pair_id].pop(0)
			#found_pairs
		else:
			self.events_to_match[pair_id].append(e)

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

for msg in msg_it:

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

	if "sched:sched_switch" == event.name:
		m = 'CPU of sched_switch: {}'
		print(m.format(event.packet.context_field["cpu_id"]))
		print(m.format(event["cpu_id"]))
		print(event.payload_field.keys)
		t = msg.default_clock_snapshot.ns_from_origin
		p.check_cpu_pair(msg, event["cpu_id"])


m = """
Unrelated Event Count: {}
Not Event MSG Count: {}
IRQ + Sched Event Count: {}
"""
print (m.format(unrelated_event_count, not_event_msg_count, irq_count + sched_count))