# -*- coding: utf-8 -*-
##############################################################################
#
#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015 Mariano Ruiz (<https://github.com/mrsarm/mongotail>).
#
#  Author: Mariano Ruiz <mrsarm@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import re, json
from bson import ObjectId, DBRef, regex
from datetime import datetime
from uuid import UUID

REGEX_TYPE = type(re.compile(""))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return "ObjectId(%sObjectId)" % str(o)
        if isinstance(o, UUID): 
            return "UUID(%sUUID)" % str(o)
        if isinstance(o, DBRef):
            return "DBRef(Field(%sField), ObjectId(%sObjectId)DBRef)" % (o.collection, str(o.id))
        if isinstance(o, datetime):
            try:
                return "ISODate(" + o.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "ZISODate)"
            except ValueError:
                return "ISODate(" + o.isoformat()[:-3] + "ZISODate)"
        if isinstance(o, (REGEX_TYPE, regex.Regex)):
            return {"$regex": o.pattern}
        return json.JSONEncoder.default(self, o)

    def encode(self, o):
        result = super(JSONEncoder, self).encode(o)
        result = result.replace('Field(', '"')
        result = result.replace("Field)", '"')
        result = result.replace('ObjectId(', 'ObjectId("')
        result = result.replace('"ObjectId(', 'ObjectId(')
        result = result.replace('ObjectId)"', '")')
        result = result.replace('ObjectId)', '")')
        result = result.replace('"DBRef(', 'DBRef(')
        result = result.replace("DBRef)\"", ')')
        result = result.replace("\"ISODate(", "ISODate(\"")
        result = result.replace("ISODate)\"", "\")")
        result = result.replace("\"UUID(", "UUID(\"")
        result = result.replace("UUID)\"", "\")")
        return result
