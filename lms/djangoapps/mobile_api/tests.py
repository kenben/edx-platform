"""
Tests for mobile API utilities
"""

import ddt

from courseware.tests.factories import UserFactory

from rest_framework.test import APITestCase

from student import auth

from mobile_api.utils import should_allow_mobile_access

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

ROLE_CASES = (
        (auth.CourseBetaTesterRole, True),
        (auth.CourseStaffRole, True),
        (auth.CourseInstructorRole, True),
        (None, False)
)

@ddt.ddt
class TestMobileApiUtils(ModuleStoreTestCase, APITestCase):
    """
    Tests for mobile API utilities
    """
    @ddt.data(*ROLE_CASES)
    @ddt.unpack
    def test_mobile_role_access(self, role, should_have_access):
        """
        Verifies that our mobile access function properly handles using roles to grant access
        """
        user = UserFactory.create()
        course = CourseFactory.create(mobile_available=False)
        if role:
            role(course.id).add_users(user)
        self.assertEqual(should_have_access, should_allow_mobile_access(course, user))

    def test_mobile_explicit_access(self):
        """
        Verifies that our mobile access function listens to the mobile_available flag as it should
        """
        user = UserFactory.create()
        course = CourseFactory.create(mobile_available=True)
        self.assertTrue(should_allow_mobile_access(course, user))
