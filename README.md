# Number of trips by public transport in Switzerland
This code computes the number of trips in Switzerland by public transport by type of season tickets owned.

## What is exactly available
The following variables are available (incl. the confidence interval):
- All transport modes
  - Number of trips
  - Daily distance (in km)
- By public transport
  - Number of trips
  - Daily distance (in km)
- By public transport by people owning a general abonnement (GA travelcard)
  - Numnber of trips
  - Daily distance (in km)
- By public transport by people owning a first class general abonnement (GA travelcard)
  - Numnber of trips
  - Daily distance (in km)
- By public transport by people owning a second class general abonnement (GA travelcard)
  - Numnber of trips
  - Daily distance (in km)
- By public transport by people owning a half fare travelcard
  - Numnber of trips
  - Daily distance (in km)
- By public transport by people owning a regional fare network travelcard
  - Numnber of trips
  - Daily distance (in km)
- By public transport by people owning a regional fare network travelcard and a half fare travelcard
  - Numnber of trips
  - Daily distance (in km)
  
These results are available for the general population. They are also differentiated by:
- Gender
- Age (6-17, 18-24, 25-44, 45-64, 65-79, 80+)
- Car availability (always, on demand, never)
- Day of the week (monday to friday, saturday, sunday)

## Results
The results can be found in the CSV file <a href="https://github.com/antonindanalet/nb-trips-by-public-transport-in-Switzerland/blob/master/data/output/nb_trips_per_person.csv">nb_trips_per_person.csv</a> in `data/output/`.

## Getting started
These instructions will get you a copy of the code up and running on your local machine for reproducing the result and understanding how it has been generated.

### Prerequisites
To run the code itself, you need python 3, pandas and numpy.
For it to produce the results, you also need the raw data of the Transport and Mobility Microcensus 2015, not included on GitHub. These data are individual data and therefore not open. You can however get them by filling in this form in <a href="https://www.are.admin.ch/are/de/home/verkehr-und-infrastruktur/grundlagen-und-daten/mzmv/datenzugang.html">German</a>, <a href="https://www.are.admin.ch/are/fr/home/mobilite/bases-et-donnees/mrmt/accesauxdonnees.html">French</a> or <a href="https://www.are.admin.ch/are/it/home/mobilita/basi-e-dati/mcmt/accessoaidati.html">Italian</a>. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code
Please copy the files `wegeinland.csv` and `zielpersonen.csv` from 2015 that you receive from the Swiss Federal Statistical Office (FSO) in the folders "<a href="https://github.com/antonindanalet/nb-trips-by-public-transport-in-Switzerland/tree/master/data/input">data/input</a>". Then run <a href="https://github.com/antonindanalet/nb-trips-by-public-transport-in-Switzerland/blob/master/src/run_nb_trips_by_public_transport.py">run_availability_of_parking.py</a>.

DO NOT commit or share in any way these two CSV-files! These are personal data.

### Contact
Please don't hesitate to contact me if you have questions or comments about this code: antonin.danalet@are.admin.ch
