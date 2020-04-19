import requests
from bs4 import BeautifulSoup as soup

class Course:

    def __init__(self, link, seat=0):
        self.link = link
        self.initialSeat = 0 if seat == None else seat

    def getLink(self):
        return self.link

    def setInitialSeat(self, seat):
        self.initialSeat = seat

    def hasAvailableSeats(self):
        response = self.get()
        numberOfSeats = self.parse(response)
        return self.initialSeat < int(numberOfSeats)

    def get(self):
        try:
            return requests.get(self.link)
        except Exception as e : 
            raise Exception('Unable to access link. Please check link provided.')

    # returns number of general seats in a corse
    def parse(self, response):
        try:
            page = soup(response.content, 'html.parser')
            result = page.find(string="General Seats Remaining:").find_next("td").get_text()
            return result
        except Exception as e :
            print("link provided does not have General Seats Remaining. Please provide a valid link ")
    



