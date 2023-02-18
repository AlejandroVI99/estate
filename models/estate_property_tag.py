from odoo import fields, models

class EstatePropertyTag(models.Model):
  _name = "estate.property.tag"
  _description = "Property Tag Model"

  name = fields.Char(required = True)

  _sql_constraints = [
    ("unique_tag_name",
    "UNIQUE(name)",
    "Tag name alredy exists")
  ]
