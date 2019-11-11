import pandas as pd
import xml.etree.ElementTree as ET
import io
import os
import glob
import csv
import chardet

def parse_generate():

	filename = "trame.csv"
	if not os.path.exists(filename):
		print("File does not exists")
		return

	# XML
	# create the file structure
	lheo = ET.Element('lheo')
	lheo.attrib['xmlns'] = 'http://www.lheo.org/2.2'

	file_encoding = 'UTF-8'
	sep = ','
	with open(r'trame.csv', 'rb') as f:
		result = chardet.detect(f.read()) # or readline if the file is large
		file_encoding = result['encoding']
		if file_encoding.lower() != "utf-8":
			sep = ';'

	print("Encoding is ", file_encoding)
	engine = 'c' #c or python

	# Read in the data
	# ISO-8859-1
	# unicode
	# utf-16
	# utf-8
	# cp1252
	# utf-8-sig
	# latin1
	data = pd.read_csv(filename, engine=engine, encoding=file_encoding, quoting=csv.QUOTE_NONE, error_bad_lines=False, sep=sep)

	for index, row in data.iterrows():
		print("File generation...")

		offres = ET.SubElement(lheo,'offres')

		formation = ET.SubElement(offres,'formation')
		formation.attrib['numero'] = str(row['numero'])
		formation.attrib['datemaj'] = str(row['datemaj'])
		formation.attrib['datecrea'] = str(row['datecrea'])

		intitule_formation = ET.SubElement(formation,'intitule-formation')
		intitule_formation.text = str(row['intitule-formation'])

		objectif_formation = ET.SubElement(formation,'objectif-formation')
		objectif_formation.text = str(row['objectif-formation'])

		resultats_attendus = ET.SubElement(formation,'resultats-attendus')
		resultats_attendus.text = str(row['resultats-attendus'])

		contenu_formation = ET.SubElement(formation,'contenu-formation')
		contenu_formation.text = str(row['contenu-formation'])

		parcours_de_formation = ET.SubElement(formation,'parcours-de-formation')
		parcours_de_formation.text = str(row['parcours-de-formation'])

		objectif_general_formation = ET.SubElement(formation,'objectif-general-formation')
		objectif_general_formation.text = str(row['objectif-general-formation'])

		certification = ET.SubElement(formation,'certification')
		code_CERTIFINFO = ET.SubElement(certification,'code-CERTIFINFO')
		code_CERTIFINFO.text = str(row['code-CERTIFINFO'])

		# Action
		action = ET.SubElement(formation,'action')
		action.attrib['numero'] = str(row['action-numero'])
		action.attrib['datemaj'] = str(row['action-datemaj'])
		action.attrib['datecrea'] = str(row['action-datecrea'])

		rythme_formation = ET.SubElement(action,'rythme-formation')
		rythme_formation.text = str(row['rythme-formation'])

		niveau_entree_obligatoire = ET.SubElement(action,'niveau-entree-obligatoire')
		niveau_entree_obligatoire.text = str(row['niveau-entree-obligatoire'])

		modalites_enseignement = ET.SubElement(action,'modalites-enseignement')
		modalites_enseignement.text = str(row['modalites-enseignement'])

		conditions_specifiques = ET.SubElement(action,'conditions-specifiques')
		conditions_specifiques.text = str(row['conditions-specifiques'])
		
		lieu_de_formation = ET.SubElement(action,'lieu-de-formation')
		coordonnees = ET.SubElement(lieu_de_formation,'coordonnees')
		coordonnees.attrib['numero'] = str(row['lieu-de-formation-coordonnees-numero'])

		nom = ET.SubElement(coordonnees,'nom')
		nom.text = str(row['lieu-de-formation-coordonnees-nom'])

		prenom = ET.SubElement(coordonnees,'prenom')
		prenom.text = str(row['lieu-de-formation-coordonnees-prenom'])

		adresse = ET.SubElement(coordonnees,'adresse')
		adresse.attrib['numero'] = str(row['lieu-de-formation-adresse-numero'])

		ligne = ET.SubElement(adresse,'ligne')
		ligne.text = str(row['lieu-de-formation-adresse-numero'])+str(row['lieu-de-formation-adresse-ligne'])

		codepostal = ET.SubElement(adresse,'codepostal')
		codepostal.text = str(row['lieu-de-formation-adresse-codepostal'])

		ville = ET.SubElement(adresse,'ville')
		ville.text = str(row['lieu-de-formation-adresse-ville'])

		telfixe = ET.SubElement(coordonnees,'telfixe')
		numtel = ET.SubElement(telfixe,'numtel')
		numtel.text = str(row['lieu-de-formation-numtel'])

		courriel = ET.SubElement(coordonnees,'courriel')
		courriel.text = str(row['lieu-de-formation-courriel'])
		
		modalites_entrees_sorties = ET.SubElement(action,'modalites-entrees-sorties')
		modalites_entrees_sorties.text = str(row['modalites-entrees-sorties'])
		
		url_action = ET.SubElement(action,'url-action')
		urlweb = ET.SubElement(url_action,'urlweb')
		urlweb.text = str(row['urlweb'])
		
		session = ET.SubElement(action,'session')
		session.attrib['numero'] = str(row['session-numero'])
		session.attrib['datemaj'] = str(row['session-datemaj'])
		session.attrib['datecrea'] = str(row['session-datecrea'])

		periode = ET.SubElement(session,'periode')
		debut = ET.SubElement(periode,'debut')
		fin = ET.SubElement(periode,'fin')
		debut.text = str(row['debut'])
		fin.text = str(row['fin'])

		adresse_inscription = ET.SubElement(session,'adresse-inscription')
		adresse = ET.SubElement(adresse_inscription,'adresse')
		adresse.attrib['numero'] = str(row['session-adresse-numero'])
		ligne = ET.SubElement(adresse,'ligne')
		ligne.text = str(row['session-adresse-numero'])+str(row['session-adresse-ligne'])
		codepostal = ET.SubElement(adresse,'codepostal')
		codepostal.text = str(row['session-adresse-codepostal'])
		ville = ET.SubElement(adresse,'ville')
		ville.text = str(row['session-adresse-ville'])

		etat_recrutement = ET.SubElement(session,'etat-recrutement')
		etat_recrutement.text = str(row['etat-recrutement'])

		# Extras
		extras = ET.SubElement(session,'extras')
		extras.attrib['info'] = 'session'
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'contact-inscription'
		coordonnees = ET.SubElement(extra,'coordonnees')
		coordonnees.attrib['numero'] = str(row['session-extra-coordonnees-numero'])
		nom = ET.SubElement(coordonnees,'nom')
		nom.text = str(row['session-extra-coordonnees-nom'])
		prenom = ET.SubElement(coordonnees,'prenom')
		prenom.text = str(row['session-extra-coordonnees-prenom'])
		telfixe = ET.SubElement(coordonnees,'telfixe')
		numtel = ET.SubElement(telfixe,'numtel')
		numtel.text = str(row['session-extra-numtel'])
		courriel = ET.SubElement(coordonnees,'courriel')
		courriel.text = str(row['session-extra-courriel'])
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'garantie'
		extra.text = str(row['session-extra-garantie'])

		# Adresse Info
		adresse_information = ET.SubElement(action,'adresse-information')
		adresse = ET.SubElement(adresse_information,'adresse')
		adresse.attrib['numero'] = str(row['adresse-information-numero'])
		ligne = ET.SubElement(adresse,'ligne')
		ligne.text = str(row['adresse-information-numero'])+str(row['adresse-information-ligne'])
		codepostal = ET.SubElement(adresse,'codepostal')
		codepostal.text = str(row['adresse-information-codepostal'])
		ville = ET.SubElement(adresse,'ville')
		ville.text = str(row['adresse-information-ville'])

		restauration = ET.SubElement(action,'restauration')
		restauration.text = str(row['restauration'])

		hebergement = ET.SubElement(action,'hebergement')
		hebergement.text = str(row['hebergement'])

		transport = ET.SubElement(action,'transport')
		transport.text = str(row['transport'])

		acces_handicapes = ET.SubElement(action,'acces-handicapes')
		acces_handicapes.text = str(row['acces-handicapes'])

		langue_formation = ET.SubElement(action,'langue-formation')
		langue_formation.text = str(row['langue-formation'])

		modalites_recrutement = ET.SubElement(action,'modalites-recrutement')
		modalites_recrutement.text = str(row['modalites-recrutement'])

		modalites_pedagogiques = ET.SubElement(action,'modalites-pedagogiques')
		modalites_pedagogiques.text = str(row['modalites-pedagogiques'])

		code_perimetre_recrutement = ET.SubElement(action,'code-perimetre-recrutement')
		code_perimetre_recrutement.text = str(row['code-perimetre-recrutement'])

		nombre_heures_centre = ET.SubElement(action,'nombre-heures-centre')
		nombre_heures_centre.text = str(row['nombre-heures-centre'])

		nombre_heures_entreprise = ET.SubElement(action,'nombre-heures-entreprise')
		nombre_heures_entreprise.text = str(row['nombre-heures-entreprise'])

		# Extras
		extras = ET.SubElement(action,'extras')
		extras.attrib['info'] = 'action'
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'contact-information'
		coordonnees = ET.SubElement(extra,'coordonnees')
		coordonnees.attrib['numero'] = str(row['action-extra-coordonnees-numero'])
		nom = ET.SubElement(coordonnees,'nom')
		nom.text = str(row['action-extra-coordonnees-nom'])
		prenom = ET.SubElement(coordonnees,'prenom')
		prenom.text = str(row['action-extra-coordonnees-prenom'])
		telfixe = ET.SubElement(coordonnees,'telfixe')
		numtel = ET.SubElement(telfixe,'numtel')
		numtel.text = str(row['action-extra-numtel'])
		courriel = ET.SubElement(coordonnees,'courriel')
		courriel.text = str(row['action-extra-courriel'])
		
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'modalites-handicap'
		extra.text = str(row['action-extra-modalites-handicap'])
		
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'info-admission'
		extra.text = str(row['action-extra-info-admission'])
		
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'duree-apprentissage'
		extra.text = str(row['action-extra-duree-apprentissage'])
		
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'code-rythme-formation'
		extra.text = str(row['action-extra-code-rythme-formation'])
		
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'individuelle-collective'
		extra.text = str(row['action-extra-individuelle-collective'])
		
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'frais-anpec'
		extra.text = str(row['action-extra-frais-anpec'])
		
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'detail-frais-anpec'
		extra.text = str(row['action-extra-detail-frais-anpec'])
		
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'code-modele-economique'
		extra.text = str(row['action-extra-code-modele-economique'])
		
		extra = ET.SubElement(extras,'extras')
		extra2 = ET.SubElement(extra,'extra')
		extra2.attrib['info'] = 'taux-tva'
		extra2.text = str(row['action-extra-taux-tva'])
		extra2 = ET.SubElement(extra,'extra')
		extra2.attrib['info'] = 'frais-ht'
		extra2.text = str(row['action-extra-frais-ht'])
		extra2 = ET.SubElement(extra,'extra')
		extra2.attrib['info'] = 'frais-ttc'
		extra2.text = str(row['action-extra-frais-ttc'])
		
		# Organisme de formation
		organisme_formation_responsable = ET.SubElement(formation,'organisme-formation-responsable')
		SIRET_organisme_formation = ET.SubElement(organisme_formation_responsable,'SIRET-organisme-formation')
		siret = ET.SubElement(SIRET_organisme_formation,'SIRET')
		siret.text = str(row['SIRET'])

		# Extra
		extras = ET.SubElement(formation,'extras')
		extras.attrib['info'] = 'formation'
		extra = ET.SubElement(extras,'extra')
		extra.attrib['info'] = 'resume-contenu'
		extra.text = str(row['resume-contenu'])
		
	print("File generated.")

	# create a new XML file with the results
	myoffers = ET.tostring(lheo, encoding='utf-8').decode() # python3
	# myoffers = ET.tostring(lheo, encoding='UTF-8').decode()
	mycatalogue = io.open("catalogue.xml", "w", encoding='utf8')
	mycatalogue.write(myoffers)
	
# Start parsing
parse_generate()

# Remove files
def remove_file(filename):
	if os.path.exists(filename):
		os.remove(filename)
		return

# Delete old trame.csv
for f in glob.glob("trame.csv*"):
    os.remove(f)