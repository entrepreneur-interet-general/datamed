#!/usr/bin/env python
# coding: utf-8

# # Décret stock
# Définir une métrique pour le choix des classes ATC à prioriser dans le décret stock

# In[1]:


import sys
from collections import defaultdict

import numpy as np
import pandas as pd

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db

pd.set_option('display.max_rows', None)


# # Table ruptures

# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df = pd.read_sql_table('ruptures_dc', connection)
df = df[['id_signal', 'date_signalement', 'laboratoire', 'specialite', 'voie', 'voie_4_classes', 'atc',
         'date_signal_debut_rs', 'duree_ville', 'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]
df = df[df.date_signalement >= '2018-01-01']
df.atc = df.atc.str.upper()
df.specialite = df.apply(
    lambda x: x.specialite.replace(' /', '/').replace('/ ', '/').replace('intraoculaire', 'intra-oculaire'),
    axis=1)

df.head(2)


# In[4]:


len(df)


# # Avoir toutes les combinaisons (atc, voie_4_classes) possibles

# In[5]:


from itertools import product

# tous les tuples possibles (atc, voie_4_classes)
atc_voie_tuples = list(set(product(df.atc, df.voie_4_classes)))


# In[6]:


df['atc_voie'] = df.apply(lambda x: (x.atc, x.voie_4_classes) if x.atc else None, axis=1)


# # Retrouver le code CIS

# In[7]:


df_cis_1 = pd.read_sql_table('specialite', connection)
df_cis_1 = df_cis_1[df_cis_1.type_amm != "Autorisation d'importation parallèle"]
df_cis_1 = df_cis_1.rename(columns={'name': 'specialite'})


# In[8]:


df_cis_2 = pd.read_excel('../data/decret_stock/correspondance_cis_nom.xlsx', names=['specialite', 'cis'])
df_cis_2 = df_cis_2.drop(df_cis_2.index[0])
df_cis_2.specialite = df_cis_2.specialite.str.lower()
df_cis_2.cis = df_cis_2.cis.map(str)
df_cis_2 = df_cis_2.drop_duplicates()
df_cis_2['type_amm'] = None
df_cis_2['etat_commercialisation'] = None
df_cis_2 = df_cis_2[~df_cis_2.cis.isin(df_cis_1.cis.unique())]


# In[9]:


df_cis = pd.concat([df_cis_1, df_cis_2])
df_cis = df_cis[~df_cis.specialite.isna()]

df_cis.head(1)


# # Ventes

# In[10]:


# Le count ne garde pas les NaN
df_ventes = pd.read_sql_table('ventes', connection)
df_ventes = df_ventes.where(pd.notnull(df_ventes), '')

df_ventes.atc = df_ventes.atc.replace(['N03AE', 'N05AX'], ['N05CD08', 'N03AG02'])
df_ventes.atc = df_ventes.atc.replace(['J05AP01'], ['J05AB04'])
df_ventes.atc = df_ventes.atc.replace(['A04AD'], ['N05AD08'])
df_ventes.loc[df_ventes.cis == '68915556', 'voie_4_classes'] = 'iv'
df_ventes.loc[df_ventes.cis == '68915556', 'voie'] = 'iv'

df_ventes['atc_voie'] = df_ventes.apply(lambda x: (x.atc, x.voie_4_classes) if x.atc else None, axis=1)
df_ventes['ventes_total'] = df_ventes['unites_officine'] + df_ventes['unites_hopital']

df_ventes.head(1)


# # SMR

# In[11]:


df_smr = pd.read_sql_table('service_medical_rendu', connection)

df_smr.smr = df_smr.smr.replace(
    ['Important', 'Insuffisant', 'Modéré', 'Faible', 'Non précisé', 'Commentaires'],
    [4, 1, 3, 2, 0, 0]
)

df_smr.head()


# In[12]:


# Merge df_smr in df_ventes
df_ventes = df_ventes.merge(df_smr[['cis', 'smr']], on='cis', how='left')


# # Froid

# In[13]:


df_froid = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/analysis/data/decret_stock/froid.csv',
                       dtype={'cis': str})
#df_froid.cis = df_froid.cis.map(int)
#df_froid.cis = df_froid.cis.map(str)


# In[14]:


# Merge df_froid in df_ventes
df_ventes['froid'] = df_ventes.cis.apply(lambda x: x in df_froid.cis.unique())


# # Stupéfiants

# In[15]:


df_stup = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/analysis/data/decret_stock/stupefiants.csv',
                      dtype={'cis': str})
#df_stup.cis = df_stup.cis.map(int)
#df_stup.cis = df_stup.cis.map(str)


# In[16]:


