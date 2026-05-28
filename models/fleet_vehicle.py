from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    customer_id = fields.Many2one(
        "res.partner", string="Cliente", copy=False, tracking=True
    )
    lot_body_serial = fields.Char(
        related="lot_id.body_serial", string="Serial de la carroceria", readonly=False
    )
    lot_engine_serial = fields.Char(
        related="lot_id.engine_serial", string="Serial del motor", readonly=False
    )
    lot_vehicle_plate = fields.Char(
        related="lot_id.vehicle_plate", string="Placa del lote", readonly=False
    )
