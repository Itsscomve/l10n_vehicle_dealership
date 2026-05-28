from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()
        if self.picking_type_code == "outgoing":
            for ml in self.move_line_ids:
                if ml.lot_id:
                    v = self.env["fleet.vehicle"].search(
                        [("lot_id", "=", ml.lot_id.id)], limit=1
                    )
                    if v:
                        values = {"customer_id": self.partner_id.id or False}
                        if ml.lot_id.name and not v.vin_sn:
                            values["vin_sn"] = ml.lot_id.name
                        if ml.lot_id.vehicle_plate and not v.license_plate:
                            values["license_plate"] = ml.lot_id.vehicle_plate
                        v.write(values)
        return res
