# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.easy_my_coop_website.controllers.main import WebsiteSubscription


class WebsiteSubscription(WebsiteSubscription):


    def fill_values(self, values, is_company, logged, load_from_user=False):
        values = super(WebsiteSubscription, self).fill_values(values, is_company, logged, load_from_user=False)
        sub_req_obj = request.env['subscription.request']
        fields_desc = sub_req_obj.sudo().fields_get(['join_commission', 'discovery_channel'])
        company = request.env['res.company']._company_default_get()
        values.update({
            'commissions': fields_desc['join_commission']['selection'],
            'channels': fields_desc['discovery_channel']['selection'],
            'display_sepa': company.display_sepa_approval,
            'sepa_required': company.sepa_approval_required,
            'sepa_text': company.sepa_approval_text
        })
        return values
