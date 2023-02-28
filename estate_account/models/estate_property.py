from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):

        res = super().action_sold_property()
        journal = self.env["account.journal"].sudo().search([("type", "=", "sale")], limit=1)
        for property_record in self:
            print(" reached ".center(100, "="))
            self.env["account.move"].sudo().create(
                {
                    "partner_id": property_record.partner_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": property_record.name,
                                "quantity": 1,
                                "price_unit": property_record.selling_price * 6.0 / 100.0,
                            },
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1,
                                "price_unit": 100.0,
                            },
                        ),
                    ],
                }
            )

        return res
