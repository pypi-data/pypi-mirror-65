import pandas as pd

def checking_max(a):
    return a.shape[0]

def counry_pop_search(country, countries_population):
    res = 0
    for i in range(0, checking_max(countries_population)):
        if countries_population.loc[i][1] == country:
            res = int(str(countries_population.loc[i][2]).replace('.', ''))
            break
    return res

def list_boat_counrties_NO_dispo_population_info(countries_population, confirmed_global):
    countries_people_data = countries_population['name']
    countries_covid = confirmed_global['Country/Region']
    c_data = list(set(countries_people_data))
    c_check = list(set(countries_covid))
    no_dispo_list = []
    for i in c_check:
        if i not in c_data:
            no_dispo_list.append(i)
    return no_dispo_list

def list_countries_dispo(confirmed_global):
    countries_dispo = []
    for i in range(0, checking_max(confirmed_global)):
        countries_dispo.append(confirmed_global.loc[i][1])
    return countries_dispo


def info_confirmed(df_info, result, country, date):
    for i in range(0, checking_max(df_info)):
        if df_info.loc[i][1] == country:
            result += df_info.loc[i][date]
    return result

def percent_infected_in_counrie(number_infected_confirmed, population):
    if number_infected_confirmed == 0:
        return 0
    else:
        percent_infected = format(((number_infected_confirmed / population) * 100), '.10f')  # rounding, 10 numbers after decimal point
        if percent_infected == 0:
            return 0
        else:
            return percent_infected


def dates_dispo_list(df):
    return list(df.columns[4:len(df.columns)])


def start_date_infection_country(confirmed_global, country):
    list_countrys = list_countries_dispo(confirmed_global)
    res = ''
    data_searche_country = confirmed_global['Country/Region'] == country
    data_country = confirmed_global[data_searche_country]
    for i in list(data_country.columns[4:len(data_country.columns)]):
        if country not in list_countrys:
            res = 'There is no such country or you made a syntax error!!!!'
        elif country == 'China':
            res = 'End of December 2019...'
            break
        elif sum(data_country[i]) > 0:
            res = 'Date when the virus started spreading in {} is: {}'.format(country, i)
            break
    return res

def date_data_dict(date, dispo_country_list, confirmed_global):
    date_info_dict = {}
    for country in list(set(dispo_country_list)):
        data_searche_country = confirmed_global['Country/Region'] == country
        data_country = confirmed_global[data_searche_country]
        date_column = sum(data_country[date])
        date_info_dict[country]= int(date_column)
    return date_info_dict

def aii_dataframe(date, dispo_country_list, confirmed_global, deaths_global, recovered_global):
    res = {}
    confirmed = date_data_dict(date, dispo_country_list, confirmed_global).values()
    death = date_data_dict(date, dispo_country_list, deaths_global).values()
    recovered = date_data_dict(date, dispo_country_list, recovered_global).values()
    countryes = date_data_dict(date, dispo_country_list, confirmed_global).keys()
    res['Country'] = list(countryes)
    res['Confirmed'] = list(confirmed)
    res['Death'] = list(death)
    res['Recovered'] = list(recovered)
    return pd.DataFrame(res).sort_values('Country')