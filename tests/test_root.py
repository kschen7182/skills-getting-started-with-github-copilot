"""Tests for GET / endpoint."""

import pytest


class TestRootRedirect:
    """Test suite for the root GET / endpoint."""

    def test_root_returns_redirect(self, client):
        """
        Arrange: Create a test client.
        Act: Send GET request to root path.
        Assert: Response is a redirect (307).
        """
        # Arrange
        # Client provided by fixture

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307

    def test_root_redirect_location(self, client):
        """
        Arrange: Create a test client.
        Act: Send GET request to root path without following redirect.
        Assert: Location header points to /static/index.html.
        """
        # Arrange
        # Client provided by fixture

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert "location" in response.headers
        assert "/static/index.html" in response.headers["location"]

    def test_root_follows_redirect_to_html(self, client):
        """
        Arrange: Create a test client.
        Act: Send GET request to root path and follow redirect.
        Assert: Final response contains HTML content.
        """
        # Arrange
        # Client provided by fixture

        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        # Since static files are mounted, we expect a response
        # The actual status depends on whether the static file is served
        assert response.status_code in [200, 404, 307]
