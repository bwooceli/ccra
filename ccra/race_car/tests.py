from django.test import TestCase

import race_car.models as car_models
from django.contrib.auth.models import User


class TestRaceEvent(TestCase):
    def setUp(self):

        self.test_user = User.objects.create_user(
            username="test_user", password="test_password"
        )

        self.cars_for_test_race = [
            car_models.Car.objects.create(name="Scout Test Car 1"),
            car_models.Car.objects.create(name="Scout Test Car 2"),
            car_models.Car.objects.create(name="Scout Test Car 3"),
            car_models.Car.objects.create(name="Scout Test Car 4"),
            car_models.Car.objects.create(name="Scout Test Car 5"),
            car_models.Car.objects.create(name="Scout Test Car 6"),
            car_models.Car.objects.create(name="Scout Test Car 7"),
            car_models.Car.objects.create(name="Scout Test Car 8"),
            car_models.Car.objects.create(name="Outlaw Test Car 1"),
            car_models.Car.objects.create(name="Outlaw Test Car 2"),
            car_models.Car.objects.create(name="Outlaw Test Car 3"),
            car_models.Car.objects.create(name="Outlaw Test Car 4"),
        ]

        # self.event = car_models.RaceEvent.objects.create(title="Test Event")
        
        # self.race = car_models.Race.objects.create(title="Scouts")

    def test_car_names_return_correctly(self):
        for car in self.cars_for_test_race:
            self.assertEqual(car.name, str(car))

    def test_car_name_does_not_save_with_extra_spaces(self):
        car = car_models.Car.objects.create(name=" Test Car ")
        self.assertEqual(car.name, "Test Car")
    
    def test_save_car_maker_saves_correctly(self):
        first_name_with_spaces = " Anrew  "
        last_name_with_spaces = "  Livingston  "
        car_maker_child = car_models.CarMaker.objects.create(
            first_name=first_name_with_spaces,
            last_name=last_name_with_spaces,)
        first_name_without_spaces = first_name_with_spaces.strip()
        last_name_without_spaces = last_name_with_spaces.strip()


        self.assertEqual(car_maker_child.first_name, "Anrew")
        self.assertEqual(car_maker_child.last_name, "Livingston")

        self.assertEqual(f"{first_name_without_spaces} {last_name_without_spaces}", str(car_maker_child))

        car_maker_parent = car_models.CarMaker.objects.create(
            user = self.test_user
        )
        self.assertEqual(car_maker_parent.user.username, str(car_maker_parent))

        car_maker_child.helper = car_maker_parent
        car_maker_child.save()
        print(car_maker_child)
        self.assertEqual(f"{car_maker_child.first_name} {car_maker_child.last_name} (Helper: {self.test_user})", str(car_maker_child))

    def test_car_maker_save_raises_error_when_no_user_or_first_and_last_name(self):
        # assert that a validation error is raised when no user or first and last name are provided
        with self.assertRaises(ValueError):
            car_maker_fail = car_models.CarMaker.objects.create()


