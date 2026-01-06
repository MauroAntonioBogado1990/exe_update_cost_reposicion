# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def actualizar_costo_contable(self):
        productos = self.search([('standard_price', '>', 0)])
        for producto in productos:
            if producto.cost_method == 'standard':
                producto.standard_price = producto.replacement_cost