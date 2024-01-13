from django.test import TestCase, TransactionTestCase

from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.utils.text import slugify

import grand_prix.models as gp_models
import race_organization.models as org_models


class GrandPrixModelTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@testing.com"
        )

        self.org = org_models.RaceOrganization.objects.create(
            name="Test Organization",
        )

        self.grandprix = gp_models.GrandPrix.objects.create(
            title="Test Grand Prix",
            description="This is a test grand prix",
            organization=self.org,
        )

        self.session_title = "Test Qualifying"
        self.racesession = gp_models.RaceSession.objects.create(
            event=self.grandprix,
            title=self.session_title,
        )

    def test_grand_prix_creation(self):
        """Test GrandPrix model creation"""
        gp_title = "Test Grand Prix"
        gp_title_slug = slugify(gp_title)

        # test creating a grand prix with the same slug and organization as the one created in the setup
        with self.assertRaises(IntegrityError):
            gp = gp_models.GrandPrix.objects.create(
                title=gp_title,
                description="This is a test grand prix",
                organization=self.org,
            )

        gp_title = "A New Test Grand Prix"
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

    def test_race_session_creation(self):
        """Test Session model creation"""
        # test creating a grand prix with the same slug and organization as the one created in the setup
        with self.assertRaises(IntegrityError):
            session = gp_models.RaceSession.objects.create(
                event=self.grandprix,
                title=self.session_title,
            )

        new_session_title = "Test Outlaw"

        session_title_slug = slugify(new_session_title)

        session = gp_models.RaceSession.objects.create(
            event=self.grandprix,
            title=new_session_title,
        )
        self.assertEqual(str(session), new_session_title)
        self.assertEqual(session.slug, session_title_slug)

    def test_session_heat_new_heats_increment_on_save(self):
        """Test that the heat number is incremented when a new heat is created"""
        number_of_heats = 5

        for i in range(number_of_heats):
            heat = gp_models.SessionHeat.objects.create(session=self.racesession)
            self.assertEqual(heat.heat_number, i + 1)

    def test_grand_prix_invitation(self):
        """Test GrandPrixInvitation model"""
        invitation = gp_models.GrandPrixInvitation.objects.create(
            grandprix=self.grandprix, code = "this is a test code"
        )

        self.assertEqual(invitation.code, "this is a test code")
        self.assertEqual(invitation.grandprix, self.grandprix)
        self.assertEqual(invitation.status, "active")

    def test_grand_prix(self):
        """Test GrandPrix model"""
        pass