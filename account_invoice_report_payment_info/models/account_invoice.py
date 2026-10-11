# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_payments_widget_reconciled_info(self):
        res = super()._compute_payments_widget_reconciled_info()
        info_pattern = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_str("account_invoice_report_payment_info.info_pattern", default="")
        )
        Move = self.env["account.move"]
        for one in self:
            if not res and not one.invoice_payments_widget:
                continue
            # Json field: reading returns a copy, so update it and reassign
            widget = one.invoice_payments_widget
            for payment_dict in widget["content"]:
                move = Move.browse(payment_dict["move_id"])
                payment_dict["move_ref"] = move.ref
                payment_dict["extra_info"] = info_pattern.format(**payment_dict)
            one.invoice_payments_widget = widget
        return res
