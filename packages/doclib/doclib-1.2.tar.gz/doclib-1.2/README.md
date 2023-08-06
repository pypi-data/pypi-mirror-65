# **DocLib**
A chatbot library for euphoria.io.
# Usage
## Installation
To install, use `pip` or `pip3`:
```bash
pip3 install doclib
```
## Basic Bots
A basic bot will be a `Bot` object, constructed with a `nick`(the bot's name, shown in the room), a `room`(where the bot is sent by default, defaults to bots or test in debug mode), and an `owner`(your euphoria username.):
```python
from doclib import Bot
sampleBot = Bot(nick = 'bugBot', room = 'test', owner = 'sample user')
```
Once constructed, the user should assign a regex dictionary if planning to use `simple_start`:
```python
sampleBot.set_regexes({'^!command$' : function, '(?i)word' : 'response'})
```
