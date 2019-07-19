# coding=latin-1

from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std
from utils_mtmc.get_mtmc_files import get_trips_in_Switzerland, get_zp
import pandas as pd
import numpy as np
from pathlib import Path


def run_nb_trips_by_public_transport():
    selected_columns_trips = ['HHNR',
                              'pseudo',
                              'w_rdist',
                              'wmittela']  # main transport mode for the trip
    df_trips_in_Switzerland = get_trips_in_Switzerland(2015, selected_columns_trips)
    ''' Remove trips including at least one pseudo trip leg (i.e., traveling as job) '''
    df_trips_in_Switzerland = df_trips_in_Switzerland[df_trips_in_Switzerland['pseudo'] == 1]
    df_trips_in_Switzerland.drop('pseudo', axis=1, inplace=True)
    ''' Count trips of people traveling '''
    df_trips_in_Switzerland['count_trips'] = 1  # Generates a new column with ones for each trip, in order to count
    df_nb_trips_per_person = df_trips_in_Switzerland.groupby('HHNR').agg({'count_trips':'count',
                                                                          'w_rdist': 'sum'})
    ''' Add people with no trips '''
    selected_columns_zp = ['HHNR', 'WP',
                           'gesl',  # Variable for sex of the person: 1 = man, 2 = woman
                           'alter',  # Variable containing the age of the person
                           'f42100e',  # Variable about the availability of cars: 1 = always, 2 = on demand, 3 = never
                           'tag',  # Day of the week: 1 = Monday, ...
                           'f41610a',  # General abonnement: 1 = yes, 2 = no
                           'f41610b',  # Half-fare abonnement: 1 = yes, ...
                           'f41610c']
    df_zp = get_zp(2015, selected_columns_zp)
    df_nb_trips_per_person = pd.merge(df_nb_trips_per_person, df_zp, left_on='HHNR', right_on = 'HHNR', how='right')
    df_nb_trips_per_person.fillna(0, inplace=True)
    ''' Get results for the full Swiss population '''
    df_output_full_population = get_nb_trips_per_person(df_nb_trips_per_person, check_official_numbers=True)
    ''' Nb trips by public transport '''
    # Keep only trips by public transport
    df_trips_in_Switzerland_by_public_transport = df_trips_in_Switzerland[df_trips_in_Switzerland['wmittela'] == 3]
    df_trips_in_Switzerland_by_public_transport = df_trips_in_Switzerland_by_public_transport.drop('wmittela', axis=1)
    df_nb_trips_per_person_by_public_transport = df_trips_in_Switzerland_by_public_transport.groupby('HHNR')\
        .agg({'count_trips':'count', 'w_rdist': 'sum'})
    df_nb_trips_per_person_by_public_transport = pd.merge(df_nb_trips_per_person_by_public_transport, df_zp,
                                                          left_on='HHNR', right_on='HHNR', how='outer')
    df_nb_trips_per_person_by_public_transport.fillna(0, inplace=True)
    df_output_by_public_transport = get_nb_trips_per_person(df_nb_trips_per_person_by_public_transport)
    df_output_by_public_transport.columns = ['Nombre de déplacements en transports publics', '+/-',
                                             'Distance journalière en transports publics, en km', '+/-']

    ''' Nb trips by public transport for people with a general abonnement '''
    df_nb_trips_per_person_by_public_transport = df_trips_in_Switzerland_by_public_transport.groupby('HHNR')\
        .agg({'count_trips':'count', 'w_rdist': 'sum'})
    df_zp_general_abo = df_zp[df_zp['f41610a'] == 1]
    df_zp.drop('f41610a', axis=1, inplace=True)
    df_nb_trips_per_person_by_PT_with_GA = pd.merge(df_nb_trips_per_person_by_public_transport, df_zp_general_abo,
                                                    left_on='HHNR', right_on='HHNR', how='right')
    del df_zp_general_abo
    df_nb_trips_per_person_by_PT_with_GA.fillna(0, inplace=True)
    df_output_by_PT_with_GA = get_nb_trips_per_person(df_nb_trips_per_person_by_PT_with_GA)
    df_output_by_PT_with_GA.columns = ["Nombre de déplacements en transports publics des possesseurs d'un abonnement "
                                       "général", '+/-',
                                       "Distance journalière en transports publics des possesseurs d'un abonnement "
                                       "général, en km", '+/-']
    ''' Nb trips by public transport for people with a half-fare abonnement '''
    df_nb_trips_per_person_by_public_transport = df_trips_in_Switzerland_by_public_transport.groupby('HHNR')\
        .agg({'count_trips':'count', 'w_rdist': 'sum'})
    df_zp_half_fare = df_zp[df_zp['f41610b'] == 1]
    df_nb_trips_per_person_by_PT_with_HT = pd.merge(df_nb_trips_per_person_by_public_transport, df_zp_half_fare,
                                                    left_on='HHNR', right_on='HHNR', how='right')
    del df_zp_half_fare
    df_nb_trips_per_person_by_PT_with_HT.fillna(0, inplace=True)
    df_output_by_PT_with_HT = get_nb_trips_per_person(df_nb_trips_per_person_by_PT_with_HT)
    df_output_by_PT_with_HT.columns = ["Nombre de déplacements en transports publics des possesseurs d'un abonnement "
                                       "demi-tarif", '+/-',
                                       "Distance journalière en transports publics des possesseurs d'un abonnement "
                                       "demi-tarif, en km", '+/-']
    ''' Nb trips by public transport for people with a community abonnement '''
    df_nb_trips_per_person_by_public_transport = df_trips_in_Switzerland_by_public_transport.groupby('HHNR')\
        .agg({'count_trips':'count', 'w_rdist': 'sum'})
    df_zp_community_abo = df_zp[df_zp['f41610c'] == 1]
    df_nb_trips_per_person_by_PT_with_community_abo = pd.merge(df_nb_trips_per_person_by_public_transport,
                                                               df_zp_community_abo,
                                                               left_on='HHNR', right_on='HHNR', how='right')
    del df_zp_community_abo
    df_nb_trips_per_person_by_PT_with_community_abo.fillna(0, inplace=True)
    df_output_by_PT_with_community_abo = get_nb_trips_per_person(df_nb_trips_per_person_by_PT_with_community_abo)
    df_output_by_PT_with_community_abo.columns = ["Nombre de déplacements en transports publics des possesseurs d'un "
                                                  "abonnement communautaire", '+/-',
                                                  "Distance journalière en transports publics des possesseurs d'un "
                                                  "abonnement communautaire, en km", '+/-']
    ''' Nb trips by public transport for people with a community abonnement and a half-fare abonnement '''
    df_nb_trips_per_person_by_public_transport = df_trips_in_Switzerland_by_public_transport.groupby('HHNR')\
        .agg({'count_trips':'count', 'w_rdist': 'sum'})
    df_zp_HT_community_abo = df_zp[(df_zp['f41610c'] == 1) & (df_zp['f41610b'] == 1)]
    df_nb_trips_per_person_by_PT_with_HT_community_abo = pd.merge(df_nb_trips_per_person_by_public_transport,
                                                                  df_zp_HT_community_abo,
                                                                  left_on='HHNR', right_on='HHNR', how='right')
    df_nb_trips_per_person_by_PT_with_HT_community_abo.fillna(0, inplace=True)
    df_output_by_PT_with_HT_community_abo = get_nb_trips_per_person(df_nb_trips_per_person_by_PT_with_HT_community_abo)
    df_output_by_PT_with_HT_community_abo.columns = ["Nombre de déplacements en transports publics des possesseurs "
                                                     "d'un abonnement communautaire et d'un abonnement demi-tarif",
                                                     '+/-',
                                                     "Distance journalière en transports publics des possesseurs "
                                                     "d'un abonnement communautaire et d'un abonnement demi-tarif, "
                                                     "en km", '+/-']
    ''' Group results together '''
    df_results = pd.concat([df_output_full_population,
                            df_output_by_public_transport,
                            df_output_by_PT_with_GA,
                            df_output_by_PT_with_HT,
                            df_output_by_PT_with_community_abo,
                            df_output_by_PT_with_HT_community_abo], axis=1)
    folder_path_output = Path('../data/output/')
    df_results.to_csv(folder_path_output / 'nb_trips_per_person.csv', index=True, sep=',', encoding='iso-8859-1')


