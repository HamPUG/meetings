# Outputs details of the default sink/source

from pulsectl import Pulse, PulseVolumeInfo

with Pulse('hampug') as pulse:
    def_source = pulse.server_info().default_source_name
    print("\nsource", def_source)
    for s in pulse.source_list():
        if s.name == def_source:
            print("- name:", s.name)
            print("- desc:", s.description)
            if s.port_active is not None:
                print("- port name:", s.port_active.name)
                print("- port desc:", s.port_active.description)
            print("- volume: ", s.volume.value_flat, s.volume.values)
    
    def_sink = pulse.server_info().default_sink_name
    print("\nsink:", def_sink)
    for s in pulse.sink_list():
        if s.name == def_sink:
            print("- name:", s.name)
            print("- desc:", s.description)
            if s.port_active is not None:
                print("- port name:", s.port_active.name)
                print("- port desc:", s.port_active.description)
            print("- volume: ", s.volume.value_flat, s.volume.values)

