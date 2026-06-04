from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()
        if res is not True:
            return res

        for picking in self:
            for line in picking.move_line_ids:
                if not line.lot_id:
                    continue

                vehicle = picking._get_vehicle_from_move_line(line)
                if not vehicle:
                    continue

                if picking.picking_type_code == "incoming":
                    values = {"lot_id": line.lot_id.id}
                    if line.lot_id.name and not vehicle.vin_number:
                        values["vin_number"] = line.lot_id.name
                    if line.lot_id.vehicle_plate and not vehicle.license_plate:
                        values["license_plate"] = line.lot_id.vehicle_plate
                    vehicle.write(values)

                if picking.picking_type_code == "outgoing":
                    values = {"customer_id": picking.partner_id.id or False}
                    if line.lot_id.name and not vehicle.vin_number:
                        values["vin_number"] = line.lot_id.name
                    if line.lot_id.vehicle_plate and not vehicle.license_plate:
                        values["license_plate"] = line.lot_id.vehicle_plate
                    vehicle.write(values)
        return res
