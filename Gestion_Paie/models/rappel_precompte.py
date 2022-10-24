from odoo import fields, api, models, tools, _
from datetime import date, datetime, time
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


# heritage de la classe employee
# class HrEmployees(models.Model):
#     _inherit = "hr.employee"
#
#     x_rappel_ids = fields.One2many('payroll_rappel', 'x_employe_id', string="Rappels")
#
#     x_trop_precu_ids = fields.One2many('payroll_trop_percu', 'x_employe_id', string="Trop percu")


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def vide_rappel_percu_precompte(self):
        for val in self:
            emp_id = val.employee_id

            # rappel
            emp_id.mnt_rappel_salaire = 0
            emp_id.mnt_rappel_solde_indiciaire = 0
            emp_id.mnt_rappel_residence = 0
            emp_id.mnt_rappel_resp = 0
            emp_id.mnt_rappel_loge = 0
            emp_id.mnt_rappel_astr = 0
            emp_id.mnt_rappel_techn = 0
            emp_id.mnt_rappel_spec = 0
            emp_id.mnt_rappel_it = 0
            emp_id.mnt_rappel_ish = 0
            emp_id.mnt_rappel_allocation = 0
            emp_id.mnt_rappel_salaire_net = 0

            # trop percu
            emp_id.mnt_percu_salaire_net = 0
            emp_id.mnt_percu_salaire = 0
            emp_id.mnt_percu_solde_indiciaire = 0
            emp_id.mnt_percu_residence = 0
            emp_id.mnt_percu_resp = 0
            emp_id.mnt_percu_loge = 0
            emp_id.mnt_percu_astr = 0
            emp_id.mnt_percu_techn = 0
            emp_id.mnt_percu_spec = 0
            emp_id.mnt_percu_spec_it = 0
            emp_id.mnt_percu_spec_ish = 0
            emp_id.mnt_percu_allocation = 0
            emp_id.mnt_percu_iuts = 0

            # precompte
            emp_id.mnt_foner = 0
            emp_id.mnt_precompte_avsolde = 0
            emp_id.x_uab_vie = 0
            emp_id.x_sbe = 0
            emp_id.x_sonar_vie = 0
            emp_id.x_saham_vie = 0
            emp_id.x_sunu = 0
            emp_id.x_poste_burkina = 0
            emp_id.x_cegeci = 0
            emp_id.x_sobca = 0
            emp_id.gle_vie = 0
            emp_id.mnt_pecompte_indiciaire = 0
            emp_id.mnt_precompte_allocation = 0
            emp_id.mnt_precompte_indem_sujet = 0
            emp_id.mnt_precompte_indem_loge = 0
            emp_id.mnt_precompte_ish = 0
            emp_id.mnt_precompte_mena = 0
            emp_id.mnt_precompte_ensbase = 0
            emp_id.mnt_precompte_smess = 0
            emp_id.mnt_precompte_tech = 0
            emp_id.mnt_precompte_astr = 0
            emp_id.mnt_precompte_resp = 0
            emp_id.mnt_precompte_prestage = 0
            emp_id.mnt_precompte_salbase = 0

    def calcul_rappel(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['payroll_rappel'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    if r.x_rappel_id.code == 'mnt_rappel_salaire':
                        emp_id.mnt_rappel_salaire = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_loge':
                        emp_id.mnt_rappel_loge = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_solde_indiciaire':
                        emp_id.mnt_rappel_solde_indiciaire = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_residence':
                        emp_id.mnt_rappel_residence = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_resp':
                        emp_id.mnt_rappel_resp = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_astr':
                        emp_id.mnt_rappel_astr = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_techn':
                        emp_id.mnt_rappel_techn = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_spec':
                        emp_id.mnt_rappel_spec = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_it':
                        emp_id.mnt_rappel_it = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_ish':
                        emp_id.mnt_rappel_ish = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_allocation':
                        emp_id.mnt_rappel_allocation = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_salaire_net':
                        emp_id.mnt_rappel_salaire_net = r.mnt_rappel

    def set_valide_rappel(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['payroll_rappel'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    r.state = 'P'
                    r.fiche_paie_id = val.id

    def calcul_trop_percu(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['payroll_trop_percu'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))
            print(result)
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    if r.x_rappel_id.code == 'mnt_percu_salaire_net':
                        emp_id.mnt_percu_salaire_net = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_percu_iuts':
                        emp_id.mnt_percu_iuts = r.mnt_rappel

    def set_valide_trop_percu(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['payroll_trop_percu'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    r.state = 'P'
                    r.fiche_paie_id = val.id

    def calcul_precompte(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['hr_paie_precompte'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))

            for r in result:
                if r.montant_reste >= r.montant_echeance:
                    montant = r.montant_echeance
                else:
                    montant = r.montant_reste

                if r.x_precompte_id.code == 'mnt_foner':
                    emp_id.mnt_foner += montant
                elif r.x_precompte_id.code == 'mnt_precompte_avsolde':
                    emp_id.mnt_precompte_avsolde += montant
                elif r.x_precompte_id.code == 'x_uab_vie':
                    emp_id.x_uab_vie += montant
                elif r.x_precompte_id.code == 'x_sbe':
                    emp_id.x_sbe += montant
                elif r.x_precompte_id.code == 'x_sonar_vie':
                    emp_id.x_sonar_vie += montant
                elif r.x_precompte_id.code == 'x_saham_vie':
                    emp_id.x_saham_vie += montant
                elif r.x_precompte_id.code == 'x_sunu':
                    emp_id.x_sunu += montant
                elif r.x_precompte_id.code == 'x_poste_burkina':
                    emp_id.x_poste_burkina += montant
                elif r.x_precompte_id.code == 'x_cegeci':
                    emp_id.x_cegeci += montant
                elif r.x_precompte_id.code == 'x_sobca':
                    emp_id.x_sobca += montant
                elif r.x_precompte_id.code == 'gle_vie':
                    emp_id.gle_vie += montant
                elif r.x_precompte_id.code == 'mnt_pecompte_indiciaire':
                    emp_id.mnt_pecompte_indiciaire += montant
                elif r.x_precompte_id.code == 'mnt_precompte_allocation':
                    emp_id.mnt_precompte_allocation += montant
                elif r.x_precompte_id.code == 'mnt_precompte_indem_sujet':
                    emp_id.mnt_precompte_indem_sujet += montant
                elif r.x_precompte_id.code == 'mnt_precompte_indem_loge':
                    emp_id.mnt_precompte_indem_loge += montant
                elif r.x_precompte_id.code == 'mnt_precompte_ish':
                    emp_id.mnt_precompte_ish += montant
                elif r.x_precompte_id.code == 'mnt_precompte_mena':
                    emp_id.mnt_precompte_mena += montant
                elif r.x_precompte_id.code == 'mnt_precompte_ensbase':
                    emp_id.mnt_precompte_ensbase += montant
                elif r.x_precompte_id.code == 'mnt_precompte_smess':
                    emp_id.mnt_precompte_smess += montant
                elif r.x_precompte_id.code == 'mnt_precompte_tech':
                    emp_id.mnt_precompte_tech += montant
                elif r.x_precompte_id.code == 'mnt_precompte_astr':
                    emp_id.mnt_precompte_astr += montant
                elif r.x_precompte_id.code == 'mnt_precompte_resp':
                    emp_id.mnt_precompte_resp += montant
                elif r.x_precompte_id.code == 'mnt_precompte_prestage':
                    emp_id.mnt_precompte_prestage += montant
                elif r.x_precompte_id.code == 'mnt_precompte_salbase':
                    emp_id.mnt_precompte_salbase += montant

    def set_valide_precompte(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['hr_paie_precompte'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))

            for r in result:
                if r.montant_reste >= r.montant_echeance:
                    montant = r.montant_echeance
                else:
                    montant = r.montant_reste
                self.env['hr_paie_precompte_line'].create({
                    'montant': montant,
                    'payslip_id': val.id,
                    'state': 'P',
                    'x_date_debut': val.date_from,
                    'x_date_fin': val.date_to,
                    'precompte_id': r.id})

                if r.montant_paye == r.montant:
                    r.state = 'P'

    @api.multi
    def compute_sheet(self):
        for val in self:
            val.vide_rappel_percu_precompte()
            val.calcul_rappel()
            val.calcul_trop_percu()
            val.calcul_precompte()
        return super(HrPayslip, self).compute_sheet()

    def action_payslip_done(self):
        for val in self:
            emp_id = val.employee_id
            result = self.env['hr.payslip'].search([
                ('employee_id', '=', emp_id.id),
                ('state', '=', "done"), ])

            mois_courant = val.date_from.month
            annee_courant = val.date_from.year
            for r in result:
                mois = r.date_from.month
                annee = r.date_from.year
                if mois_courant == mois and annee_courant == annee:
                    raise ValidationError(
                        _("Le bulletin de ce mois a été déjà génére et validé"))

            val.compute_sheet()

            val.set_valide_rappel()
            val.set_valide_trop_percu()
            val.set_valide_precompte()

            val.vide_rappel_percu_precompte()
        return super(HrPayslip, self).action_payslip_done()

# rappel
class PayrollRappel(models.Model):
    _name = "payroll_rappel"
    _rec_name = 'x_employe_id'
    _order = 'date'

    x_employe_id = fields.Many2one('hr.employee', string='Employé', required=True)
    x_rappel_id = fields.Many2one('hr_rappel_element', string='Elément', required=True)
    date = fields.Date(string='Période', required=True)
    date_to = fields.Date(string='Date', required=False)
    date_effet = fields.Date(string='Date effet', required=True)
    date_dernier = fields.Date(string='Date fin', required=True)
    date_validation = fields.Date(string='Date validation', required=False)
    raison = fields.Char('Motif', required=False)
    motif_ann_paie = fields.Char('Motif annulation', required=False)
    mnt_avant = fields.Float(string='Mont. perçu', required=True, default=0)
    mnt_apres = fields.Float(string='Mont. aurait dû', required=True, default=0)
    occurence = fields.Integer(string='Durée (jours)', required=False,  compute="on_cal_occurence")
    mnt_rappel = fields.Float(string='Montant rappel', required=True, default=0, compute="on_calcul_mtn")
    fiche_paie_id = fields.Many2one('hr.payslip', string='Fiche de paie', required=False)
    is_paye = fields.Boolean(string="Payé ?", default=False)

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('A', 'Annulé'),
        ('P', 'Soldé'),
    ], 'Etat', default='draft', index=True, required=True)

    @api.onchange("date", "date_to")
    def pres(self):
        for val in self:
            if val.date and val.date_to:
                if val.date >= val.date_to:
                    raise ValidationError(_("La date de fin doit être superieur à la date de début"))

    def set_valider(self):
        for val in self:
            result = val.env['payroll_rappel'].search((
                ('x_employe_id', '=', val.x_employe_id.id),
                ('state', 'in', ('V', 'P')),
                ('x_rappel_id', '=', val.x_rappel_id.id),
            ))
            for r in result:
                mois_courant = val.date.month
                annee_courant = val.date.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    raise ValidationError(_("Vous avez déja enregistré un rappel pour cet élément dans cette période"))

            val.state = 'V'
            val.date_validation = date.today()

    def set_annuler(self):
        for val in self:
            if not val.motif_ann_paie:
                raise ValidationError(
                    _("Veuillez remplir le champ motif annulation"))

            val.state = 'A'

    @api.depends("date_dernier", "date_effet")
    def on_cal_occurence(self):
        for rec in self:
            rec.occurence = 0
            if rec.date_dernier and rec.date_effet:
                rec.occurence = (rec.date_dernier - rec.date_effet).days + 1

    @api.depends("mnt_apres", "mnt_avant", "occurence")
    def on_calcul_mtn(self):
        for rec in self:
            rec.mnt_rappel = round(((rec.mnt_apres - rec.mnt_avant)/30) * rec.occurence)


class HrRappelElement(models.Model):
    _name = "hr_rappel_element"
    _rec_name = 'libelle'

    code = fields.Char('Code', required=True)
    libelle = fields.Char('Libellé', required=True)

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

# trop percu
class PayrollTropPercu(models.Model):
    _name = "payroll_trop_percu"
    _rec_name = 'x_employe_id'
    _order = 'date'

    x_employe_id = fields.Many2one('hr.employee', string='Employé', required=True)
    x_rappel_id = fields.Many2one('hr_rappel_trop_percu_element', string='Elément', required=True)
    date = fields.Date(string='Date', required=True)
    date_to = fields.Date(string='Date', required=True)
    date_effet = fields.Date(string='Date effet', required=True)
    date_dernier = fields.Date(string='Date fin', required=True)
    date_validation = fields.Date(string='Date validation', required=False)
    raison = fields.Char('Motif', required=False)
    motif_ann_paie = fields.Char('Motif annulation', required=False)
    mnt_avant = fields.Float(string='Mont. perçu', required=True, default=0)
    mnt_apres = fields.Float(string='Mont. aurait dû', required=True, default=0)
    occurence = fields.Integer(string='Durée (jours)', required=False, compute="on_cal_occurence")
    mnt_rappel = fields.Float(string='Montant trop perçu', required=True, default=0, compute="on_calcul_mtn")
    fiche_paie_id = fields.Many2one('hr.payslip', string='Fiche de paie', required=False)
    is_paye = fields.Boolean(string="Payé ?", default=False)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('A', 'Annulé'),
        ('P', 'Soldé'),
    ], 'Etat', default='draft', index=True, required=True)

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

    @api.onchange("date", "date_to")
    def pres(self):
        for val in self:
            if val.date and val.date_to:
                if val.date >= val.date_to:
                    raise ValidationError(_("La date de fin doit être superieur à la date de début"))

    def set_valider(self):
        for val in self:
            result = val.env['payroll_trop_percu'].search((
                ('x_employe_id', '=', val.x_employe_id.id),
                ('state', 'in', ('V', 'P')),
                ('x_rappel_id', '=', val.x_rappel_id.id),
            ))
            for r in result:
                mois_courant = val.date.month
                annee_courant = val.date.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    raise ValidationError(
                        _("Vous avez déja enregistré un trop perçu pour cet élément dans cette période"))

            val.state = 'V'
            val.date_validation = date.today()

    def set_annuler(self):
        for val in self:
            if not val.motif_ann_paie:
                raise ValidationError(
                    _("Veuillez remplir le champ motif annulation"))

            val.state = 'A'

    @api.depends("date_dernier", "date_effet")
    def on_cal_occurence(self):
        for rec in self:
            rec.occurence = 0
            if rec.date_dernier and rec.date_effet:
                rec.occurence = (rec.date_dernier - rec.date_effet).days + 1

    @api.depends("mnt_apres", "mnt_avant", "occurence")
    def on_calcul_mtn(self):
        for rec in self:
            rec.mnt_rappel = round(((rec.mnt_avant - rec.mnt_apres)/30) * rec.occurence)


class HrTropPercuElement(models.Model):
    _name = "hr_rappel_trop_percu_element"
    _rec_name = 'libelle'

    code = fields.Char('Code', required=True)
    libelle = fields.Char('Libellé', required=True)

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)


# Precompte#
class HrPaiePrecompte(models.Model):
    _name = "hr_paie_precompte"

    name = fields.Char(string="N°", default="/", readonly=True)
    x_employe_id = fields.Many2one('hr.employee', string='Agent', required=True)
    x_precompte_id = fields.Many2one('hr_paie_precompte_element', string='Element', required=True)
    reference = fields.Char('Reference', required=False)

    montant = fields.Float(string="Montant initial", required=True, help="Montant du prêt")
    montant_echeance = fields.Float(string="Ret. Mens.", required=True, help="Montant du prêt")
    nbr_echeance = fields.Integer(string="Nombre d'échéance", default=1, compute="calcul_echeance",
                                  )
    date_deb = fields.Date(string="Date début paiement", required=True, default=fields.Date.today(), )

    lines_ids = fields.One2many('hr_paie_precompte_line', 'precompte_id', string="Lignes", index=True)

    date_validation = fields.Date(string='Date validation', required=False)
    raison = fields.Char('Motif', required=False, default="-")
    motif_ann_paie = fields.Char('Motif annulation/paiement', required=False)
    fiche_paie_id = fields.Many2one('hr.payslip', string='Fiche de paie', required=False)
    is_paye = fields.Boolean(string="Payé ?", default=False)

    montant_paye = fields.Float(string="Mt. Remb.", required=True, compute="calcul_montant_paye")
    montant_reste = fields.Float(string="Reste", required=True, compute="calcul_montant_reste")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('S', 'Suspendu'),
        ('A', 'Annulé'),
        ('P', 'Soldé'),
    ], 'Etat', default='draft', index=True, required=True, store=True)

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

    def set_valider(self):
        for val in self:
            if val.name == '/':
                val.name = self.env['ir.sequence'].next_by_code('etat.hr.precompte.code') or '/'
            val.state = 'V'
            val.date_validation = date.today()

    def set_annuler(self):
        for val in self:
            if not val.motif_ann_paie:
                raise ValidationError(
                    _("Veuillez remplir le champ motif annulation/paiement"))

            val.state = 'A'

    def set_suspendre(self):
        for val in self:
            val.state = 'S'

    def set_reprendre(self):
        for val in self:
            val.state = 'V'
            
    def set_payer(self):
        for val in self:
            if not val.motif_ann_paie:
                raise ValidationError(
                    _("Veuillez remplir le champ motif annulation/paiement"))

            val.state = 'P'

    @api.constrains('montant')
    def _check_montant(self):
        for val in self:
            if val.montant_paye > val.montant:
                raise ValidationError(_("Le montant total ne peut pas être inferieur au montant payé."))

    @api.constrains('montant', 'montant_echeance')
    def _check_montant_echeance(self):
        for val in self:
            if val.montant_echeance > val.montant_reste:
                raise ValidationError(_("Le montant de l'échéance ne peut pas être supérieur au montant restant à payé."))

    @api.depends('lines_ids')
    def calcul_montant_paye(self):
        for val in self:
            print(val.state)
            montant_paye = 0
            for l in val.lines_ids:
                if l.state == 'P':
                    montant_paye = montant_paye + l.montant

            val.montant_paye = montant_paye

            # print("Maxxx")
            # if val.state != 'P':
            #     if val.montant_paye and val.montant and val.montant_paye == val.montant:
            #         print("okk")
            #         val.state = 'P'
            #         print(val.state)

            # if val.montant_paye == val.montant:
            #     val.state = 'P'

    @api.depends('montant', 'montant_paye')
    def calcul_montant_reste(self):
        for val in self:
            val.montant_reste = val.montant - val.montant_paye

    @api.depends('montant', 'montant_echeance')
    def calcul_echeance(self):
        for val in self:
            val.nbr_echeance = 0
            if val.montant_echeance:
                val.nbr_echeance = int(val.montant / val.montant_echeance)

    def _inverse_calcul_echeance(self):
        for val in self:
            print("Maxx")
            if val.nbr_echeance:
                val.montant_echeance = round(val.montant / val.nbr_echeance)

    def calcul_ta(self):
        for val in self:
            val.lines_ids.unlink()
            date_start = datetime.strptime(str(val.date_deb), '%Y-%m-%d')
            for i in range(1, val.nbr_echeance):
                self.env['hr_paie_precompte_line'].create({
                    'date': date_start,
                    'montant': val.montant_echeance,
                    'precompte_id': val.id})
                date_start = date_start + relativedelta(months=1)

            montant_echeance = val.montant - (val.montant_echeance * (val.nbr_echeance - 1))
            self.env['hr_paie_precompte_line'].create({
                'date': date_start,
                'montant': montant_echeance,
                'precompte_id': val.id})

        return True



class HrPaiePrecompteElement(models.Model):
    _name = "hr_paie_precompte_element"
    _rec_name = 'libelle'

    code = fields.Char('Code', required=True)
    libelle = fields.Char('Libellé', required=True)

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)


class HrPretLine(models.Model):
    _name = "hr_paie_precompte_line"
    _description = "Installment Line"

    date = fields.Date(string="Date", required=False, )
    montant = fields.Float(string="Montant", required=True)
    is_paye = fields.Boolean(string="Payé", help="Paid")
    precompte_id = fields.Many2one('hr_paie_precompte', string="Précompte")
    payslip_id = fields.Many2one('hr.payslip', string="Fiche de paie", help="Payslip")
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('A', 'Annulé'),
        ('P', 'Payé'),
    ], 'Etat', default='P', index=True, required=True)
