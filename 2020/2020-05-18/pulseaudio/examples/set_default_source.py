# Sets the 4th source as default at 50% volume

from pulsectl import Pulse

with Pulse('hampug') as pulse:
    source = pulse.source_list()[4]
    pulse.default_set(source)
    source.volume.value_flat = 0.5
    pulse.volume_set(source, source.volume)

