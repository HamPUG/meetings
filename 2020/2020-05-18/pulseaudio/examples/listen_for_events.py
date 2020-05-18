# Listens for events

from pulsectl import Pulse

with Pulse('nzpug') as pulse:
  def print_events(ev):
    print('Pulse event:', ev)

  pulse.event_mask_set('all')
  pulse.event_callback_set(print_events)
  pulse.event_listen()
