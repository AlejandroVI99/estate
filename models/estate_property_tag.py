from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag Model"

    name = fields.Char(required=True)
