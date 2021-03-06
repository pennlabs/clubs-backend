import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from clubs.models import Advisor, Badge, Club, Event, Favorite, Membership, Note, Tag


class ClubTestCase(TestCase):
    def setUp(self):
        date = pytz.timezone("America/New_York").localize(datetime.datetime(2019, 1, 1))
        self.club1 = Club.objects.create(
            code="a", name="a", subtitle="a", founded=date, description="a", size=1
        )
        self.club2 = Club.objects.create(
            code="b", name="b", subtitle="b", founded=date, description="b", size=1
        )
        self.club2.parent_orgs.add(self.club1)

    def test_str(self):
        self.assertEqual(str(self.club1), self.club1.name)

    def test_parent_children(self):
        self.assertEqual(self.club2.parent_orgs.first(), self.club1)
        self.assertEqual(self.club1.children_orgs.first(), self.club2)


class ProfileTestCase(TestCase):
    def test_profile_creation(self):
        """
        Ensure that a Profile object is created when the user is created.
        """
        self.person = get_user_model().objects.create_user("test", "test@example.com", "test")
        self.assertTrue(self.person.profile)


class EventTestCase(TestCase):
    def setUp(self):
        date = pytz.timezone("America/New_York").localize(datetime.datetime(2019, 1, 1))
        self.club = Club.objects.create(
            code="a", name="a", subtitle="a", founded=date, description="a", size=1
        )
        self.event = Event.objects.create(
            name="a", club=self.club, start_time=date, end_time=date, description="a"
        )

    def test_str(self):
        self.assertEqual(str(self.event), self.event.name)


class FavoriteTestCase(TestCase):
    def setUp(self):
        date = pytz.timezone("America/New_York").localize(datetime.datetime(2019, 1, 1))
        self.person = get_user_model().objects.create_user("test", "test@example.com", "test")
        self.club = Club.objects.create(
            code="a", name="a", subtitle="a", founded=date, description="a", size=1
        )
        self.favorite = Favorite.objects.create(club=self.club, person=self.person)

    def test_str(self):
        self.assertTrue(str(self.favorite))


class MembershipTestCase(TestCase):
    def setUp(self):
        date = pytz.timezone("America/New_York").localize(datetime.datetime(2019, 1, 1))
        self.person = get_user_model().objects.create_user("test", "test@example.com", "test")
        self.club = Club.objects.create(
            code="a", name="a", subtitle="a", founded=date, description="a", size=1
        )
        self.membership = Membership.objects.create(club=self.club, person=self.person)

    def test_str(self):
        self.assertTrue(str(self.membership))


class TagTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="super interesting tag")

    def test_str(self):
        self.assertEqual(str(self.tag), self.tag.name)


class BadgeTestCase(TestCase):
    def setUp(self):
        self.badge = Badge.objects.create(label="SAC Funded", description="SAC Funded Club")

    def test_str(self):
        self.assertTrue(str(self.badge), self.badge.label)


class AdvisorTestCase(TestCase):
    def setUp(self):
        date = pytz.timezone("America/New_York").localize(datetime.datetime(2019, 1, 1))
        club = Club.objects.create(
            code="a", name="a", subtitle="a", founded=date, description="a", size=1
        )
        self.advisor = Advisor.objects.create(name="Eric Wang", phone="+12025550133", club=club)

    def test_str(self):
        self.assertEqual(str(self.advisor), self.advisor.name)


class NoteTestCase(TestCase):
    def setUp(self):
        date = pytz.timezone("America/New_York").localize(datetime.datetime(2019, 1, 1))
        self.person = get_user_model().objects.create_user("test", "test@example.com", "test")
        self.club1 = Club.objects.create(
            code="a", name="a", subtitle="a", founded=date, description="a", size=1
        )
        self.club2 = Club.objects.create(
            code="b", name="b", subtitle="b", founded=date, description="b", size=1
        )
        self.note1 = Note.objects.create(
            creator=self.person,
            creating_club=self.club1,
            subject_club=self.club2,
            title="Note1",
            content="content",
            creating_club_permission=10,
            outside_club_permission=0,
        )

    def test_club_relation(self):
        self.assertEqual(self.note1.creating_club, self.club1)
        self.assertEqual(self.note1, self.club1.note_by_club.first())
        self.assertEqual(self.note1.subject_club, self.club2)
        self.assertEqual(self.note1, self.club2.note_of_club.first())
