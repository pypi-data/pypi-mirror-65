# -*- coding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, ERP-PLM-CAD Open Source Solution
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
Created on 30 Mar 2020

@author: mboscolo
'''
import wtforms.fields.html5 as fields5
import wtforms as fields
import wtforms.validators as validator
import flask_table as ft


WTF_FIELDS_ATTRIBUTES = ['label',       #– The label of the field.
                         'validators',  # – A sequence of validators to call when validate is called.
                         'filters',     # – A sequence of filters which are run on input data by process.
                         'description', # – A description for the field, typically used for help text.
                         'id',          # – An id to use for the field. A reasonable default is set by the form, and you shouldn’t need to set this manually.
                         'default',     # – The default value to assign to the field, if no form or object input is provided. May be a callable.
                         'widget',      # – If provided, overrides the widget used to render the field.
                         'render_kw',   # (dict) – If provided, a dictionary which provides default keywords that will be given to the widget at render time.
                         '_form',       # – The form holding this field. It is passed by the form itself during construction. You should never pass this value yourself.
                         '_name',       # – The name of this field, passed by the enclosing form during its construction. You should never pass this value yourself.
                         '_prefix',     # – The prefix to prepend to the form name of this field, passed by the enclosing form during construction.
                         '_translations', # – A translations object providing message translations. Usually passed by the enclosing form during construction. See I18n docs for information on message translations.
                         '_meta',       #– – If provided, this is the ‘meta’ instance from the form. You usually don’t pass this yourself.
]

WTF_TRYTON_FIELD_ATTRIBUTES_MAPPING = {'name': 'id',
                                       #'loading': '',
                                       #'context': '',
                                       #'depends': '',
                                       #'on_change_with': '',
                                       #'on_change': '',
                                       #'select': 'choices',
                                       #'states': '',
                                       #'domain': '',
                                       #'readonly': '',
                                       #'required': '',
                                       'help': 'description',
                                       'string':'label'}

WTF_TRYTON_FIELD_ATTRIBUTES_SPECIFIC = {'selection': {'select': 'choices'}}

WTF_TRYTON_FIELD_MAPPING = {'boolean': fields.BooleanField,
                            'integer':fields.IntegerField,
                            'biginteger':fields.IntegerField,
                            'char': fields.StringField,
                            'text': fields.TextAreaField,
                            'float':fields.FloatField,
                            'numeric': fields.DecimalField,
                            'date': fields.DateField,
                            'datetime': fields.DateTimeField,
                            #'timestamp':fields. ,
                            #'time'
                            #'timedelta'
                            'binary': fields.FileField,
                            'selection': fields.SelectField,
                            #'multiselection'
                            #'reference'
                            #'many2one':fields.FormField
                            #'one2many':fields.FormField
                            #'many2many':fields.FormField
                            #'one2one':fields.FormField
                            #function
                            #multivalue
                            #dict
                            }


FT_TRYTON_FIELD_ATTRIBUTE_MAPPING = {
                    'integer': ft.Col,
                    'char': ft.Col,
                    'text': ft.Col,
                    'selection': ft.Col,
                    'biginteger': ft.Col,
                    'optcol': ft.OptCol,           # Converts values according to a dictionary of choices. Eg for turning stored codes into human readable text.
                    'boolean': ft.BoolNaCol,    # BoolNaCol (subclass of BoolCol) - converts values to yes/no/na
                    'date': ft.DateCol,         # For dates (uses format_date from babel.dates).
                    'datetime': ft.DatetimeCol, # For date-times (uses format_datetime from babel.dates).
                    'link':ft.LinkCol,             # Creates a link by specifying an endpoint and url_kwargs.
                    'button': ft.ButtonCol,     # (subclass of LinkCol) creates a button that posts the the given address.
                    'many2many': ft.NestedTableCol # Allows nesting of tables inside columns
                    }
