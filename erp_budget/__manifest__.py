{
	'name' : 'Gestion Budgetaire',
	'author' : 'Telia Informatique',
	'version' : "1.0",
	'depends' : ['base','referentiel'],
	'description' : 'Gestion Budgetaire',
    'summary' : "Gestion Budgetaire",
	'data' : ['security/budget_security.xml','views/budget.xml', 'views/report_budget.xml', 'security/ir.model.access.csv','data/budg_data.xml'],
	'installable' : True,
	'auto_install' : False,
}
