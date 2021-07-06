#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import bt2
import sys
import datetime

def get_seconds_from_second_input(metadata_path):
	"""To workaround an issue with perf the take_trace.sh saves the current seconds from Unix epoch to a file called perf.meta to be read later by this function.
	
	This has nothing to do with the metadata already in the ctf folder."""

	with open(metadata_path,'r') as f:
		return int(f.readline())

trace_file_path = sys.argv[1]
trace_meta_path = sys.argv[2]

# Find the `ctf` plugin (shipped with Babeltrace 2).
ctf_plugin = bt2.find_plugin('ctf')

# Get the `source.ctf.fs` component class from the plugin.
fs_cc = ctf_plugin.source_component_classes['fs']

# Create a trace collection msg iterator from the first
# cmd-line arg
msg_it = bt2.TraceCollectionMessageIterator(bt2.ComponentSpec(fs_cc, {
	# Get the CTF trace path from the first command-line argument.
	'inputs': [sys.argv[1]],
		# Set the time origin so babeltrace2 does not print the Unix epoch
	'clock-class-offset-s': get_seconds_from_second_input(trace_meta_path),
}))
checked_events = ['irq:irq_handler_entry', 'sched:sched_switch', 'sched:sched_core_thread_cookie']
irq1 = 0
sswitch = 0
sched = 0
last_event_ns_from_origin = None

for msg in msg_it:

	if type(msg) is not bt2._EventMessageConst:
		continue

	event = msg.event

	if event.name not in checked_events:
		#msg = 'Event: {}'
		#print(msg.format(event.name))
		continue

	if event.name == checked_events[0]:
		if irq1 < 5:
			msg = 'Event: {}'
			print(msg.format(event.name))
		irq1 = irq1 + 1

	if event.name == checked_events[1]:
		if sswitch < 5:
			prev_comm = event['prev_comm']
			next_comm = event['next_comm']
			ns_from_origin = msg.default_clock_snapshot.ns_from_origin
			dt = datetime.datetime.fromtimestamp(ns_from_origin / 1e9)
			# Compute the time difference since the last event message.
			diff_s = 0
			if last_event_ns_from_origin is not None:
				diff_s = (ns_from_origin - last_event_ns_from_origin) / 1e9
			msg = 'Event: {} | Clock Val: {} | NS from Origin: {} | Switching process: `{}` → `{}`'
			print(msg.format(event.name, dt, diff_s, prev_comm, next_comm))
			fmt = '{} (+{:.6f} s): {}'
			print(fmt.format(dt, diff_s, event.name))
			last_event_ns_from_origin = ns_from_origin
		sswitch = sswitch + 1

	if event.name == checked_events[2]:
		if sched < 5:
			msg = 'Event: {}'
			print(msg.format(event.name))
		sched = sched + 1

	if irq1 >= 5 and sswitch >= 5:
		exit(0)