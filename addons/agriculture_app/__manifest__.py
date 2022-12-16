{
    "name": "Dolimi Agriculture",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "PIMIYA",
    "website": "https://github.com/PIMIYA/Odoo_15",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Operations/Agriculture",
    "version": "15.0.1.0.8",
    # any module necessary for this one to work correctly
    "depends": ["base", "contacts", "account", "sale", "stock"],
    # always loaded
    "data": [
        # "security/agriculture_security.xml",
        "security/ir.model.access.csv",
        "views/crop_view.xml",
        "views/crop_list_template.xml",
        "views/archived_view.xml",
        "views/archived_additional_item.xml",
        "views/member_view.xml",
        "views/member_list_template.xml",
        "views/inherit_res_partner.xml",
        "views/crop_variety_view.xml",
        "views/settings.xml",
        "views/crop_storage.xml",
        "views/crop_storage_materials.xml",
        "views/inherit_stock_picking.xml",
        "views/agriculture_menu.xml",
        "views/archived_blackcat_obt.xml",
        "report/agriculture_archived_reports.xml",
        "report/agriculture_archived_templates.xml",
        "report/agriculture_crop_reports.xml",
        "report/agriculture_crop_templatex.xml",
        "data/crop_stage_data.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "application": True,
}
