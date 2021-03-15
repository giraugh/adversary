import sys
import argparse
import textwrap
import arrow
from ics import Calendar, Event

valid_freqs = ["year", "month", "day"]

def ordinal(i):
    ld = int(str(i)[-1])
    if 11 <= i <= 20:
        return 'th'
    if ld == 1:
        return 'st'
    elif ld == 2:
        return 'nd'
    elif ld == 3:
        return 'rd'
    return 'th'

def format_name(name_pattern, i):
    name = name_pattern
    name = name.replace('{}', str(i))
    name = name.replace('{s}', 's' if i > 1 else '')
    name = name.replace('{st}', ordinal(i))
    return name

def create_recurring_event(name_pattern, index, date, time, duration):
    e = Event()
    i = index + 1
    e.name = format_name(name_pattern, index + 1)
    e.begin = date
    if time == None:
        e.make_all_day()
    else:
        [time_hours, time_mins] = time.split(':')
        e.begin = e.begin.shift(hours=int(time_hours), minutes=int(time_mins)).replace(tzinfo='local').to('utc')
        if duration != None:
            [dur_hours, dur_mins] = duration.split(':')
            e.duration = {"hours": int(dur_hours), "minutes": int(dur_mins)}
    return e

def create_recurring_events(name_pattern, start, freq, count, time=None, duration=None):
    start = arrow.get(start, 'DD/MM/YYYY')
    dates = [start.shift(**{freq + "s": i}) for i in range(1, count+1)]
    events = [create_recurring_event(name_pattern, i, date, duration, time) for i, date in enumerate(dates)]
    
    return events

def create_cal(name_pattern, start, freq, count, filename='', time=None, duration=None):
    # Validate arguments
    if freq not in valid_freqs:
        sys.stderr.write(f"Invalid frequency '{freq}'. Valid frequencies are {', '.join(valid_freqs)}\n")
        return

    if duration != None and time == None:
        sys.stderr.write(f"Must specify an event time when specifying a duration.\n")
        return

    if duration != None:
        pass # TODO: regexp validate

    # Create a calendar and add the events
    c = Calendar()
    events = create_recurring_events(name_pattern, start, freq, count, duration, time)
    for event in events:
        c.events.add(event)

    # Output to file or stdout
    if filename != '':
        with open(filename, "w") as icsf:
            icsf.writelines(c)
    else:
        print(c)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="adversary",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Adversary: Create ics calendars with dynamic repeating events.
            
            substitution rules:
                The namepattern field can contain substitution characters such
                as {} which are swapped out for event-specific fields. More details are provided below.

                {}      Index of event (1-indexed)
                {s}     plural suffix ("s" if index is greater than 1)
                {st}    ordinal suffix ("st"/"nd"/"rd"/"th" dependent on index)

            example usage:
                adversary -f birthdays.ics "{} Year{s} Old" "10/03/1998" 20 year
                adversary -f move-in.ics "{}{st} Mensiversary of Moving In" "02/01/2015" 30 month
            """)
    )
    parser.add_argument('namepattern', type=str, help="Name pattern for events. See substitution rules above for more.")
    parser.add_argument('startdate', type=str, help="Start date for events in DD/MM/YYYY format.")
    parser.add_argument('count', type=int, help="Number of events to create.")
    parser.add_argument('freq', type=str, choices=valid_freqs, help="How often to repeat the event.")
    parser.add_argument('-t', '--time', default=None, type=str, help="Start time of event in 24-hour HH:MM format (local time).")
    parser.add_argument('-d', '--duration', default=None, type=str, help="Duration of event in HH:MM format.")
    parser.add_argument('-f', dest='out', default='', type=str, help='Output filename.')
    args = parser.parse_args()

    create_cal(
        args.namepattern,
        args.startdate,
        args.freq,
        args.count,
        filename=args.out,
        duration=args.duration,
        time=args.time
    )
