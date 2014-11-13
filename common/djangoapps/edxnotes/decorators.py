"""
Decorators related to edXNotes.
"""
from edxnotes.helpers import (
    get_storage_url,
    get_token,
    generate_uid,
)
from edxmako.shortcuts import render_to_string
from django.conf import settings


def edxnotes(cls):
    """
    Decorator that makes components annotatable.
    """
    original_get_html = cls.get_html

    def get_html(self, *args, **kargs):
        """
        Returns raw html for the component.
        """
        # edXNotes must be disabled in Studio, returns original method in this case.
        if getattr(self.system, 'is_author_mode', False):
            return original_get_html(self, *args, **kargs)
        else:
            return render_to_string('edxnotes_wrapper.html', {
                'content': original_get_html(self, *args, **kargs),
                'uid': generate_uid(),
                'params': {
                    # Use camelCase to name keys.
                    'usageId': unicode(self.scope_ids.usage_id).encode('utf-8'),
                    'courseId': unicode(self.runtime.course_id).encode('utf-8'),
                    'token': get_token(),
                    'endpoint': get_storage_url(),
                    'debug': settings.DEBUG,
                },
            })

    cls.get_html = get_html
    return cls
