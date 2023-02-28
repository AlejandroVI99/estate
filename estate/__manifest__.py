{
    "name": "Real Estate",
    "category": "Real Estate/Brokerage",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/estate_security.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_view.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
