import os
import lxml.etree as ET

import chardet
import pandas as pd
from lxml.etree import CDATA

from utils.log import write_server_log


def celltostr(cell):
    if not pd.isnull(cell):
        return str(cell)
    return ''


def parse_generate(file_csv_path):
    if not os.path.exists(file_csv_path):
        write_server_log("File does not exists")
        return False

    # XML
    # create the file structure
    lheo = ET.Element('lheo')
    lheo.attrib['xmlns'] = 'https://www.of.moncompteformation.gouv.fr'

    offres = ET.SubElement(lheo, 'offres')

    file_encoding = 'UTF-8'
    sep = ','
    with open(fr'{file_csv_path}', 'rb') as f:
        result = chardet.detect(f.read())  # or readline if the file is large
        file_encoding = result['encoding']
        if file_encoding.lower() != "utf-8":
            sep = ';'

    write_server_log(f"Encoding is {file_encoding}")
    engine = 'c'  # c or python

    # Read in the data
    # ISO-8859-1
    # unicode
    # utf-16
    # utf-8
    # cp1252
    # utf-8-sig
    # latin1
    try:
        data = pd.read_csv(file_csv_path, engine=engine, encoding=file_encoding, error_bad_lines=False, sep=sep,
                        quotechar="\"")

        for index, row in data.iterrows():
            write_server_log("File generation...")
            write_server_log(index)

            formation = ET.SubElement(offres, 'formation')
            formation.attrib['numero'] = celltostr(row['numero'])
            formation.attrib['datemaj'] = celltostr(row['datemaj'])
            formation.attrib['datecrea'] = celltostr(row['datecrea'])

            intitule_formation = ET.SubElement(formation, 'intitule-formation')
            intitule_formation.text = celltostr(row['intitule-formation'])

            objectif_formation = ET.SubElement(formation, 'objectif-formation')
            objectif_formation.text = CDATA(celltostr(row['objectif-formation']))

            resultats_attendus = ET.SubElement(formation, 'resultats-attendus')
            resultats_attendus.text = CDATA(celltostr(row['resultats-attendus']))

            contenu_formation = ET.SubElement(formation, 'contenu-formation')
            contenu_formation.text = CDATA(celltostr(row['contenu-formation']))

            parcours_de_formation = ET.SubElement(formation, 'parcours-de-formation')
            parcours_de_formation.text = celltostr(row['parcours-de-formation'])

            objectif_general_formation = ET.SubElement(formation, 'objectif-general-formation')
            objectif_general_formation.text = celltostr(row['objectif-general-formation'])

            certification = ET.SubElement(formation, 'certification')
            code_CERTIFINFO = ET.SubElement(certification, 'code-CERTIFINFO')
            code_CERTIFINFO.text = celltostr(row['code-CERTIFINFO'])

            # Action
            action = ET.SubElement(formation, 'action')
            action.attrib['numero'] = celltostr(row['action-numero'])
            action.attrib['datemaj'] = celltostr(row['action-datemaj'])
            action.attrib['datecrea'] = celltostr(row['action-datecrea'])

            # rythme_formation = ET.SubElement(action,'rythme-formation')
            # rythme_formation.text = celltostr(row['rythme-formation'])

            niveau_entree_obligatoire = ET.SubElement(action, 'niveau-entree-obligatoire')
            niveau_entree_obligatoire.text = celltostr(row['niveau-entree-obligatoire'])

            modalites_enseignement = ET.SubElement(action, 'modalites-enseignement')
            modalites_enseignement.text = celltostr(row['modalites-enseignement'])

            conditions_specifiques = ET.SubElement(action, 'conditions-specifiques')
            conditions_specifiques.text = CDATA(celltostr(row['conditions-specifiques']))

            lieu_de_formation = ET.SubElement(action, 'lieu-de-formation')
            coordonnees = ET.SubElement(lieu_de_formation, 'coordonnees')
            coordonnees.attrib['numero'] = celltostr(row['lieu-de-formation-coordonnees-numero'])

            nom = ET.SubElement(coordonnees, 'nom')
            nom.text = celltostr(row['lieu-de-formation-coordonnees-nom'])
            prenom = ET.SubElement(coordonnees, 'prenom')
            prenom.text = celltostr(row['lieu-de-formation-coordonnees-prenom'])

            adresse = ET.SubElement(coordonnees, 'adresse')
            adresse.attrib['numero'] = celltostr(row['lieu-de-formation-adresse-numero'])

            ligne = ET.SubElement(adresse, 'ligne')
            ligne.text = celltostr(row['lieu-de-formation-adresse-numero']) + ' ' + celltostr(
                row['lieu-de-formation-adresse-ligne'])
            codepostal = ET.SubElement(adresse, 'codepostal')
            codepostal.text = celltostr(row['lieu-de-formation-adresse-codepostal'])
            ville = ET.SubElement(adresse, 'ville')
            ville.text = celltostr(row['lieu-de-formation-adresse-ville'])

            # Geoloc
            geoloc = ET.SubElement(adresse, 'geolocalisation')
            lat = ET.SubElement(geoloc, 'latitude')
            lat.text = celltostr(row['lieu-de-formation-latitude'])
            lng = ET.SubElement(geoloc, 'longitude')
            lng.text = celltostr(row['lieu-de-formation-longitude'])

            # Extra adresse
            extras = ET.SubElement(adresse, 'extras')
            extras.attrib['info'] = 'adresse'
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'numero-voie'
            extra.text = celltostr(row['lieu-de-formation-extra-numero'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'code-nature-voie'
            extra.text = celltostr(row['lieu-de-formation-extra-codevoie'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'libelle-voie'
            extra.text = celltostr(row['lieu-de-formation-extra-libvoie'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'accessibilite-batimentaire'
            extra.text = celltostr(row['lieu-de-formation-extra-acces'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'conformite-reglementaire'
            extra.text = celltostr(row['lieu-de-formation-extra-regle'])

            telfixe = ET.SubElement(coordonnees, 'telfixe')
            numtel = ET.SubElement(telfixe, 'numtel')
            numtel.text = celltostr(row['lieu-de-formation-numtel'])

            courriel = ET.SubElement(coordonnees, 'courriel')
            courriel.text = celltostr(row['lieu-de-formation-courriel'])

            modalites_entrees_sorties = ET.SubElement(action, 'modalites-entrees-sorties')
            modalites_entrees_sorties.text = celltostr(row['modalites-entrees-sorties'])

            url_action = ET.SubElement(action, 'url-action')
            urlweb = ET.SubElement(url_action, 'urlweb')
            urlweb.text = celltostr(row['urlweb'])

            session = ET.SubElement(action, 'session')
            session.attrib['numero'] = celltostr(row['session-numero'])
            session.attrib['datemaj'] = celltostr(row['session-datemaj'])
            session.attrib['datecrea'] = celltostr(row['session-datecrea'])

            periode = ET.SubElement(session, 'periode')
            debut = ET.SubElement(periode, 'debut')
            fin = ET.SubElement(periode, 'fin')
            debut.text = celltostr(row['debut'])
            fin.text = celltostr(row['fin'])

            adresse_inscription = ET.SubElement(session, 'adresse-inscription')
            adresse = ET.SubElement(adresse_inscription, 'adresse')
            adresse.attrib['numero'] = celltostr(row['session-adresse-numero'])
            ligne = ET.SubElement(adresse, 'ligne')
            ligne.text = celltostr(row['session-adresse-numero']) + celltostr(row['session-adresse-ligne'])
            codepostal = ET.SubElement(adresse, 'codepostal')
            codepostal.text = celltostr(row['session-adresse-codepostal'])
            ville = ET.SubElement(adresse, 'ville')
            ville.text = celltostr(row['session-adresse-ville'])

            # Session Geoloc
            geoloc = ET.SubElement(adresse, 'geolocalisation')
            lat = ET.SubElement(geoloc, 'latitude')
            lat.text = celltostr(row['session-latitude'])
            lng = ET.SubElement(geoloc, 'longitude')
            lng.text = celltostr(row['session-longitude'])

            # Session Extra adresse
            extras = ET.SubElement(adresse, 'extras')
            extras.attrib['info'] = 'adresse'
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'numero-voie'
            extra.text = celltostr(row['session-extra-numero'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'code-nature-voie'
            extra.text = celltostr(row['session-extra-codevoie'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'libelle-voie'
            extra.text = celltostr(row['session-extra-libvoie'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'accessibilite-batimentaire'
            extra.text = celltostr(row['session-extra-acces'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'conformite-reglementaire'
            extra.text = celltostr(row['session-extra-regle'])

            etat_recrutement = ET.SubElement(session, 'etat-recrutement')
            etat_recrutement.text = celltostr(row['etat-recrutement'])

            # Extras
            extras = ET.SubElement(session, 'extras')
            extras.attrib['info'] = 'session'
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'contact-inscription'
            coordonnees = ET.SubElement(extra, 'coordonnees')
            coordonnees.attrib['numero'] = celltostr(row['session-extra-coordonnees-numero'])
            nom = ET.SubElement(coordonnees, 'nom')
            nom.text = celltostr(row['session-extra-coordonnees-nom'])
            prenom = ET.SubElement(coordonnees, 'prenom')
            prenom.text = celltostr(row['session-extra-coordonnees-prenom'])
            telfixe = ET.SubElement(coordonnees, 'telfixe')
            numtel = ET.SubElement(telfixe, 'numtel')
            numtel.text = celltostr(row['session-extra-numtel'])
            courriel = ET.SubElement(coordonnees, 'courriel')
            courriel.text = celltostr(row['session-extra-courriel'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'garantie'
            extra.text = celltostr(row['session-extra-garantie'])

            # Adresse Info
            adresse_information = ET.SubElement(action, 'adresse-information')
            adresse = ET.SubElement(adresse_information, 'adresse')
            adresse.attrib['numero'] = celltostr(row['adresse-information-numero'])
            ligne = ET.SubElement(adresse, 'ligne')
            ligne.text = celltostr(row['adresse-information-numero']) + ' ' + celltostr(row['adresse-information-ligne'])
            codepostal = ET.SubElement(adresse, 'codepostal')
            codepostal.text = celltostr(row['adresse-information-codepostal'])
            ville = ET.SubElement(adresse, 'ville')
            ville.text = celltostr(row['adresse-information-ville'])

            # Adresse Info Geoloc
            geoloc = ET.SubElement(adresse, 'geolocalisation')
            lat = ET.SubElement(geoloc, 'latitude')
            lat.text = celltostr(row['adresse-information-latitude'])
            lng = ET.SubElement(geoloc, 'longitude')
            lng.text = celltostr(row['adresse-information-longitude'])

            # Adresse Info Extra adresse
            extras = ET.SubElement(adresse, 'extras')
            extras.attrib['info'] = 'adresse'
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'ligne5-adresse'
            extra.text = celltostr(row['adresse-information-extra-ligne5-adresse'])
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'conformite-reglementaire'
            extra.text = celltostr(row['adresse-information-extra-regle'])

            restauration = ET.SubElement(action, 'restauration')
            restauration.text = CDATA(celltostr(row['restauration']))

            hebergement = ET.SubElement(action, 'hebergement')
            hebergement.text = CDATA(celltostr(row['hebergement']))

            transport = ET.SubElement(action, 'transport')
            transport.text = CDATA(celltostr(row['transport']))

            acces_handicapes = ET.SubElement(action, 'acces-handicapes')
            acces_handicapes.text = celltostr(row['acces-handicapes'])

            langue_formation = ET.SubElement(action, 'langue-formation')
            langue_formation.text = celltostr(row['langue-formation'])

            modalites_recrutement = ET.SubElement(action, 'modalites-recrutement')
            modalites_recrutement.text = celltostr(row['modalites-recrutement'])

            modalites_pedagogiques = ET.SubElement(action, 'modalites-pedagogiques')
            modalites_pedagogiques.text = CDATA(celltostr(row['modalites-pedagogiques']))

            code_perimetre_recrutement = ET.SubElement(action, 'code-perimetre-recrutement')
            code_perimetre_recrutement.text = celltostr(row['code-perimetre-recrutement'])

            nombre_heures_centre = ET.SubElement(action, 'nombre-heures-centre')
            nombre_heures_centre.text = celltostr(row['nombre-heures-centre'])

            nombre_heures_entreprise = ET.SubElement(action, 'nombre-heures-entreprise')
            nombre_heures_entreprise.text = celltostr(row['nombre-heures-entreprise'])

            # Extras
            extras = ET.SubElement(action, 'extras')
            extras.attrib['info'] = 'action'
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'contact-information'
            coordonnees = ET.SubElement(extra, 'coordonnees')
            coordonnees.attrib['numero'] = celltostr(row['action-extra-coordonnees-numero'])
            nom = ET.SubElement(coordonnees, 'nom')
            nom.text = celltostr(row['action-extra-coordonnees-nom'])
            prenom = ET.SubElement(coordonnees, 'prenom')
            prenom.text = celltostr(row['action-extra-coordonnees-prenom'])
            telfixe = ET.SubElement(coordonnees, 'telfixe')
            numtel = ET.SubElement(telfixe, 'numtel')
            numtel.text = celltostr(row['action-extra-numtel'])
            courriel = ET.SubElement(coordonnees, 'courriel')
            courriel.text = celltostr(row['action-extra-courriel'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'modalites-handicap'
            extra.text = celltostr(row['action-extra-modalites-handicap'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'info-admission'
            extra.text = celltostr(row['action-extra-info-admission'])

            extra = ET.SubElement(extras, 'extras')
            extra.attrib['info'] = 'codes-modalites-admission'
            extra2 = ET.SubElement(extra, 'extra')
            extra2.attrib['info'] = 'code-modalites-admission'
            extra2.text = celltostr(row['action-extra-modalites-admission'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'duree-apprentissage'
            extra.text = celltostr(row['action-extra-duree-apprentissage'])

            extra = ET.SubElement(extras, 'extras')
            extra.attrib['info'] = 'codes-rythme-formation'
            extra2 = ET.SubElement(extra, 'extra')
            extra2.attrib['info'] = 'code-rythme-formation'
            extra2.text = celltostr(row['action-extra-codes-rythme-formation'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'individuelle-collective'
            extra.text = celltostr(row['action-extra-individuelle-collective'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'frais-anpec'
            extra.text = celltostr(row['action-extra-frais-anpec'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'frais-certif-inclus-frais-anpec'
            extra.text = celltostr(row['action-extra-frais-certif-anpec'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'detail-frais-anpec'
            extra.text = celltostr(row['action-extra-detail-frais-anpec'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'code-modele-economique'
            extra.text = celltostr(row['action-extra-code-modele-economique'])

            extra = ET.SubElement(extras, 'extras')
            extra.attrib['info'] = 'frais-pedagogiques'
            extra2 = ET.SubElement(extra, 'extra')
            extra2.attrib['info'] = 'taux-tva'
            extra2.text = celltostr(row['action-extra-taux-tva'])
            extra2 = ET.SubElement(extra, 'extra')
            extra2.attrib['info'] = 'frais-ht'
            extra2.text = celltostr(row['action-extra-frais-ht'])
            extra2 = ET.SubElement(extra, 'extra')
            extra2.attrib['info'] = 'frais-ttc'
            extra2.text = celltostr(row['action-extra-frais-ttc'])

            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'existence-prerequis'
            extra.text = celltostr(row['action-extra-existence-prerequis'])

            # Organisme de formation
            organisme_formation_responsable = ET.SubElement(formation, 'organisme-formation-responsable')
            SIRET_organisme_formation = ET.SubElement(organisme_formation_responsable, 'SIRET-organisme-formation')
            siret = ET.SubElement(SIRET_organisme_formation, 'SIRET')
            siret.text = celltostr(row['SIRET'])

            # Extra
            extras = ET.SubElement(formation, 'extras')
            extras.attrib['info'] = 'formation'
            extra = ET.SubElement(extras, 'extra')
            extra.attrib['info'] = 'resume-contenu'
            extra.text = CDATA(celltostr(row['resume-contenu']))
    except:
        write_server_log("Error while parsing file.")
        return False

    write_server_log("File generated.")

    # create a new XML file with the results
    # myoffers = ET.tostring(lheo, encoding='utf-8').decode()  # python3

    # Old way to save XML in UTF-8 encoding
    # mycatalogue = io.open("catalogue.xml", "w", encoding='utf8')
    # mycatalogue.write(myoffers)

    tree = ET.ElementTree(lheo)
    tree.write('upload/catalogue.xml', encoding='iso-8859-1', xml_declaration=True)
    return True
