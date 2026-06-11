from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    body_serial = fields.Char(string="Serial de la carroceria", copy=False)
    engine_serial = fields.Char(string="Serial del motor", copy=False)
    vehicle_plate = fields.Char(string="Placa", copy=False)
    vehicle_information_ids = fields.One2many(
        "vehicle.information",
        "lot_id",
        string="Vehiculos vinculados",
        readonly=True,
    )
    vehicle_information_id = fields.Many2one(
        "vehicle.information",
        string="Vehiculo",
        compute="_compute_vehicle_trade_fields",
    )
    management_profile_id = fields.Many2one(
        "vehicle.management.profile",
        string="Perfil de gestion",
        compute="_compute_vehicle_trade_fields",
    )
    vehicle_origen_id = fields.Many2one(
        "vehicle.origen",
        string="Origen del vehiculo",
        compute="_compute_vehicle_trade_fields",
    )
    vehicle_stock_type_id = fields.Many2one(
        "vehicle.stock.type",
        string="Tipo de stock",
        compute="_compute_vehicle_trade_fields",
    )
    vehicle_type_unit_id = fields.Many2one(
        "vehicle.type.unit",
        string="Tipo de unidad",
        compute="_compute_vehicle_trade_fields",
    )

    @api.depends(
        "vehicle_information_ids",
        "vehicle_information_ids.management_profile_id",
        "vehicle_information_ids.vehicle_origen_id",
        "vehicle_information_ids.vehicle_stock_type_id",
        "vehicle_information_ids.vehicle_type_unit_id",
    )
    def _compute_vehicle_trade_fields(self):
        for lot in self:
            vehicle = lot.vehicle_information_ids[:1]
            lot.vehicle_information_id = vehicle
            lot.management_profile_id = vehicle.management_profile_id
            lot.vehicle_origen_id = vehicle.vehicle_origen_id
            lot.vehicle_stock_type_id = vehicle.vehicle_stock_type_id
            lot.vehicle_type_unit_id = vehicle.vehicle_type_unit_id
