#
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
from marshmallow import fields, Schema, post_load


class NotificationSchema(Schema):
    description = fields.String()
    file_ext_id = fields.UUID()
    created_at = fields.Integer()

    @post_load
    def make_object(self, data, **kwargs):
        return Notification(**data)


class Notification:

    def __init__(self, description=None, file_ext_id=None, created_at=None):
        self.description = description
        self.file_ext_id = str(file_ext_id)
        self.created_at = created_at

    def __str__(self):
        ret = "Notification{"
        ret += "description: {}; ".format(self.description)
        ret += "file_ext_id: {}; ".format(self.file_ext_id)
        ret += "created_at: {}; ".format(self.created_at)
        ret += "}"
        return ret
