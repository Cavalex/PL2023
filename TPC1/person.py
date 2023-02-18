class Person:
    def __init__(self, id, age, gender, tension, colesterol, beat, disease):
        self.id = id
        self.age = age
        self.gender = gender
        self.tension = tension
        self.colesterol = colesterol
        self.beat = beat
        self.disease = disease
    def __str__(self):
        return f"{self.id} is {self.age} years old, has {self.tension} tension, {self.colesterol} colesterol, {self.beat} beat and has a {self.disease} disease."
