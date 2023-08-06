import csv

from termcolor import colored
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from epidemic.source import Predict

def train(predict_evidence, year):

    with open("./train.csv") as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        labels = []

        for row in reader:

            # 1 = True, 0 = False
            if row[2] == 'True':
                if row[0] == str(year):
                    return 1, 0, 1

                labels.append(1)
            else:
                labels.append(0)

            population = float(row[3])
            climate_change = float(row[4])
            democracy_index = float(row[5])
            poverty = float(row[6])
            global_health = float(row[7])
            flight = float(row[8])

            evidence.append([population, climate_change, democracy_index, poverty, global_health, flight])


    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=0.1
    )

    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)

    predictions = model.predict([predict_evidence])

    correct = round((y_test == predictions).sum() / len(y_test), 2)
    incorrect = round((y_test != predictions).sum() / len(y_test), 2)

    return correct, incorrect, predictions


def predict_virus(year):

    population = Predict(year).population()
    climate_change = Predict(year).climate_change()
    democracy_index = Predict(year).democracy_index()
    poverty = Predict(year).poverty()
    global_health = Predict(year).global_health_gdp_average()
    flight = Predict(year).flights()
    correct, incorrect, prediction = train([population, climate_change, democracy_index, poverty, global_health, flight], year)
    return correct, incorrect, prediction