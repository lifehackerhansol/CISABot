# CISABot

## How to use

1. Make a copy of `config.json.example` and name it `config.json`.
1. Set your bot's token ID.
    - You will need to create a bot over at [Discord Developer Portal](https://discord.com/developers/applications).
1. Configure stuff in `config.json` tailored to your server.
    - Bot does not support more than one server at this time.
1. (Optional) Set your command prefix to whatever you like.
    - Default is `.`
1. Install the following for your host:
    - Python 3.9.x (and its respective pip)
1. Run `pip install -r requirements.txt`
1. Run the following command:
    - UNIX-based: `python3 cisa.py`
    - Windows: `py cisa.py`

## License

```
   Copyright 2021-2023 lifehackerhansol

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

## Credits
- Discord.py: This wouldn't exist without it
- [Nintendo Homebrew's Kurisu](https://github.com/nh-server/kurisu): `utils.py` error embeds, `load.py`
