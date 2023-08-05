# -*- coding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, ERP-PLM-CAD Open Source Solutions
#    Copyright (C) 2011-2020 https://OmniaSolutions.website
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this prograIf not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
'''
Created on 4 Apr 2020

@author: mboscolo
'''
import logging
from flask_table import Table
from .convetion import FT_TRYTON_FIELD_ATTRIBUTE_MAPPING

class FTTable(Table):
    trytonObject = None
    tryton_fields_name = {}
    def __init__(self ,*arg, **args):
        if self.trytonObject:
            items = []
            tryton_search = args.get('tryton_search', [])
            tmp_data = self.trytonObject.search(tryton_search)
            if not self.tryton_fields_name:
                self.tryton_fields_name=self.trytonObject._fields.keys()
            # define the header
            available_fields = []
            for fields_name in self.tryton_fields_name:
                 field = self.trytonObject._fields.get(fields_name)
                 FTField = FT_TRYTON_FIELD_ATTRIBUTE_MAPPING.get(field._type)
                 if FTField:
                     self.add_column(fields_name, FTField(fields_name))
                     available_fields.append(fields_name)
                 else:
                     logging.warning("Field Not supported %s" % field._type)
            # order the data
            for data in tmp_data:
                row = {}
                for fields_name in available_fields:
                    row[fields_name ] = getattr(data, fields_name)
                items.append(row)
        return super(FTTable, self).__init__(items, *arg, **args)

