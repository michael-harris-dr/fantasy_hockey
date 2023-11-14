#associates an ID number with the name of a team (e.g. "1" and "New Jersey Devils")
class IDTeam:
    def __init__(self, id, team):
        self.id = id
        self.team = team

    def __str__(self):
        return f"{self.id} -> {self.team}"
    
class Player:
    def __init__(self, id):
        self.id = id
        

class Team:
    def __init__(self, city, name, id, code):
        self.city = city
        self.name = name
        self.id = id
        self.code = code