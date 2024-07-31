from odoo import models, fields, api

class MetagraphConfig(models.Model):
    _name = 'metagraph.config'
    _description = 'Metagraph Configuration'

    name = fields.Char(string='Name', required=True)
    wallet_address = fields.Char(string='Wallet Address', required=True)
    testnet_url = fields.Char(string='TestNet URL', default='https://l0-lb-testnet.constellationnetwork.io')
    integration_url = fields.Char(string='IntegrationNet URL', default='https://l0-lb-integrationnet.constellationnetwork.io')
    mainnet_url = fields.Char(string='MainNet URL', default='https://l0-lb-mainnet.constellationnetwork.io')
    faucet_testnet_url = fields.Char(string='TestNet Faucet URL', default='https://faucet.constellationnetwork.io/testnet/faucet')
    faucet_integration_url = fields.Char(string='IntegrationNet Faucet URL', default='https://faucet.constellationnetwork.io/integrationnet/faucet')
    faucet_mainnet_url = fields.Char(string='MainNet Faucet URL', default='https://faucet.constellationnetwork.io/mainnet/faucet')
    check_status_testnet_url = fields.Char(string='TestNet Check Status URL', default='https://be-testnet.constellationnetwork.io')
    check_status_integration_url = fields.Char(string='IntegrationNet Check Status URL', default='https://be-integrationnet.constellationnetwork.io')
    check_status_mainnet_url = fields.Char(string='MainNet Check Status URL', default='https://be-mainnet.constellationnetwork.io')
    payment_testnet_url = fields.Char(string='TestNet Payment URL', default='https://payments-testnet.constellationnetwork.io')
    payment_integration_url = fields.Char(string='IntegrationNet Payment URL', default='https://payments-integrationnet.constellationnetwork.io')
    payment_mainnet_url = fields.Char(string='MainNet Payment URL', default='https://payments-mainnet.constellationnetwork.io')
    environment = fields.Selection([
        ('testnet', 'TestNet'),
        ('integration', 'IntegrationNet'),
        ('mainnet', 'MainNet')
    ], string='Environment', default='testnet')

    # Add these fields to hold the computed URLs
    base_url = fields.Char(string='Base URL', compute='_compute_urls', store=True)
    faucet_url = fields.Char(string='Faucet URL', compute='_compute_urls', store=True)
    check_status_url = fields.Char(string='Check Status URL', compute='_compute_urls', store=True)
    payment_url = fields.Char(string='Payment URL', compute='_compute_urls', store=True)

    @api.depends('environment', 'testnet_url', 'integration_url', 'mainnet_url', 'faucet_testnet_url', 'faucet_integration_url', 'faucet_mainnet_url', 'check_status_testnet_url', 'check_status_integration_url', 'check_status_mainnet_url', 'payment_testnet_url', 'payment_integration_url', 'payment_mainnet_url')
    def _compute_urls(self):
        for record in self:
            if record.environment == 'testnet':
                record.base_url = record.testnet_url
                record.faucet_url = record.faucet_testnet_url
                record.check_status_url = record.check_status_testnet_url
                record.payment_url = record.payment_testnet_url
            elif record.environment == 'integration':
                record.base_url = record.integration_url
                record.faucet_url = record.faucet_integration_url
                record.check_status_url = record.check_status_integration_url
                record.payment_url = record.payment_integration_url
            else:
                record.base_url = record.mainnet_url
                record.faucet_url = record.faucet_mainnet_url
                record.check_status_url = record.check_status_mainnet_url
                record.payment_url = record.payment_mainnet_url
