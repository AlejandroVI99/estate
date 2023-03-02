from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):

        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)

        for property_record in self:
            self.env["account.move"].create(
                {
                    "partner_id": property_record.partner_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": property_record.name,
                                "quantity": 1,
                                "price_unit": property_record.selling_price * 6.0 / 100.0,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": "Administrative fees",
                                "quantity": 1,
                                "price_unit": 100.0,
                            },
                        ),
                    ],
                }
            )

        return super().action_sold_property()
