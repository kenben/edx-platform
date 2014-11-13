"""
Unit tests for the EdxNotes app.
"""

import collections
from mock import patch
from unittest import skipUnless
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

from xmodule.tabs import EdxNotesTab
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.tests.factories import CourseFactory
from student.tests.factories import UserFactory
from . import helpers


@skipUnless(settings.FEATURES["ENABLE_EDXNOTES"], 'EdxNotes feature needs to be enabled.')
class EdxNotesHelpersTest(TestCase):
    """
    Tests for EdxNotes helpers.
    """
    def setUp(self):
        """
        Setup a dummy course-like object with a tabs field that can be
        accessed via attribute lookup.
        """
        self.course = collections.namedtuple("DummyCourse", ["tabs"])
        self.course.tabs = []

    def test_edxnotes_not_enabled(self):
        """
        Tests that edxnotes are disabled when the course tab configuration does NOT
        contain a tab with type "edxnotes."
        """
        self.assertFalse(helpers.edxnotes_enabled_for_course(self.course))

    def test_edxnotes_enabled(self):
        """
        Tests that edxnotes are enabled when the course tab configuration contains
        a tab with type "edxnotes."
        """
        self.course.tabs = [{"type": "foo"},
                            {"name": "Notes", "type": "edxnotes"},
                            {"type": "bar"}]

        self.assertTrue(helpers.edxnotes_enabled_for_course(self.course))

    def test_get_endpoint(self):
        """
        Tests that storage_url method returns correct values.
        """
        with patch.dict("django.conf.settings.EDXNOTES_INTERFACE", {"url": "http://example.com/"}):
            self.assertEqual("http://example.com/api/v1", helpers.get_endpoint())

        with patch.dict("django.conf.settings.EDXNOTES_INTERFACE", {"url": "http://example.com"}):
            self.assertEqual("http://example.com/api/v1", helpers.get_endpoint())

        with patch.dict("django.conf.settings.EDXNOTES_INTERFACE", {"url": "http://example.com"}):
            self.assertEqual("http://example.com/api/v1/some_path", helpers.get_endpoint("/some_path"))

        with patch.dict("django.conf.settings.EDXNOTES_INTERFACE", {"url": "http://example.com"}):
            self.assertEqual("http://example.com/api/v1/some_path", helpers.get_endpoint("some_path"))

        with patch.dict("django.conf.settings.EDXNOTES_INTERFACE", {"url": None}):
            self.assertRaises(ImproperlyConfigured, helpers.get_endpoint)


@skipUnless(settings.FEATURES["ENABLE_EDXNOTES"], 'EdxNotes feature needs to be enabled.')
class EdxNotesViewsTest(TestCase):
    """
    Tests for EdxNotes views.
    """
    def setUp(self):
        super(EdxNotesViewsTest, self).setUp()
        self.course = CourseFactory.create(edxnotes=True)
        self.user = UserFactory.create(username="Bob", email="bob@example.com", password="edx")
        self.client.login(username=self.user.username, password="edx")
        self.notes_page_url = reverse("edxnotes", args=[unicode(self.course.id)])

    @patch.dict("django.conf.settings.FEATURES", {"ENABLE_EDXNOTES": True})
    def test_edxnotes_view_is_enabled(self):
        """
        Tests that appropriate view is received if EdxNotes feature is enabled.
        """
        self.course.tabs.append(EdxNotesTab())
        modulestore().update_item(self.course, self.user.id)

        response = self.client.get(self.notes_page_url)
        self.assertContains("<h1>Notes</h1>", response.content)

    @patch.dict("django.conf.settings.FEATURES", {"ENABLE_EDXNOTES": False})
    def test_edxnotes_view_is_disabled(self):
        """
        Tests that 404 response is received if EdxNotes feature is disabled.
        """
        response = self.client.get(self.notes_page_url)
        self.assertEqual(404, response.status_code)
