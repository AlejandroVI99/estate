from odoo import fields, models

class EstatePropertyType(models.Model):
  _name = "estate.property.type"
  _description = "Property Type Model"

  name = fields.Char(required = True)

  _sql_constraints = [
    ("unique_type_name",
    "UNIQUE(name)",
    "Type name alredy exists")
  ]
