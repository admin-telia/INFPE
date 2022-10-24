{
    "name": "Gestion des Formations et Stages des Employés",
    "version": "1.0",
    "author": "TELIA INFORMATIQUE",
    "depends":["base","Gestion_RH"],
    "data":[
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/vue_formation.xml",
        #"Report/report_attestation.xml",
        #"Report/report_employe_formation.xml",
    ],
    "category": "EPE",
    "Summary": "Gestion des Formations et Stages des Employés des EPE",
    "installable": True,
    "auto_install": False,

}
