# adversary
Create ics calendars with dynamic repeating events.

## Usage
`adversary [-h] [-t T] [-d D] [-f OUT] namepattern startdate count {year, month, day}`

### Substitution Rules

The namepattern field can contain substitution characters such
as {} which are swapped out for event-specific fields. More details are provided below.

| symbol | substitution |
| :----- | :----------- |
| `{}`     | Index of event (1-indexed) |
| `{s}`    | plural suffix ("s" if index is greater than 1) |
| `{st}`   | ordinal suffix ("st"/"nd"/"rd"/"th" dependent on index) |

### Positional Arguments

| argument | description |
| :------- | :---------- |
|namepattern           | Name pattern fo events. See substitution rules above for more.|
|startdate             | Start date for events in DD/MM/YYYY format.|
|count                 | Number of events to create.|
|{year, month, day}      | How often to repeat the event.|

### Optional Arguments
| argument | description |
| :------- | :---------- |
|  -h, --help            | show usage/help message and exit. |
|  -f OUT                | Specify output filename. |
|  (-t/--time) TIME| Specify start time of event in 24-hour HH:MM format (local time). |
|  (-d/--duration) DURATION | Specify duration of event in HH:MM format. |

## Examples 
Show the age of a child born on the 10th of March 1998 each year for 20 years.
```bash
adversary -f birthdays.ics "{} Year{s} Old" "10/03/1998" 20 year`
```

Show each mensiversary of moving into a new house on the 2nd of January 2015.
```bash
adversary -f move-in.ics "{}{st} Mensiversary of Moving In" "02/01/2015" 30 month`
```

## Building
Adversary is written in python3 using the `ics` and `arrow` pip modules.

First clone the repo and cd into it
```bash
git clone https://github.com/giraugh/adversary
cd adversary
```

Then setup a virtualenv to install the dependencies seperately to your global installation.
```bash
python -m venv .venv
```
You should see your promot update with the venv name `.venv`.

Now install the pip modules from the freeze file `requirements.txt`.
```bash
pip install -r requirements.txt
```

Now you can run the python file with
```bash
python main.py
```

## Contributing
Any and all PRs and issues are welcomed. Just check if your issue has already been created before creating a new one.

## License
Adversary is licensed under the [MIT license](https://mit-license.org/).
Copyright © 2021 Ewan Breakey 
