#
# Copyright (C) 2021-2022 DS-Homebrew
# Copyright (C) 2022 lifehackerhansol
#
# SPDX-License-Identifier: ISC
#

import json
from typing import Any, Dict


def loadSettings() -> Dict[str, Any]:
    # Load config
    with open("config.json", "r") as f:
        settings = json.load(f)

    ret = {}
    # bot internals
    ret['TOKEN'] = settings['DEFAULT']['TOKEN']
    ret['PREFIX'] = [x for x in settings['DEFAULT']['PREFIX']]
    ret['STATUS'] = settings['DEFAULT']['STATUS']

    # server specifics
    ret['GUILD'] = settings.get('GUILD')
    ret['staff_roles'] = [x for x in settings['MODERATOR']]
    ret['SETG_ROLE'] = settings['CLASS']['SETG']
    ret['SETH_ROLE'] = settings['CLASS']['SETH']
    ret['SETJ_ROLE'] = settings['CLASS']['SETJ']
    ret['DEFAULT_ROLE'] = settings['CLASS']['DEFAULT']

    # channels
    ret['WELCOME'] = settings['CHANNEL']['WELCOME']

    return ret
