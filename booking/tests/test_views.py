import pytest
from django.test import Client


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