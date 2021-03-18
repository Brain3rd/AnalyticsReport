import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties


# Updated Data on COVID-19 (coronavirus) by Our World in Data
# url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'


# Read csv
DF = pd.read_csv('data/owid-covid-data.csv')


class CovidReport:
    def __init__(self, countries: list, days: int):
        self.days = days
        if self.days < 3:
            self.days = 3
        self.country = DF.loc[DF['iso_code'] == 'FIN']
        self.data = self.country.groupby('date').sum().reset_index().tail(self.days)
        self.country_list = countries
        self.file = f'CovidPast{self.days}d.pdf'

        # Make new pdf file
        with PdfPages(self.file) as export_pdf:
            # Loop through all columns
            for column in self.data.columns:
                if column != 'date':
                    for country in self.country_list:
                        # Select country
                        self.country = DF.loc[DF['iso_code'] == country]
                        # Organize data by date
                        data = self.country.groupby('date').sum().reset_index().tail(self.days)
                        # Plot data to graph
                        plt.plot(
                            data.date,
                            data[column],
                            label=country,
                            linewidth=1,
                            # linestyle='--',
                            # marker='.',
                            # markersize=3
                        )

                    # Add title
                    plt.title(
                        f'{column.title()} Past {self.days} Days',
                        fontdict={'fontname': 'Comic Sans MS',
                                  'fontsize': 16}
                    )
                    # Add label
                    plt.xlabel('Date')
                    plt.xticks(data.date[::round(self.days/4.1)])

                    # Legend settings
                    font = FontProperties()
                    font.set_size('xx-small')
                    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left', prop=font)

                    # Add page to pdf
                    export_pdf.savefig()

                    plt.close()


if __name__ == '__main__':

    choice_list = []

    all_countries = DF.iso_code.unique()
    print(f"Countries:\n{all_countries}\n")

    while True:
        country_choice = str(input(
            "Enter 1 country e.g. FIN or 'n' for no more: "
        )).upper()
        if country_choice == 'N':
            break
        elif country_choice in all_countries:
            choice_list.append(country_choice)
            print(f"Countries selected: {choice_list}")
        else:
            print(f"{country_choice} not in the list!")

    print(f"You selected {len(choice_list)} countries: {choice_list}")
    choice_days = int(input("Enter days(past) e.g. 7: "))
    covid_report = CovidReport(choice_list, choice_days)
    print(f"New {covid_report.file} created.")
