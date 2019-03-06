# gameserver-rotator

This is a piece of software which can start/stop gameservers (or any kind of software)
at a given point in time.

## Requirements:

- Python >= 3.5
- aiohttp
- Jinja2

## how to install

1. `git clone https://github.com/991jo/gameserver-rotator.git`
2. `cd gameserver-rotator`
3. `python3 -m venv .`
4. `source bin/activate`
5. `pip install -r requirements.txt`

## how to run

either you can activate the virtual env first by running

```
source bin/activate
python3 main.py
```

or you can execute it directly via `bin/python3 main.py`.

## how to configure

The configuration is done in the data.json file.
The format should be pretty self-explanatory.
The description field may contain html markup.
