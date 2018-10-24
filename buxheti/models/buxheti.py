# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import ustr
from odoo.exceptions import UserError, ValidationError

# ---------------------------------------------------------
# Budgets
# ---------------------------------------------------------
class KategoriShpenzimi(models.Model):

    _name = "kategori.shpenzimi"
    _description = "Kategori Shpenzimi"

    name = fields.Char(string="Emri", required=True)
    info = fields.Char(string='Pershkrimi')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Kategoria eshte regjistruar me pare !"),
    ]

class Produkt(models.Model):
    _name = "produkti"
    _order = "name"
    _description = "Produkti"

    name = fields.Char(string="Emri", required=True)
    kodi = fields.Char(string="Kodi i Produktit", required=True)
    cmimi = fields.Float(string="Cmimi", required=True)
    info_produkti = fields.Char(string="Pershkrimi")
    kategori_id = fields.Many2one('kategori.shpenzimi', string="Kategoria", required=True)

    _sql_constraints = [
        ('kodi_uniq', 'unique (kodi)', "Ky produkt eshte regjistruar me pare !"),
    ]

class PlanifikimBuxheti(models.Model):
    _name = "planifikim.buxheti"
    _description = "Planifikim Buxheti"

    name = fields.Char(string="Emri", required=True)
    info_plan = fields.Char(string="Pershkrimi")
    date_fillimi = fields.Date(string="Data e fillimit")
    date_perfundimi = fields.Date(string="Data e perfundimit")
    vlere_limit = fields.Float(string="Limiti i vleres", required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Konfirmuar') ], string="Statusi", default='draft')
    planifikim_ids = fields.One2many('rreshta.planifikimi', 'planifikim_id', string=" Rreshta planifikimi")
    shpenzim_ids = fields.One2many('rreshta.shpenzimi', 'planifikim_id', string="Rreshta shpenzimi", readonly=True)
    total_planifikuar = fields.Float(string="Vlera totale e planifikuar", compute='_compute_total')
    total_realizuar = fields.Float(string="Vlera totale e realizuar", compute='_compute_total')
    diferenca = fields.Float(string="Diferenca", compute='_compute_total')

    @api.depends('planifikim_ids.vlera', 'shpenzim_ids.vlera')
    def _compute_total(self):
        for planifikim in self:
            total_plan = 0
            total_realizim = 0
            for rresht in planifikim.planifikim_ids:
                total_plan += rresht.vlera
            for rresht in planifikim.shpenzim_ids:
                total_realizim += rresht.vlera
            planifikim.total_planifikuar = total_plan
            planifikim.total_realizuar = total_realizim
            planifikim.diferenca = total_plan-total_realizim

    def confirm(self):
        self.write({'state':'confirm'})


class RreshtaPlanifikimi(models.Model):
    _name = "rreshta.planifikimi"
    _description = "Rreshta planifikimi"

    name = fields.Char(string="Emri")
    kategori_id = fields.Many2one('kategori.shpenzimi', string="Kategoria", required=True)
    planifikim_id = fields.Many2one('planifikim.buxheti', string="Planifikimi")
    vlera = fields.Float(string="Vlera", required=True)
    info_rresht = fields.Char(string="Pershkrimi")

class Shpenzimi(models.Model):
    _name = "shpenzimi"
    _description = "Shpenzimi"

    name = fields.Char(string="Emri", required=True)
    date_shpenzimi = fields.Date(string="Data e shpenzimit", required=True)
    info_shpenzimi = fields.Char(string="Pershkrimi")
    vlera_shpenzimit = fields.Float(string="Vlera e shpenzimit", required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Konfirmuar')], string="Statusi i shpenzimit")
    shpenzim_ids = fields.One2many('rreshta.shpenzimi', 'shpenzim_id', string=" Rreshta shpenzimi")

    @api.depends('shpenzim_ids.vlera')
    def _compute_total(self):
        for shpenzim in self:
            total_shpenzim = 0
            for rresht in shpenzim.shpenzim_ids:
                total_shpenzim += rresht.vlera
            shpenzim.vlera_shpenzimit = total_shpenzim

class RreshtaShpenzimi(models.Model):
    _name = "rreshta.shpenzimi"
    _description = "Rreshta shpenzimi"

    name = fields.Char(string="Emri")
    date_rreshti = fields.Date(string="Data")
    info_rreshti = fields.Char(string="Pershkrimi")
    produkt_id = fields.Many2one('produkti', string="Produkti", required=True)
    kategori_id = fields.Many2one('kategori.shpenzimi', string="Kategoria", required=True)
    planifikim_id = fields.Many2one('planifikim.buxheti', string="Planifikimi")
    shpenzim_id = fields.Many2one('shpenzimi', string="Shpenzimi", required=True)
    vlera = fields.Float(string="Vlera", required=True)


