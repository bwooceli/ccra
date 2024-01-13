from django.test import TestCase

import race_organization.models as org_models
from django.contrib.auth.models import User


class TestRaceEventOrganization(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="test_user", password="test_password"
        )

        self.test_organization = org_models.RaceOrganization.objects.create(
            name="Test Organization"
        )

        self.test_parent_organization = org_models.RaceOrganization.objects.create(
            name="Test Parent Organization"
        )

        self.test_child_organization = org_models.RaceOrganization.objects.create(
            name="Test Child Organization",
            parent_organization=self.test_parent_organization,
        )

    def test_organization_name_returns_correctly(self):
        self.assertEqual(self.test_organization.name, str(self.test_organization))

    def test_organization_name_does_not_save_with_extra_spaces(self):
        self.test_organization.name = " Test Organization with Extra Spaces "
        self.test_organization.save()
        self.assertEqual(
            self.test_organization.name, "Test Organization with Extra Spaces"
        )