# Merge df_stup in df_ventes
df_ventes['stup'] = df_ventes.cis.apply(lambda x: x in df_stup.cis.unique())


# # MITM oui/non

# In[17]:


df_mitm = pd.read_sql_table('production', connection)
df_mitm = df_mitm[['cis', 'mitm']]

df_mitm['mitm_oui'] = df_mitm.mitm.apply(lambda x: 'oui' if x == 'oui' else None)
df_mitm['mitm_non'] = df_mitm.mitm.apply(lambda x: 'oui' if (pd.isnull(x) or x != 'oui') else None)
df_mitm = df_mitm.where(pd.notnull(df_mitm), None)

# df_mitm = df_mitm[df_mitm.mitm == 'oui']
# df_mitm = df_mitm.dropna()
df_mitm = df_mitm.drop_duplicates()
df_mitm.head(1)


# In[18]:


df_ventes = df_ventes.merge(df_mitm, on='cis', how='left')
df_ventes.mitm_non = df_ventes.apply(
    lambda x: 'oui' if (pd.isnull(x.mitm_oui) and pd.isnull(x.mitm_non)) else x.mitm_non, axis=1
)


# # Grouper par ...

# In[19]:


group = 'atc_voie'


# In[20]:


# df_mitm_by_group = df_ventes.groupby([group, 'cis']).agg(
#     {'mitm': 'nunique'}).reset_index().groupby(group).sum().reset_index()
df_mitm_by_group = df_ventes.groupby([group, 'cis']).agg(
    {'mitm_oui': 'nunique', 'mitm_non': 'nunique'}).reset_index().groupby(group).sum().reset_index()

df_froid_by_group = df_ventes.groupby([group, 'cis']).agg(
    {'froid': 'first'}).reset_index().groupby(group).sum().reset_index()

df_stup_by_group = df_ventes.groupby([group, 'cis']).agg(
    {'stup': 'first'}).reset_index().groupby(group).sum().reset_index()

df_smr_by_group = df_ventes.groupby(group).agg({'smr': 'max'}).reset_index()


# In[21]:


# Compter nb spécialités par classe ATC
df_nb_spe = df_ventes.groupby(group).agg({'cis': 'nunique'}).reset_index()
df_nb_spe = df_nb_spe.rename(columns={'cis': 'nb_specialites_groupe'})
df_nb_spe = df_nb_spe.merge(df_mitm_by_group, on=group, how='left')
df_nb_spe = df_nb_spe.merge(df_froid_by_group, on=group, how='left')
df_nb_spe = df_nb_spe.merge(df_stup_by_group, on=group, how='left')
df_nb_spe = df_nb_spe.merge(df_smr_by_group, on=group, how='left')

df_nb_spe['pourcentage_mitm'] = df_nb_spe.apply(lambda x: x.mitm_oui / x.nb_specialites_groupe * 100, axis=1)
df_nb_spe['pourcentage_non_mitm'] = df_nb_spe.apply(lambda x: x.mitm_non / x.nb_specialites_groupe * 100, axis=1)
df_nb_spe['pourcentage_froid'] = df_nb_spe.apply(lambda x: x.froid / x.nb_specialites_groupe * 100, axis=1)
df_nb_spe['pourcentage_stup'] = df_nb_spe.apply(lambda x: x.stup / x.nb_specialites_groupe * 100, axis=1)

df_nb_spe.head(3)


# # Ventes par ATC, CIS, etc.

# In[22]:


# Récupérer l'année du signalement
df['annee'] = df.date_signalement.apply(lambda x: x.year)


# In[23]:


df_ventes_groupe = df_ventes.groupby(['annee', group]).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_groupe = df_ventes_groupe.to_dict(orient='records')
ventes_par_groupe = {annee: {ventes_dict[group]: ventes_dict['ventes_total']
                            for ventes_dict in ventes_par_groupe if ventes_dict['annee'] == annee - 1}
                     for annee in df.annee.unique()}

df_ventes_cis = df_ventes.groupby(['annee', 'cis']).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_cis = df_ventes_cis.to_dict(orient='records')
ventes_par_cis = {annee: {ventes_dict['cis']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == annee - 1}
                  for annee in df.annee.unique()}


# In[24]:


