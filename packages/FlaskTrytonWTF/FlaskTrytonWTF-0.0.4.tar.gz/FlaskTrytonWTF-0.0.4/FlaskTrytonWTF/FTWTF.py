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
#
from flask_admin.form import DatePickerWidget, DateTimePickerWidget
from flask_wtf import FlaskForm
import wtforms as fields
import wtforms.validators as validator
from .convetion import WTF_TRYTON_FIELD_MAPPING
from .convetion import WTF_TRYTON_FIELD_ATTRIBUTES_MAPPING
from .convetion import WTF_TRYTON_FIELD_ATTRIBUTES_SPECIFIC


class TFlaskForm(FlaskForm):
    trytonObject = None
    tryton_fields = {}
    """
    tryton_fields must be a dictionary like oject field 
    """
    submitLable = "Submit"
    
    def __init__(self, *arg, **kargs):
        self._trytonId = None
        self.GetWtfFromTryton()
        self._unbound_fields.append(('submit', fields.SubmitField(self.submitLable)))
        super(TFlaskForm, self).__init__(*arg, **kargs)

    def GetWtfFromTryton(self):
        """
        Get a brand new FlaskForm created from tryton module
        """
        allTrytonFields = self.trytonObject._fields.keys()
        values = self.trytonObject.default_get(self.tryton_fields)
        if not self.tryton_fields:
            tryton_fields = allTrytonFields
        else:
            tryton_fields = self.tryton_fields
        for tryton_field_name in tryton_fields :
            
            if tryton_fields and tryton_field_name not in allTrytonFields:
                continue  
            field = self.trytonObject._fields.get(tryton_field_name)
            wtField = WTF_TRYTON_FIELD_MAPPING.get(field._type)
            if wtField:
                wtFielAttibutes = {}
                attribute_to_compute = {}
                attribute_to_compute.update(WTF_TRYTON_FIELD_ATTRIBUTES_MAPPING)
                attribute_to_compute.update(WTF_TRYTON_FIELD_ATTRIBUTES_SPECIFIC.get(field._type, {}))
                for trytonFieldAttribure, WTFFieldAttribute in attribute_to_compute.items():
                    if trytonFieldAttribure=='select':
                        wtFielAttibutes[WTFFieldAttribute] = field.selection
                    else:
                        wtFielAttibutes[WTFFieldAttribute] = getattr(field, trytonFieldAttribure)

                if 'label' not in wtFielAttibutes:
                    wtFielAttibutes['label'] = tryton_field_name
                wtFielAttibutes['default'] = values.get(tryton_field_name)
                wtFielAttibutes.update(tryton_fields.get(tryton_field_name, {}))
                if field._type == 'datetime':
                    wtFielAttibutes['widget'] = DateTimePickerWidget()
                if field._type == 'date':
                    wtFielAttibutes['widget'] = DatePickerWidget()
                if field.required:
                    validators = wtFielAttibutes.get('validators',[])
                    validators.append(validator.DataRequired())
                    wtFielAttibutes['validators']=validators
                self._unbound_fields.append((tryton_field_name, wtField(**wtFielAttibutes)))
            else:
                raise NotImplementedError("Widget for filed %r not implemented" % tryton_field_name)

    def trytonSubmit(self):
        create_vals = {}
        for field_name in self.tryton_fields.keys():
            if field_name in self:
                create_vals[field_name] = self.__getitem__(field_name).data
        self._trytonId = self.trytonObject.create([create_vals])
        return create_vals
        
        
             