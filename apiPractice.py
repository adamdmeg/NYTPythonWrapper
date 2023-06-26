import requests

# raises an exception if key is wrong
class APIKeyException(Exception):
    def __init__(self, message): self.message = message

#raises an exception if query is wrong
class InvalidQueryException(Exception):
    def __init__(self,message): self.message = message

# class for api object to store all methods and such
class ReviewAPI(object):
    # initializes api object
    def __init__(self, key=None):
        self.key = key
        # where the query is coming from. {} replaces date and key
        self.root = 'https://api.nytimes.com/svc/books/v3/lists/overview/{}.json?api-key={}'
        # if there is no key, raises an error
        if not self.key:
            nyt_dev_page = 'http://developer.nytimes.com/docs/reference/keys'
            exception_str = 'Warning: API Key required. Please visit {}'
            raise APIKeyException(exception_str.format(nyt_dev_page))
    # initializes a query object, taking in a date and api key because that is what is needed
    def query(self, date=None, key=None):
        if not key:
            key = self.key
        # makes url request
        url = self.root.format(date, key)
        # gets data from internet
        r = requests.get(url)
        # returns information in json format
        return r.json()
# where to put api key
api_key = 'YOUR_API_KEY'
# creates api object using key
review_api = ReviewAPI(key=api_key)
# creates a query using api key and desired date
response = review_api.query(date='2023-06-15')

# if response is OK == everything is working:
if response["status"] == "OK":
    # grabs the lists array from results
    lists = response["results"]["lists"]
    # for each list in the lists array:
    for l in lists:
        list_name = l["display_name"]
        # grabs the array of books in that list
        books = l["books"]
        # creates a dictionary for each list with the title being the list name and the content being a list of books
        list_data = {
            "list_name": list_name,
            "books": []
        }
        # for each book in the books list of that specific list:
        for book in books:
            title = book["title"]
            author = book["author"]
            description = book["description"]
            book_image = book["book_image"]

            # creates a dictionary for the specific book of all of its details
            book_data = {
                "title": title,
                "author": author,
                "description": description,
                "book_image": book_image
            }

            list_data["books"].append(book_data)

        print(list_data)
        print("\n")
else:
    print("Error in API response")