from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from .. import views

from django.test import RequestFactory
import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestFavoritesView:
    def test_if_view_favorites_is_displaying_when_not_logged_in(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()

        resp = views.favorites(req)

        assert resp.status_code == 200, \
            'Is callable by guests'
        assert "Suivez ce lien pour vous connecter." in str(resp.getvalue()), \
            'Is returning a False boolean called empty for the template to display, when not logged in, ' \
            'an invitation to log in'

    def test_if_view_favorites_is_displaying_when_logged_in_with_no_favorites_yet_for_this_user(self):
        user = mixer.blend('auth.User', id=2)
        mixer.blend('favorites.Favorites', user_id=3)
        req = RequestFactory().get('/')
        req.user = user

        resp = views.favorites(req)

        assert resp.status_code == 200, \
            'Is callable by logged-in user with no prior favorites'
        assert "Aucuns substituts" in str(resp.getvalue()), \
            'Is returning a False boolean called empty for the template to display, when logged in,' \
            ' a text saying there are no substitutes yet'

    def test_if_view_favorites_is_displaying_previous_favorites_when_logged_in(self):
        user = mixer.blend('auth.User', id=2)
        mixer.blend('favorites.Favorites', user_id=2)
        req = RequestFactory().get('/')
        req.user = user

        resp = views.favorites(req)

        assert resp.status_code == 200, 'Is callable by logged-in user with prior favorites'
        assert "Voici la liste de vos aliments" in str(resp.getvalue()), \
            'Is returning a True boolean called empty for the template to display the previous favorites'

    def test_if_view_favorites_is_saving_favorites_when_logged_in(self):
        objproduct_initial = mixer.blend('products.Product')
        objproduct_substitute = mixer.blend('products.Product')
        user = mixer.blend('auth.User')
        post = {
            "user_id": user.id,
            "product": objproduct_initial.code,
            "substitute": objproduct_substitute.code
        }
        req = RequestFactory().post('/', data=post)
        req.user = user
        resp = views.favorites(req)

        assert resp.status_code == 200, \
            'Should save a new entry in favorites database'
        assert str(post['product']) and str(post['substitute']) in str(resp.getvalue()), \
            'Should display the newly saved product on the favorites page'

    def test_if_view_favorites_is_preventing_saving_duplicates_in_favorites_when_logged_in(self):
        objproduct_initial = mixer.blend('products.Product')
        objproduct_substitute = mixer.blend('products.Product')
        mixer.blend(
            'favorites.Favorites',
            user_id=2,
            product_id=objproduct_initial.code,
            substitute_id=objproduct_substitute.code)

        user = mixer.blend('auth.User', id=2)
        post = {
            "user_id": user.id,
            "product": objproduct_initial.code,
            "substitute": objproduct_substitute.code
        }
        req = RequestFactory().post('/', data=post)
        req.user = user
        resp = views._add_favorites(req)

        assert resp is True, 'Should return True for the boolean called "already exists"'