def get_nb_trips_per_person(df_nb_trips_per_person, check_official_numbers=False):
    results = get_weighted_avg_and_std(df_nb_trips_per_person, 'WP', percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland = results[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland = results[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland = results[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland = results[0]['w_rdist'][1]
    basis = results[1]  # gives the statistical basis
    print('Basis:', basis)
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland !=  3.3670153430049696 or \
                        std_nb_trip_per_person_in_Switzerland != 0.017535045753395737 or \
                daily_dist_per_person_in_Switzerland != 36.83175306457636 or \
                        std_daily_dist_per_person_in_Switzerland != 0.4602142135149309:
            raise Exception('The official numbers are not reproduced!')
    # print('Nb of trips per person in Switzerland:', nb_trip_per_person_in_Switzerland,
    #       '+/-', std_nb_trip_per_person_in_Switzerland)

    ''' Results for men '''
    df_nb_trips_per_person_men = df_nb_trips_per_person[df_nb_trips_per_person['gesl'] == 1]
    results_men = get_weighted_avg_and_std(df_nb_trips_per_person_men, 'WP', percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_men = results_men[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_men = results_men[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_men = results_men[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_men = results_men[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_men != 3.448184538912166 or \
                        std_nb_trip_per_person_in_Switzerland_men != 0.024778470121518674 or \
                        daily_dist_per_person_in_Switzerland_men != 41.98820369365788 or \
                        std_daily_dist_per_person_in_Switzerland_men != 0.7173771733812191:
            raise Exception('The official numbers (men) are not reproduced!')
    # print('Nb of trips per person (men only) in Switzerland:', nb_trip_per_person_in_Switzerland_men,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_men)
    ''' Results for women '''
    df_nb_trips_per_person_women = df_nb_trips_per_person[df_nb_trips_per_person['gesl'] == 2]
    results_women = get_weighted_avg_and_std(df_nb_trips_per_person_women, 'WP', percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_women = results_women[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_women = results_women[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_women = results_women[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_women = results_women[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_women != 3.2879974526755964 or \
                        std_nb_trip_per_person_in_Switzerland_women != 0.02477962980210629 or \
                        daily_dist_per_person_in_Switzerland_women != 31.811968825695274 or \
                        std_daily_dist_per_person_in_Switzerland_women != 0.5764122140325488:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (women only) in Switzerland:', nb_trip_per_person_in_Switzerland_women,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_women)
    df_nb_trips_per_person.drop('gesl', axis=1)

    ''' Results by age '''
    df_nb_trips_per_person_6_17 = df_nb_trips_per_person[df_nb_trips_per_person['alter'] <= 17]
    results_6_17 = get_weighted_avg_and_std(df_nb_trips_per_person_6_17, 'WP', percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_6_17 = results_6_17[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_6_17 = results_6_17[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_6_17 = results_6_17[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_6_17 = results_6_17[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_6_17 != 3.5149604553991214 or \
                        std_nb_trip_per_person_in_Switzerland_6_17 != 0.04295538788832046 or \
                        daily_dist_per_person_in_Switzerland_6_17 != 24.1918212260026 or \
                        std_daily_dist_per_person_in_Switzerland_6_17 != 0.926261640804652:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (6-17 years old only) in Switzerland:', nb_trip_per_person_in_Switzerland_6_17,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_6_17)

    df_nb_trips_per_person_18_24 = df_nb_trips_per_person[(df_nb_trips_per_person['alter'] <= 24) &
                                                          (df_nb_trips_per_person['alter'] >= 18)]
    results_18_24 = get_weighted_avg_and_std(df_nb_trips_per_person_18_24, 'WP', percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_18_24 = results_18_24[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_18_24 = results_18_24[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_18_24 = results_18_24[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_18_24 = results_18_24[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_18_24 != 3.521964247176923 or \
                        std_nb_trip_per_person_in_Switzerland_18_24 != 0.06046609291806194 or \
                        daily_dist_per_person_in_Switzerland_18_24 != 47.951383208875164 or \
                        std_daily_dist_per_person_in_Switzerland_18_24 != 1.7618363008240678:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (18-24 years old only) in Switzerland:', nb_trip_per_person_in_Switzerland_18_24,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_18_24)

    df_nb_trips_per_person_25_44 = df_nb_trips_per_person[(df_nb_trips_per_person['alter'] <= 44) &
                                                          (df_nb_trips_per_person['alter'] >= 25)]
    results_25_44 = get_weighted_avg_and_std(df_nb_trips_per_person_25_44, 'WP', percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_25_44 = results_25_44[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_25_44 = results_25_44[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_25_44 = results_25_44[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_25_44 = results_25_44[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_25_44 != 3.678900780592289 or \
                        std_nb_trip_per_person_in_Switzerland_25_44 != 0.03633596266469706 or \
                        daily_dist_per_person_in_Switzerland_25_44 != 44.90134048831685 or \
                        std_daily_dist_per_person_in_Switzerland_25_44 != 1.0008949738185364:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (25-44 years old only) in Switzerland:', nb_trip_per_person_in_Switzerland_25_44,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_25_44)

    df_nb_trips_per_person_45_64 = df_nb_trips_per_person[(df_nb_trips_per_person['alter'] <= 64) &
                                                          (df_nb_trips_per_person['alter'] >= 45)]
    results_45_64 = get_weighted_avg_and_std(df_nb_trips_per_person_45_64, 'WP', percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_45_64 = results_45_64[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_45_64 = results_45_64[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_45_64 = results_45_64[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_45_64 = results_45_64[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_45_64 != 3.4816046940077428 or \
                        std_nb_trip_per_person_in_Switzerland_45_64 != 0.031126415000797963 or \
                        daily_dist_per_person_in_Switzerland_45_64 != 39.69129212692978 or \
                        std_daily_dist_per_person_in_Switzerland_45_64 != 0.8319404038661198:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (45-64 years old only) in Switzerland:', nb_trip_per_person_in_Switzerland_45_64,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_45_64)

    df_nb_trips_per_person_65_79 = df_nb_trips_per_person[(df_nb_trips_per_person['alter'] <= 79) &
                                                          (df_nb_trips_per_person['alter'] >= 65)]
    results_65_79 = get_weighted_avg_and_std(df_nb_trips_per_person_65_79, 'WP', percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_65_79 = results_65_79[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_65_79 = results_65_79[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_65_79 = results_65_79[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_65_79 = results_65_79[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_65_79 != 2.7735456118285895 or \
                        std_nb_trip_per_person_in_Switzerland_65_79 != 0.04012988302440813 or \
                        daily_dist_per_person_in_Switzerland_65_79 != 27.18256242396237 or \
                        std_daily_dist_per_person_in_Switzerland_65_79 != 1.0253043007315443:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (65-79 years old only) in Switzerland:', nb_trip_per_person_in_Switzerland_65_79,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_65_79)

    df_nb_trips_per_person_80_plus = df_nb_trips_per_person[df_nb_trips_per_person['alter'] >= 80]
    results_80_plus = get_weighted_avg_and_std(df_nb_trips_per_person_80_plus, 'WP', percentage=False,
                                               list_of_columns=None)
    nb_trip_per_person_in_Switzerland_80_plus = results_80_plus[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_80_plus = results_80_plus[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_80_plus = results_80_plus[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_80_plus = results_80_plus[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_80_plus != 2.0438108174970484 or \
                        std_nb_trip_per_person_in_Switzerland_80_plus != 0.07178905831502098 or \
                        daily_dist_per_person_in_Switzerland_80_plus != 13.307696053973576 or \
                        std_daily_dist_per_person_in_Switzerland_80_plus != 1.6081042685253475:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (80+ years old only) in Switzerland:', nb_trip_per_person_in_Switzerland_80_plus,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_80_plus)

    df_nb_trips_per_person.drop('alter', axis=1)

    ''' Results by availability of a car '''
    df_nb_trips_per_person_always_available = df_nb_trips_per_person[df_nb_trips_per_person['f42100e'] == 1]
    results_always_available = get_weighted_avg_and_std(df_nb_trips_per_person_always_available, 'WP', percentage=False,
                                                        list_of_columns=None)
    nb_trip_per_person_in_Switzerland_always_available = results_always_available[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_always_available = results_always_available[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_always_available = results_always_available[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_always_available = results_always_available[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_always_available != 3.5417249096337113 or \
                        std_nb_trip_per_person_in_Switzerland_always_available != 0.023860396502259344 or \
                        daily_dist_per_person_in_Switzerland_always_available != 43.022560701958454 or \
                        std_daily_dist_per_person_in_Switzerland_always_available != 0.653919578872654:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (only people with a car always available) in Switzerland:',
    #       nb_trip_per_person_in_Switzerland_always_available,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_always_available)

    df_nb_trips_per_person_available_on_demand = df_nb_trips_per_person[df_nb_trips_per_person['f42100e'] == 2]
    results_available_on_demand = get_weighted_avg_and_std(df_nb_trips_per_person_available_on_demand, 'WP',
                                                           percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_available_on_demand = results_available_on_demand[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_available_on_demand = results_available_on_demand[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_available_on_demand = results_available_on_demand[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_available_on_demand = results_available_on_demand[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_available_on_demand != 3.4712662485673937 or \
                        std_nb_trip_per_person_in_Switzerland_available_on_demand != 0.05033597693586781 or \
                        daily_dist_per_person_in_Switzerland_available_on_demand != 40.43512883463786 or \
                        std_daily_dist_per_person_in_Switzerland_available_on_demand != 1.34510062679397:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (only people with a car available on demand) in Switzerland:',
    #       nb_trip_per_person_in_Switzerland_available_on_demand,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_available_on_demand)

    df_nb_trips_per_person_not_available = df_nb_trips_per_person[df_nb_trips_per_person['f42100e'] == 3]
    results_not_available = get_weighted_avg_and_std(df_nb_trips_per_person_not_available, 'WP',
                                                     percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_not_available = results_not_available[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_not_available = results_not_available[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_not_available = results_not_available[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_not_available = results_not_available[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_not_available != 2.928721066538652 or \
                        std_nb_trip_per_person_in_Switzerland_not_available != 0.07805688136609493 or \
                        daily_dist_per_person_in_Switzerland_not_available != 28.44167495488072 or \
                        std_daily_dist_per_person_in_Switzerland_not_available != 2.0314645291068527:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (only people with a no car available) in Switzerland:',
    #       nb_trip_per_person_in_Switzerland_not_available,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_not_available)

    ''' Results by day of the week '''
    df_nb_trips_per_person_saturday = df_nb_trips_per_person[df_nb_trips_per_person['tag'] == 6]
    results_saturday = get_weighted_avg_and_std(df_nb_trips_per_person_saturday, 'WP',
                                                percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_saturday = results_saturday[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_saturday = results_saturday[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_saturday = results_saturday[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_saturday = results_saturday[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_saturday != 3.1871486233633197 or \
                        std_nb_trip_per_person_in_Switzerland_saturday != 0.0483467665968927 or \
                        daily_dist_per_person_in_Switzerland_saturday != 39.5272524090048 or \
                        std_daily_dist_per_person_in_Switzerland_saturday != 1.4257334171308653:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (only on Saturday) in Switzerland:',
    #       nb_trip_per_person_in_Switzerland_saturday,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_saturday)

    df_nb_trips_per_person_sunday = df_nb_trips_per_person[df_nb_trips_per_person['tag'] == 7]
    results_sunday = get_weighted_avg_and_std(df_nb_trips_per_person_sunday, 'WP',
                                              percentage=False, list_of_columns=None)
    nb_trip_per_person_in_Switzerland_sunday = results_sunday[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_sunday = results_sunday[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_sunday = results_sunday[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_sunday = results_sunday[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_sunday != 2.0770673159518447 or \
                        std_nb_trip_per_person_in_Switzerland_sunday != 0.03157107383160285 or \
                        daily_dist_per_person_in_Switzerland_sunday != 34.52205065700436 or \
                        std_daily_dist_per_person_in_Switzerland_sunday != 1.1781923146003312:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (only on Sunday) in Switzerland:',
    #       nb_trip_per_person_in_Switzerland_sunday,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_sunday)

    df_nb_trips_per_person_monday_to_friday = df_nb_trips_per_person[df_nb_trips_per_person['tag'] <= 5]
    results_monday_to_friday = get_weighted_avg_and_std(df_nb_trips_per_person_monday_to_friday, 'WP',
                                                        percentage=False,
                                                        list_of_columns=None)
    nb_trip_per_person_in_Switzerland_monday_to_friday = results_monday_to_friday[0]['count_trips'][0]
    std_nb_trip_per_person_in_Switzerland_monday_to_friday = results_monday_to_friday[0]['count_trips'][1]
    daily_dist_per_person_in_Switzerland_monday_to_friday = results_monday_to_friday[0]['w_rdist'][0]
    std_daily_dist_per_person_in_Switzerland_monday_to_friday = results_monday_to_friday[0]['w_rdist'][1]
    if check_official_numbers:
        if nb_trip_per_person_in_Switzerland_monday_to_friday != 3.66593963090948 or \
                        std_nb_trip_per_person_in_Switzerland_monday_to_friday != 0.021049505685417687 or \
                        daily_dist_per_person_in_Switzerland_monday_to_friday != 36.76347714800342 or \
                        std_daily_dist_per_person_in_Switzerland_monday_to_friday != 0.5307394032061866:
            raise Exception('The official numbers (women) are not reproduced!')
    # print('Nb of trips per person (only between Monday and Friday) in Switzerland:',
    #       nb_trip_per_person_in_Switzerland_monday_to_friday,
    #       '+/-', std_nb_trip_per_person_in_Switzerland_monday_to_friday)
    df_output = pd.DataFrame([[nb_trip_per_person_in_Switzerland, std_nb_trip_per_person_in_Switzerland,
                               daily_dist_per_person_in_Switzerland, std_daily_dist_per_person_in_Switzerland],
                              [nb_trip_per_person_in_Switzerland_men, std_nb_trip_per_person_in_Switzerland_men,
                               daily_dist_per_person_in_Switzerland_men, std_daily_dist_per_person_in_Switzerland_men],
                              [nb_trip_per_person_in_Switzerland_women, std_nb_trip_per_person_in_Switzerland_women,
                               daily_dist_per_person_in_Switzerland_women,
                               std_daily_dist_per_person_in_Switzerland_women],
                              [nb_trip_per_person_in_Switzerland_6_17, std_nb_trip_per_person_in_Switzerland_6_17,
                               daily_dist_per_person_in_Switzerland_6_17,
                               std_daily_dist_per_person_in_Switzerland_6_17],
                              [nb_trip_per_person_in_Switzerland_18_24, std_nb_trip_per_person_in_Switzerland_18_24,
                               daily_dist_per_person_in_Switzerland_18_24,
                               std_daily_dist_per_person_in_Switzerland_18_24],
                              [nb_trip_per_person_in_Switzerland_25_44, std_nb_trip_per_person_in_Switzerland_25_44,
                               daily_dist_per_person_in_Switzerland_25_44,
                               std_daily_dist_per_person_in_Switzerland_25_44],
                              [nb_trip_per_person_in_Switzerland_45_64, std_nb_trip_per_person_in_Switzerland_45_64,
                               daily_dist_per_person_in_Switzerland_45_64,
                               std_daily_dist_per_person_in_Switzerland_45_64],
                              [nb_trip_per_person_in_Switzerland_65_79, std_nb_trip_per_person_in_Switzerland_65_79,
                               daily_dist_per_person_in_Switzerland_65_79,
                               std_daily_dist_per_person_in_Switzerland_65_79],
                              [nb_trip_per_person_in_Switzerland_80_plus,
                               std_nb_trip_per_person_in_Switzerland_80_plus,
                               daily_dist_per_person_in_Switzerland_80_plus,
                               std_daily_dist_per_person_in_Switzerland_80_plus],
                              [nb_trip_per_person_in_Switzerland_always_available,
                               std_nb_trip_per_person_in_Switzerland_always_available,
                               daily_dist_per_person_in_Switzerland_always_available,
                               std_daily_dist_per_person_in_Switzerland_always_available],
                              [nb_trip_per_person_in_Switzerland_available_on_demand,
                               std_nb_trip_per_person_in_Switzerland_available_on_demand,
                               daily_dist_per_person_in_Switzerland_available_on_demand,
                               std_daily_dist_per_person_in_Switzerland_available_on_demand],
                              [nb_trip_per_person_in_Switzerland_not_available,
                               std_nb_trip_per_person_in_Switzerland_not_available,
                               daily_dist_per_person_in_Switzerland_not_available,
                               std_daily_dist_per_person_in_Switzerland_not_available],
                              [nb_trip_per_person_in_Switzerland_monday_to_friday,
                               std_nb_trip_per_person_in_Switzerland_monday_to_friday,
                               daily_dist_per_person_in_Switzerland_monday_to_friday,
                               std_daily_dist_per_person_in_Switzerland_monday_to_friday],
                              [nb_trip_per_person_in_Switzerland_saturday,
                               std_nb_trip_per_person_in_Switzerland_saturday,
                               daily_dist_per_person_in_Switzerland_saturday,
                               std_daily_dist_per_person_in_Switzerland_saturday],
                              [nb_trip_per_person_in_Switzerland_sunday, std_nb_trip_per_person_in_Switzerland_sunday,
                               daily_dist_per_person_in_Switzerland_sunday,
                               std_daily_dist_per_person_in_Switzerland_sunday]],
                             index=['Total',
                                    'Hommes',
                                    'Femmes',
                                    '6-17 ans',
                                    '18-24 ans',
                                    '25-44 ans',
                                    '45-64 ans',
                                    '65-79 ans',
                                    '80 ans et plus',
                                    'Voiture toujours disponible',
                                    'Voiture disponible sur demande',
                                    'Voiture pas disponible',
                                    'Lundi à vendredi',
                                    'Samedi',
                                    'Dimanche'],
                             columns=['Nombre de déplacements', '+/-', 'Distance journalière, en km', '+/-'])
    return df_output


if __name__ == '__main__':
    run_nb_trips_by_public_transport()
