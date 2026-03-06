import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import NoReverseMatch, reverse


def _reverse_first(*names, kwargs=None):
    for name in names:
        try:
            return reverse(name, kwargs=kwargs)
        except NoReverseMatch:
            continue
    pytest.skip(f"No matching URL name found in: {names}")


@pytest.mark.django_db
class TestBasicViews:
    def setup_method(self):
        self.client = Client()

    def test_home_page_responds(self):
        response = self.client.get("/")
        assert response.status_code in (200, 302)

    def test_admin_login_page_responds(self):
        response = self.client.get("/admin/login/")
        assert response.status_code in (200, 302)

    def test_admin_root_redirects_or_loads(self):
        response = self.client.get("/admin/")
        assert response.status_code in (200, 302)

    def test_unknown_url_is_not_500(self):
        response = self.client.get("/this-url-should-not-exist-12345/")
        assert response.status_code < 500

    def test_unknown_url_is_404_or_redirect(self):
        response = self.client.get("/this-url-should-not-exist-12345/")
        assert response.status_code in (404, 302)


@pytest.mark.django_db
class TestExtendedViews:
    def setup_method(self):
        self.client = Client()

    def test_named_home_route_responds(self):
        url = _reverse_first("booking:home", "home")
        response = self.client.get(url)
        assert response.status_code in (200, 302)

    def test_login_route_responds(self):
        url = _reverse_first("booking:login", "login", "user_login")
        response = self.client.get(url)
        assert response.status_code in (200, 302)

    def test_register_route_responds(self):
        url = _reverse_first("booking:register", "register")
        response = self.client.get(url)
        assert response.status_code in (200, 302)

    def test_service_list_accepts_search_query(self):
        url = _reverse_first("booking:service_list", "service_list")
        response = self.client.get(url, {"search": "test"})
        assert response.status_code < 500

    @pytest.mark.parametrize(
        "route_names",
        [
            ("booking:booking_list", "booking_list"),
            ("booking:create_booking", "create_booking"),
            ("booking:profile", "profile"),
            ("booking:logout", "logout", "user_logout"),
        ],
    )
    def test_protected_pages_redirect_for_anonymous(self, route_names):
        url = _reverse_first(*route_names)
        response = self.client.get(url)
        assert response.status_code in (302, 301)

    def test_login_then_logout_flow(self):
        login_url = _reverse_first("booking:login", "login", "user_login")
        logout_url = _reverse_first("booking:logout", "logout", "user_logout")

        User.objects.create_user(username="flow_user", password="pass12345")

        login_response = self.client.post(
            login_url,
            {"username": "flow_user", "password": "pass12345"},
        )
        assert login_response.status_code in (200, 302)
        assert self.client.session.get("_auth_user_id") is not None

        logout_response = self.client.get(logout_url)
        assert logout_response.status_code in (200, 302, 301)
        assert self.client.session.get("_auth_user_id") is None