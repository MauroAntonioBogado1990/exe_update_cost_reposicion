# -*- coding: utf-8 -*-
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def actualizar_costo_contable(self):
        """
        Actualiza el standard_price (Costo) basándose en el replenishment_cost (Reposición)
        solo para productos con método de costo 'Estándar'.
        """
        # 1. Búsqueda optimizada
        # Filtramos directamente en la base de datos para traer solo lo necesario:
        # - Productos cuyo método de costo (en la categoría) sea 'standard'
        # - Productos que tengan un costo de reposición mayor a 0 (para evitar errores)
        productos = self.search([
            ('categ_id.property_cost_method', '=', 'standard'),
            ('replenishment_cost', '>', 0)
        ])

        # 2. Iteración y actualización
        count = 0
        for producto in productos:
            # Comparamos para evitar escribir si el valor ya es el mismo
            # (Ahorra recursos y logs en el chatter)
            if producto.standard_price != producto.replenishment_cost:
                producto.standard_price = producto.replenishment_cost
                count += 1
        
        # Opcional: Log en la consola del servidor para verificar que corrió
        _logger.info(f"Cron ejecutado: {count} productos actualizados.")