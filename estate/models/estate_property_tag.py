from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag Model"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("color_field")

    _sql_constraints = [("unique_tag_name", "UNIQUE(name)", "Tag name alredy exists")]
