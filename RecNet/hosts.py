from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'api-dev', "RecNet.apiUrls", name='api-dev'),
    host(r'cdn-dev', "RecNet.cdnUrls", name='cdn-dev'),
    host(r'admin-dev', "RecNet.adminUrls", name='admin-dev'),
    host(r'email-dev', "RecNet.emailurls", name='email-dev'),
)