df = df[['id_signal', 'date_signalement', 'annee', 'atc', 'atc_voie', 'laboratoire', 'specialite',
         'date_signal_debut_rs', 'duree_ville', 'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]

df.head(2)


# # Calculer durée rupture

# In[25]:


def compute_jours(x):
    """
    Nombre de jours entre la date de prévision de fin et la date de début de RS
    """
    jours_ville = (x.date_previ_ville - x.date_signal_debut_rs).days
    jours_hopital = (x.date_previ_hopital - x.date_signal_debut_rs).days
    return max(0, jours_ville), max(0, jours_hopital)

df['jours_ville'] = df.apply(lambda x: compute_jours(x)[0], axis=1)
df['jours_hopital'] = df.apply(lambda x: compute_jours(x)[1], axis=1)


# In[26]:


def get_duree(x):
    """
    Pour chaque signalement, calculer la duree totale de la rupture
    """
    return max(x.jours_ville, x.jours_hopital)
    
# Durée moyenne des ruptures pour duree_ville ≥ 3 mois
mean_3_months = df[df.duree_ville == '≥ 3 mois'].apply(lambda x: get_duree(x), axis=1).replace(0, np.NaN).mean()

# Durée moyenne des ruptures sur tout le dataset
mean_all = df.apply(lambda x: get_duree(x), axis=1).replace(0, np.NaN).mean()

print('Mean 3 months: {} days - Mean all: {} days'.format(round(mean_3_months, 2), round(mean_all, 2)))


# In[27]:


duree_dict = {
    '≤ 1 semaine': 7,
    'Entre 1 semaine et 1 mois': 21,
    '1 à 3 mois': 70,
    '≥ 3 mois': mean_3_months,
    'Indéterminée': mean_all,
}

def compute_duree_rs(x):
    if x.jours_ville or x.jours_hopital:
        return max(x.jours_ville, x.jours_hopital)
    elif x.duree_ville or x.duree_hopital:
        return max(duree_dict.get(x.duree_ville, 0), duree_dict.get(x.duree_hopital, 0))
    else:
        return duree_dict['Indéterminée']
        
df['nb_jours_rs'] = df.apply(lambda x: compute_duree_rs(x), axis=1)


# In[28]:


len(df)


# # Retirer les ruptures de moins de 6 jours

# In[29]:


print('{}% of RS reportings last less than 2 weeks'.format(round(len(df[df.nb_jours_rs <= 14]) / len(df) * 100, 2)))


# In[30]:


df = df[df.nb_jours_rs > 14]


# # Caper les ruptures supérieures à 4 mois à 4 mois

# In[31]:


df.nb_jours_rs = df.nb_jours_rs.apply(lambda x: 122 if x > 122 else x)


# # Calcul d'une métrique

# In[32]:


len(df)


# ## 1) Pondérer par les ventes

# In[33]:


# Trouver, par classe ATC, la spécialité qui a les plus grands chiffres de vente sur 2018-2019
df_spe_max_ventes = df_ventes.groupby(
    [group, 'denomination_specialite']).agg({'ventes_total': 'sum'}).reset_index()

def get_spe_max_ventes(df_spe_max_ventes):
    """
    Pour chaque groupe, avoir la spécialité la plus vendue, sur toutes les années
    """
    records = df_spe_max_ventes.to_dict(orient='records')
    rec_dict = defaultdict(dict)
    for g in df_spe_max_ventes[group].unique():
        rec_dict[g] = {d['denomination_specialite']: d['ventes_total'] for d in records if d[group] == g}
    return {k: max(v, key=v.get) for k, v in rec_dict.items()}

max_ventes_dict = get_spe_max_ventes(df_spe_max_ventes)


# In[34]:


# Grouper par année et spécialité
df_ventes_spe = df.groupby(['annee', group, 'specialite']).agg({'nb_jours_rs': 'sum'}).reset_index()
df_ventes_spe = df_ventes_spe.merge(df_cis[['cis', 'specialite']].dropna(), on='specialite', how='left')

df_ventes_spe['ventes_cis'] = df_ventes_spe.apply(lambda x: ventes_par_cis[x.annee].get(x.cis), axis=1)

# Savoir pour combien de CIS on a les chiffres de vente
df_ventes_spe['ventes_exist'] = df_ventes_spe.ventes_cis.apply(lambda x: 0 if pd.isnull(x) else 1)

df_ventes_spe.head(3)


# ## CIS qui n'ont pas de voie dans ventes 2017 mais qui en ont dans ruptures

# In[35]:


cis_no_voie = df_ventes[df_ventes.voie == ''].cis.unique().tolist()


# In[36]:


len(cis_no_voie)


# In[37]:


df_ventes_spe[df_ventes_spe.cis.isin(cis_no_voie)]


# In[38]:


df_ventes[df_ventes.cis.isin(cis_no_voie[:3])][['annee', 'cis', 'atc_voie']]


# ## Grouper les ruptures par année et classe ATC

# In[39]:


# Grouper par année et par classe ATC
df_ventes_annee_groupe = df_ventes_spe.groupby(['annee', group]).agg(
    {'ventes_exist': 'sum', 'ventes_cis': 'sum', 'nb_jours_rs': 'sum'}).reset_index()
df_ventes_annee_groupe['ventes_groupe'] = df_ventes_annee_groupe.apply(
    lambda x: ventes_par_groupe[x.annee].get(x[group]), axis=1)

# Rajouter le nombre de spécialités à la dataframe
df_ventes_annee_groupe = df_ventes_annee_groupe.merge(df_nb_spe, on=group, how='left')
df_ventes_annee_groupe = df_ventes_annee_groupe.rename(columns={'specialite': 'nb_specialites_groupe'})

# Attribuer des ventes aux CIS = NaN
df_ventes_annee_groupe['ventes_cis_inconnus'] = df_ventes_annee_groupe.apply(
    lambda x: (x.ventes_groupe - x.ventes_cis) / (x.nb_specialites_groupe - x.ventes_exist)
    if (x.nb_specialites_groupe - x.ventes_exist) else 0, axis=1)

df_ventes_annee_groupe.head(3)


# In[40]:


# Ventes des cis de la classe ATC qui n'apparaissent pas dans les ruptures
#df_ventes_annee_groupe = df_ventes_annee_groupe.where(pd.notnull(df_ventes_annee_groupe), None)
records = df_ventes_annee_groupe.to_dict(orient='records')

ventes_cis_inconnus_dict = {(r['annee'], r[group]): r['ventes_cis_inconnus'] for r in records}

nb_spe_par_groupe = {r[group]: r['nb_specialites_groupe'] for r in records}


# In[41]:


# Ajouter à la colonne ventes_cis les ventes estimées sur les cis inconnus
df_ventes_spe.ventes_cis = df_ventes_spe.apply(
    lambda x: ventes_cis_inconnus_dict.get((x.annee, x[group]))
    if pd.isnull(x.ventes_cis) else x.ventes_cis, axis=1)

df_ventes_spe['ventes_groupe'] = df_ventes_spe.apply(lambda x: ventes_par_groupe[x.annee].get(x[group], 0), axis=1)

df_ventes_spe.head(2)


# In[42]:


def compute_score(g, df):
    """
    Calcul d'un score pondéré par les ventes
    """
    return sum([
        x.nb_jours_rs * (1 if not x.ventes_groupe else x.ventes_cis / x.ventes_groupe)
        for _, x in df[df[group] == g].iterrows()
    ])

df_score = df_ventes_annee_groupe.groupby(group).agg(
    {'ventes_groupe': 'sum', 'ventes_cis': 'sum', 'ventes_cis_inconnus': 'sum', 'nb_jours_rs': 'sum'}).reset_index()

df_score = df_score.merge(df_nb_spe, on=group, how='left')
df_score['score'] = df_score[group].apply(lambda x: compute_score(x, df_ventes_spe))

df_score['specialite_plus_vendue'] = df_score[group].apply(
    lambda x: max_ventes_dict[x] if x in max_ventes_dict else None)

# Ajouter le nom de la classe ATC (= DCI)
df_atc = pd.read_sql('specialite', connection)
name_by_atc = df_atc.to_dict(orient='records')
name_by_atc = {d['atc']: d['nom_atc'] for d in name_by_atc}
df_score['nom_atc'] = df_score.atc_voie.apply(lambda x: name_by_atc.get(x[0], None))

df_score = df_score[
    [group, 'nom_atc', 'ventes_groupe', 'specialite_plus_vendue', 'nb_jours_rs',
     'nb_specialites_groupe', 'mitm_oui', 'mitm_non', 'pourcentage_mitm', 'pourcentage_non_mitm',
     'froid', 'pourcentage_froid', 'stup', 'pourcentage_stup', 'smr', 'score']
].sort_values(by=['score'], ascending=False)

df_score.head(10)


# In[43]:


# df_score[df_score.atc == 'A06AH01']


# In[44]:


# len(df[df.atc.apply(lambda x: len(x) != 7 if x else True)])


# # Sauvegarder dans csv

# In[45]:


df_score.to_csv('../data/decret_stock/classes_atc_score_pondéré_niveau_atc5_voie_mitm.csv', index=False, sep=';')


# # Nombre de ruptures ayant l'ATC complet

# In[46]:


# len(df[df.atc.apply(lambda x: len(x) == 7 if x and isinstance(x, str) else False)]) / len(df) * 100


# In[47]:


group = ('N05CD08', 'orale')    #('G03DB07', 'orale')


# In[48]:


x = df_ventes_spe[df_ventes_spe.atc_voie == group].iloc[0]


# In[49]:


df_score[df_score.atc_voie == group]


# In[50]:


df_ventes[df_ventes.atc_voie == group]


# In[51]:


# df_ventes[df_ventes.denomination_specialite.str.contains('de sodium sandoz')]


# In[ ]:




