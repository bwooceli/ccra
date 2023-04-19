from django.test import TestCase

import grand_prix.models as gp_models
import race_organization.models as org_models

from django.contrib.auth.models import User

from django.utils.text import slugify

class GrandPrixModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="test@testing.com"
        )

        self.org = org_models.RaceOrganization.objects.create(
            name="Test Organization",
        )

    def test_grand_prix_creation(self):
        """Test GrandPrix model creation"""
        gp_title = "Test Grand Prix"
        gp_title_slug = slugify(gp_title)
        gp = gp_models.GrandPrix.objects.create(
            title=gp_title,
            description="This is a test grand prix",
            organization=self.org,
        )

        self.assertEqual(str(gp), gp_title)
        self.assertEqual(gp.description, "This is a test grand prix")
        self.assertEqual(gp.slug, gp_title_slug)
        self.assertEqual(gp.organization, self.org)
