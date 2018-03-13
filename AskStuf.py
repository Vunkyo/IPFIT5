def ask():  # vraag naar gegevens
    print("Please fill in the form below.")

    ask.reseacher_name = input("Name of researcher: ")
    ask.case_nr = input("Case number: ")
    ask.evidence_nr = input("Evidence number: ")
    ask.unique_description = input("Unique description: ")
    ask.notes = input("Notes: ")
    print("")


# plaatst gegevens in een file. deze functie kan steeds opnieuw gebruikt worden om opnieuw te plaatsen in andere files
def save(filename):

    with open(filename, "a") as myfile:
        myfile.write("Name of researcher: %s" % ask.reseacher_name + "\n")
        myfile.write("Case number: %s" % ask.case_nr + "\n")
        myfile.write("Evidence number: %s" % ask.evidence_nr + "\n")
        myfile.write("Unique description: %s" % ask.unique_description + "\n")
        myfile.write("Notes: %s" % ask.notes + "\n")
        myfile.write("\n")
        # geeft aan dat hij de items niet kan vinden maar hij vind ze blijkbaar wel want het werkt
