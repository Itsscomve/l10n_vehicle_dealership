from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    body_serial = fields.Char(string="Serial de la carroceria", copy=False)
    engine_serial = fields.Char(string="Serial del motor", copy=False)
    vehicle_plate = fields.Char(string="Placa", copy=False)
