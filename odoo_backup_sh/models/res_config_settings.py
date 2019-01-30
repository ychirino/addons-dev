# Copyright 2018 Stanislav Krotov <https://it-projects.info/team/ufaks>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    encrypt_backups = fields.Boolean(string="Encrypt Backups")
    encryption_password = fields.Char(string='Encryption Password')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update({
            'encrypt_backups': self.env['ir.config_parameter'].get_param(
                'odoo_backup_sh.encrypt_backups', 'False').lower() == 'true',
            'encryption_password': self.env['odoo_backup_sh.odoo_tools_config'].get_values(
                'options', ['odoo_backup_encryption_password'])['odoo_backup_encryption_password']
        })
        return res

    @api.multi
    def set_values(self):
        # we store the repr of the value, since the value of the parameter is a required string
        self.env['ir.config_parameter'].set_param('odoo_backup_sh.encrypt_backups', repr(self.encrypt_backups))
        self.env['odoo_backup_sh.odoo_tools_config'].set_values(
            'options', {'odoo_backup_encryption_password': (self.encryption_password or '').strip()})
        super(ResConfigSettings, self).set_values()