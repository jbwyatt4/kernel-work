#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import bt2
import sys
from pprint import pprint

class ParseTrace:
	CHECKED_EVENTS = ['irq:', 'sched:']

	def process_main_state(cls):
		pass

	def process_sswitch_state(cls):
		pass

	def is_main_state(self):
		return self.state["CURRENT_STATE"] == self.state["STATES"]["MAIN_STATE"]

	def is_sswitch_state(self):
		return self.state["CURRENT_STATE"] == self.state["STATES"]["SSWITCH_STATE"]

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
	if not any(s in event.name for s in ParseTrace.CHECKED_EVENTS):
		unrelated_event_count = unrelated_event_count + 1
		m = 'Error: Unallowed Event: {}'
		print(m.format(event.name))
		exit(1)

	if ParseTrace.CHECKED_EVENTS[0] in event.name:
		irq_count = irq_count + 1

	if ParseTrace.CHECKED_EVENTS[1] in event.name:
		sched_count = sched_count + 1

	if "sched:sched_switch" == event.name:
		m = 'CPU of sched_switch: {}'
		print(m.format(event.packet.context_field["cpu_id"]))

m = """
Unrelated Event Count: {}
Not Event MSG Count: {}
IRQ + Sched Event Count: {}
"""
print (m.format(unrelated_event_count, not_event_msg_count, irq_count + sched_count))