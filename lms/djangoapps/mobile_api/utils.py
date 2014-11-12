"""
Tests for video outline API
"""


from courseware import access
from student.roles import CourseBetaTesterRole
from student import auth

def should_allow_mobile_access(course, user):
    """
    Determines whether a user has access to a course in a mobile context.
    Checks if the course is marked as mobile_available or the user has extra permissions
    that gives them access anyway
    """

    # Implicitly includes instructor role via the following has_access check
    role = CourseBetaTesterRole(course.id)

    # The course doesn't always really exist -- we can have bad data in the enrollments
    # pointing to non-existent (or removed) courses, in which case `course` is None.
    return course and (course.mobile_available or auth.has_access(user, role) or access.has_access(user, 'staff', course))
