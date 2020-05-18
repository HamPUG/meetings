# Outputs the default pulseaudio source/sink

from pulsectl import Pulse

with Pulse('nzpug') as pulse:
    print("source", pulse.server_info().default_source_name)
    print("sink", pulse.server_info().default_sink_name)

