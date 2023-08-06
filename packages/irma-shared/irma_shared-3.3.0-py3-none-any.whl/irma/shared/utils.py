# Copyright (c) 2013-2019 Quarkslab.
# This file is part of IRMA project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.


import sys

if sys.version_info < (3, 6):
    from datetime import datetime, timedelta, timezone


def aware_datetime(dt):
    if dt.tzinfo:
        return dt

    # .astimezone on naive datetime is only available since python 3.6.
    # cf. https://bugs.python.org/issue24773
    if sys.version_info >= (3, 6):
        return dt.astimezone()
    else:
        # manually compute timezone if not available
        ud = datetime.utcnow()
        ld = datetime.now()
        minutes = (ld - ud) // timedelta(minutes=1)
        # NOTE: can only give minutes in python <3.6; otherwise raises
        #   ValueError: offset must be a timedelta representing a whole number
        #     of minutes, not datetime.timedelta(...)
        mytz = timezone(timedelta(minutes=minutes))
        return dt.replace(tzinfo=mytz)
