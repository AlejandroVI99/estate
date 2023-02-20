from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError

class EstatePropertyOffer(models.Model):
  _name = "estate.property.offer"
  _description = "Property Offer Model"
  _order = "price desc"

  price = fields.Float()
  status = fields.Selection(
    copy = False,
    selection = [("accepted", "Accepted"), ("refused","Refused")]
  )
  partner_id = fields.Many2one("res.partner", string = "Buyer", required = True)
  property_id = fields.Many2one("estate.property", required = True)
  validity = fields.Integer(default = 7)
  date_deadline = fields.Date(
    compute = "_compute_date_deadline",
    inverse = "_inverse_date_deadline"
  )
  property_type_id = fields.Many2one("estate.property.type")\

  _sql_constraints = [
    ("property_offer_price",
    "CHECK(price > 0)",
    "Tag name alredy exists")
  ]

  #public methods
  def action_accept_offer(self):
    if self.property_id.partner_id.id == False:
      self.status = "accepted"
      self.property_id.partner_id = self.partner_id.id
      self.property_id.selling_price = self.price
      self.property_id.state = "offer_accepted"
    else:
      raise UserError("Property has already a Buyer")

  def action_refuse_offer(self):
    self.status = "refused"

  #private methods
  @api.depends("validity")
  def _compute_date_deadline(self):
    for record in self:
      if record.create_date:
        record.date_deadline = record.create_date.date() + relativedelta(days = record.validity)
      else:
        record.date_deadline = fields.Date.today() + relativedelta(days = record.validity)

  def _inverse_date_deadline(self):
    for record in self:
      if record.create_date:
        record.validity = (record.date_deadline - record.create_date.date()).days
      else:
        record.validity = (record.date_deadline - fields.Date.today()).days
