from datetime import datetime, timedelta
from covid19_stat.aditional_f import *
import numpy as np

np.seterr(divide='ignore', invalid='ignore')  # for ignor this: '--RuntimeWarning: invalid value encountered in longlong_scalars--'

class Global_info():
    # ------------------------------------
    def __init__(self):
        self.countries_population = pd.read_csv('https://raw.githubusercontent.com/Sergii-Lak/covid19-info-stats/master/covid19_stat/data_population.csv')

        self.confirmed_global = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        self.deaths_global = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
        self.recovered_global = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

        self.dispo_country_list = list_countries_dispo(self.confirmed_global)
        self.no_dispo_country_list = list_boat_counrties_NO_dispo_population_info(self.countries_population, self.confirmed_global)
        self.dates_list = dates_dispo_list(self.confirmed_global)

        self.date_update = datetime.date(datetime.now() - timedelta(days=1))
        self.date_now = datetime.date(datetime.now())

        self.recovered = 0
        self.death = 0
        self.confirmed = 0

    # --------------------------------------------------------------

    def country_infected_list(self):
        dispo_country_list = list(set(list_countries_dispo(self.confirmed_global)))
        return sorted(dispo_country_list)

    def date_valid_list(self):
        return dates_dispo_list(self.confirmed_global)

    def all_data_confirmed(self):
        return self.confirmed_global

    def all_data_death(self):
        return self.deaths_global

    def all_data_recovered(self):
        return self.recovered_global


    def date_data_confirmed_dict(self, date):
        if date not in self.dates_list:
            print('Date not valid!!!')
        else:
            return date_data_dict(date, dispo_country_list=self.dispo_country_list, confirmed_global=self.recovered_global)

    def date_data_death_dict(self, date):
        if date not in self.dates_list:
            print('Date not valid!!!')
        else:
            return date_data_dict(date, dispo_country_list=self.dispo_country_list, confirmed_global=self.deaths_global)

    def date_data_recovered_dict(self, date):
        if date not in self.dates_list:
            print('Date not valid!!!')
        else:
            return date_data_dict(date, dispo_country_list=self.dispo_country_list, confirmed_global=self.deaths_global)

    def all_data_in_date(self, date):
        if date not in self.dates_list:
            print('Date not valid!!!')
        else:
            return aii_dataframe(date, self.dispo_country_list, self.confirmed_global, self.deaths_global, self.recovered_global)


    def new_case_date_info(self, date):
        if date not in self.dates_list:
            print('Date not valid!!!')
        else:
            day_1 = aii_dataframe(date, self.dispo_country_list, self.confirmed_global, self.deaths_global, self.recovered_global)

            index_day1 = self.confirmed_global.columns.get_loc(date)
            if index_day1 == 4:
                index_date2 = 4
            else:
                index_date2 = index_day1 - 1

            date2=self.confirmed_global.columns[index_date2]
            day_2 = aii_dataframe(date2, self.dispo_country_list, self.confirmed_global, self.deaths_global, self.recovered_global)
            counrys = day_1['Country']
            confirmed_res = day_1['Confirmed']-day_2['Confirmed']
            death_res = day_1['Death']-day_2['Death']
            recovered_res = day_1['Recovered']-day_2['Recovered']
            return pd.DataFrame({'Countrys': list(counrys), 'New confirmed': list(confirmed_res), 'New Death': list(death_res), 'New Recovered': list(recovered_res)})


    def info_countrys(self, country, date):

        if country in self.no_dispo_country_list and date in self.dates_list:
            confirmed_final = info_confirmed(self.confirmed_global, self.confirmed, country, date)
            death_final = info_confirmed(self.deaths_global, self.death, country, date)
            recovered_final = info_confirmed(self.recovered_global, self.recovered, country, date)

            print()
            print('--------------------COVID-19 statistic----------------------')
            print()
            print('Contry: {} / In this date: {}'.format(country, date))
            print()
            print('TOTAL population in {} no informations or this is cruise ship'.format(country))
            print('Recovered: {}'.format(recovered_final))
            print('Confirmed: {}'.format(confirmed_final))
            print('Death: {}'.format(death_final))
            print('Existing: {}'.format((confirmed_final - (recovered_final + death_final))))

        elif country in self.dispo_country_list and date in self.dates_list:
            pop = (counry_pop_search(country, self.countries_population))

            confirmed_final = info_confirmed(self.confirmed_global, self.confirmed, country, date)
            death_final = info_confirmed(self.deaths_global, self.death, country, date)
            recovered_final = info_confirmed(self.recovered_global, self.recovered, country, date)

            print()
            print('--------------------COVID-19 statistic----------------------')
            print()
            print('Contry: {} / For this date: {}'.format(country, date))
            print()
            print('TOTAL population in {}: {}'.format(country, pop))
            print('Recovered: {}'.format(recovered_final))
            print('Confirmed: {}'.format(confirmed_final))
            print('Death: {}'.format(death_final))
            print('Existing: {}'.format((confirmed_final - (recovered_final + death_final))))
            print('The percentage infected and confirmed of total population: {}%'.format(
                percent_infected_in_counrie(confirmed_final, pop)))
            print('The percentage of deaths among infected people: {}%'.format(('%g' % (float(
                percent_infected_in_counrie(death_final,
                                            confirmed_final))))))  # rounding -  '%g'%(number) - removes all zeros after decimal point
            print('The percentage of recovered among infected people: {}%'.format(
                ('%g' % (float(percent_infected_in_counrie(recovered_final, confirmed_final))))))
            print('The percentage of existing among infected people: {}%'.format(('%g' % (
                float(percent_infected_in_counrie((confirmed_final - (recovered_final + death_final)),
                                                  confirmed_final))))))
        elif country in self.dispo_country_list or country in self.no_dispo_country_list and date not in self.dates_list:
            print('Date not valid!!!')
        elif country not in self.dispo_country_list or country not in self.no_dispo_country_list and date in self.dates_list:
            print('There is no such country!!!')
        else:
            print('You made a syntax error!!!!')

        print(start_date_infection_country(self.confirmed_global, country))

        # -----------------------------------------

if __name__ == "__main__":
    covid19 = Global_info()