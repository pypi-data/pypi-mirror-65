"""Declares :class:`SuccessURLMixin`."""
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from django.utils.http import url_has_allowed_host_and_scheme


class SuccessURLMixin:
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url_allowed_hosts = set()
    next_page = None

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

    def get_default_next_page(self):
        return None

    def get_next_page(self):
        default_next_page = self.get_default_next_page()
        if self.next_page is not None:
            next_page = resolve_url(self.next_page)
        elif default_next_page:
            next_page = resolve_url(default_next_page)
        else:
            next_page = self.next_page

        if (self.redirect_field_name in self.request.POST or
                self.redirect_field_name in self.request.GET):
            next_page = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name)
            )
            url_is_safe = url_has_allowed_host_and_scheme(
                url=next_page,
                allowed_hosts=self.get_success_url_allowed_hosts(),
                require_https=self.request.is_secure(),
            )
            # Security check -- Ensure the user-originating redirection URL is
            # safe.
            if not url_is_safe:
                next_page = self.request.path
        return next_page
