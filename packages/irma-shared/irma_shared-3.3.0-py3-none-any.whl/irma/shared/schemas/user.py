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


class User:

    def __init__(self, id,
                 username,
                 display_name=None,
                 permissions=[],
                 superuser=False):
        self.id = id
        self.username = username
        self.display_name = display_name or username
        self.permissions = permissions
        self.superuser = superuser

    def __repr__(self):
        return "User." + str(self.id)

    def __str__(self):
        ret = "User{"
        ret += "id: {}; ".format(self.id)
        ret += "username: {}; ".format(self.username)
        ret += "display_name: {}; ".format(self.display_name)
        ret += "permissions: {}; ".format(self.permissions)
        ret += "superuser: {}; ".format(self.superuser)
        ret += "}"
        return ret

    def __eq__(self, other):
        """
        Checks for same user, not equal content.
        """
        return (
            isinstance(other, User)
            and self.id == other.id
            )

    def __ne__(self, other):
        return not (self == other)


class UserSchema(Schema):
    _obj_class = User
    id = fields.Integer(required=True)
    username = fields.String(required=True)
    display_name = fields.String(allow_none=True)
    permissions = fields.List(fields.String(), allow_none=True)
    superuser = fields.Boolean(allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        if self._obj_class is None:
            raise TypeError("Cannot instantiate {}, set _obj_class.".format(
                self.__class__))
        return self._obj_class(**data)


class UserWithPasswordSchema(UserSchema):
    _obj_class = None
    password = fields.String(allow_none=True)
