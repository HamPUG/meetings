# Outputs all the descriptions of the sources

from pulsectl import Pulse

with Pulse('hampug') as pulse:
    for i in range(len(pulse.source_list())):
        s = pulse.source_list()[i]
        print(i, s.description)

