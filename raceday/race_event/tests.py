from django.test import TestCase

import race_event.models as event_models


class TestRaceEvent(TestCase):
    def setUp(self):
        self.cars = [
            event_models.Car.objects.create(name="Scout Test Car 1"),
            event_models.Car.objects.create(name="Scout Test Car 2"),
            event_models.Car.objects.create(name="Scout Test Car 3"),
            event_models.Car.objects.create(name="Scout Test Car 4"),
            event_models.Car.objects.create(name="Outlaw Test Car 1"),
            event_models.Car.objects.create(name="Outlaw Test Car 2"),
            event_models.Car.objects.create(name="Outlaw Test Car 3"),
            event_models.Car.objects.create(name="Outlaw Test Car 4"),
        ]

        # self.event = event_models.RaceEvent.objects.create(title="Test Event")
        
        # self.race = event_models.Race.objects.create(title="Scouts")

    def test_car_names_return_correctly(self):
        for car in self.cars:
            self.assertEqual(car.name, str(car))