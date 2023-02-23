from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Datetime.add(fields.Date.today(), month=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation", selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type")
    user_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    property_type_id = fields.Many2one("estate.property.type")

    @api.ondelete(at_uninstall=False)
    def _check_property_state(self):
        if self.state in ("sold", "offer_received", "offer_accepted"):
            raise UserError("Property cannot be delete")

    # public methods
    def action_sold_property(self):
        if self.state != "canceled":
            self.state = "sold"
        else:
            raise UserError("Canceled properties cannot be sold")

    def action_cancel_property(self):
        if self.state != "sold":
            self.state = "canceled"
        else:
            raise UserError("Sold properties cannot be canceled")

    # private methods

    # set total area
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains("expected_price", "selling_price")
    def _selling_price(self):
        for record in self:
            condition_float_is_zero = float_is_zero(record.selling_price, precision_rounding=0.01)
            conditio_float_compare = (
                float_compare(record.selling_price, record.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            )

            if not condition_float_is_zero and conditio_float_compare:
                raise ValidationError("The selling price must be at least 90% of the expected price!")
