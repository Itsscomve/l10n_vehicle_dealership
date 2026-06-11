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

                values = None
                lot_values = {}
                if picking.picking_type_code == "incoming":
                    values = {"lot_id": line.lot_id.id}
                elif picking.picking_type_code == "outgoing":
                    values = {"customer_id": picking.partner_id.id or False}

                if values is None:
                    continue

                if line.lot_id.name and not vehicle.vin_number:
                    values["vin_number"] = line.lot_id.name
                if line.lot_id.vehicle_plate and not vehicle.license_plate:
                    values["license_plate"] = line.lot_id.vehicle_plate
                elif vehicle.license_plate and not line.lot_id.vehicle_plate:
                    lot_values["vehicle_plate"] = vehicle.license_plate

                if line.lot_id.body_serial and not vehicle.chassis_number:
                    values["chassis_number"] = line.lot_id.body_serial
                elif vehicle.chassis_number and not line.lot_id.body_serial:
                    lot_values["body_serial"] = vehicle.chassis_number

                if line.lot_id.engine_serial and not vehicle.motor_number:
                    values["motor_number"] = line.lot_id.engine_serial
                elif vehicle.motor_number and not line.lot_id.engine_serial:
                    lot_values["engine_serial"] = vehicle.motor_number

                if lot_values:
                    line.lot_id.write(lot_values)

                vehicle.write(values)
        return res
