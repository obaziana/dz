import random


class Student:
    def __init__(self, name="Максим"):
        self.name = name
        self.money = 100
        self.progress = 50
        self.gladness = 50
        self.alive = True

    def work(self):
        print(f"{self.name} пішов працювати.")
        self.money += 60
        self.progress -= 5
        self.gladness -= 10

    def study(self):
        print(f"{self.name} навчається.")
        self.progress += 15
        self.money -= 10
        self.gladness -= 5

    def chill(self):
        print(f"{self.name} відпочиває.")
        self.gladness += 20
        self.money -= 30
        self.progress -= 5


    def live_day(self, day):
        print(f"\n--- День {day} ---")
        print(f"Стан: Гроші = {self.money}$, Навчання = {self.progress}, Задоволення = {self.gladness}")

        if self.money < 30:
            self.work()
        elif self.progress < 30:
            self.study()
        elif self.gladness < 30:
            if self.money >= 30:
                self.chill()
            else:
                self.work()
        else:
            dice = random.randint(1, 3)
            if dice == 1:
                self.study()
            elif dice == 2:
                self.work()
            elif dice == 3:
                if self.money >= 30:
                    self.chill()
                else:
                    self.work()



student = Student("Максим")

for day in range(1, 366):
    if not student.alive:
        break
    student.live_day(day)

if student.alive:
    print("\nУра! Студент успішно прожив цілий рік!")