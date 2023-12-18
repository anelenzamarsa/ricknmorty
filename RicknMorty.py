import requests
import csv
from tabulate import tabulate




def initialRequest(name):
    query = requests.get(url=f"https://rickandmortyapi.com/api/character/?name={name}")
    return query.json()



def showResults(output):
    next = output['info']['next']
    saveToFile(request_output=output) ## save to file the initial request
    page = 2

    while next is not None: # pagination
        sub_query = requests.get(url=next) #do API call for the rest of pages
        sub_output = sub_query.json()
        saveToFile(request_output=sub_query.json())

        next = sub_output['info']['next']
        page += 1

    with open('data.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        data = list(csvreader)

    # Print the CSV data in a tabular format
    print(tabulate(data, headers='firstrow', tablefmt='grid'))



def getEpisode(endpoint):
    call = requests.get(endpoint)
    result = call.json()
    return f"{result['name']}-({result['episode']})"






def saveToFile(request_output):
    results = request_output['results'] # all characters in list as list


    with open('data.csv', mode='a', newline='') as character_file: ## populating table
        writer = csv.writer(character_file)


        for character in results:

            type = "-"
            if character['type'] != "":
                type = character['type']  ## in case type is None just add - to have a better seperation in lines

            episodes = ", ".join([ getEpisode(e) for e in character['episode'] ]) ## Join in String All episode name-shortcut

            row = [character['id'], character['name'], character['status'], character['species'], type, character['gender'], character['origin']['name'],character['location']['name'], episodes ] # row to be inserted
            writer.writerow(row)



def workflow(name):
    with open('data.csv', mode='w') as file:
        file.flush() ## Truncating table
        column_names = ['ID', 'Name', 'Status', 'Species', 'Type', 'Gender', 'Origin', 'Location', 'Episodes'] # write headers
        writer = csv.writer(file)
        writer.writerow(column_names)


    showResults(initialRequest(name=name))




if __name__ == '__main__':
    param = input("Let's find your Rick n Morty Character!!!\n" + "Please enter the characters name: ")
    print(workflow(param))

