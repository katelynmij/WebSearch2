#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #2
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
from pymongo import MongoClient
import string
def connectDataBase():

    # Create a database connection object using pymongo
    client = MongoClient("mongodb://localhost:27017/")
    collection = db["documents"]
    # --> add your Python code here

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary (document) to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here
    translating = str.maketrans('', '', string.punctuation)
    terms = docText.lower().translate(translating).split()

    # create a list of dictionaries (documents) with each entry including a term, its occurrences, and its num_chars. Ex: [{term, count, num_char}]
    # --> add your Python code here
    data = {}
    for term in terms:
        if term in data:
            data[term]["count"] +=  1
        else:
            data[term] = {
                "term": term,
                "count": 1,
                "num_chars": len(term)
            }
    list_of_terms = [{"term": m, "count":n["count"], "num_chars": n["num_chars"]} for m, n in data.items()]


    #Producing a final document as a dictionary including all the required fields
    # --> add your Python code here
    document = {
        "_id": docId,
        "text": docText,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "terms": list_of_terms
    }

    # Insert the document
    # --> add your Python code here
    col.insert_one(document)

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    result = col.delete_one({"_id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here
    deleteDocument(col, docId)
    # Create the document with the same id
    # --> add your Python code here
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3', ...}
    # We are simulating an inverted index here in memory.
    # --> add your Python code here
    inverted_index = {}
    documents = col.find()

    for doc in documents:
        title = doc['title']
        for term_entry in doc['terms']:
            term = term_entry['term']
            count = term_entry['count']

            if term in inverted_index:
                inverted_index[term] += f", {title}:{count}"
            else:
                inverted_index[term] = f"{title}:{count}"
            
    sorted_inverted_index = {k: inverted_index[k] for k in sorted(inverted_index)}
    return sorted_inverted_index