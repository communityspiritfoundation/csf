from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Mileage
from ..users.models import User
from ..team.models import Team
from .serializers import MileageSerializer

from freezegun import freeze_time
import datetime


class MileageTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.mileage = Mileage.objects.create(user=self.user, kilometres=100.0)

    def test_get_mileage(self):
        url = reverse('mileage:get-mileage', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = MileageSerializer([self.mileage], many=True)
        self.assertEqual(response.data, serializer.data)

    def test_post_mileage(self):
        url = reverse('mileage:post-mileage')

        data = {'user': self.user.id, 'kilometres': 200.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        twos_days_ago = datetime.date.today() - datetime.timedelta(days=2)
        data = {'user': self.user.id, 'kilometres': 200.0, 'date': twos_days_ago}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Mileage.objects.count(), 3)

    def test_post_mileage_invalid_data(self):
        url = reverse('mileage:post-mileage')

        data = {'user': self.user.id}  # Missing 'kilometres' field
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        twos_days_time = datetime.date.today() + datetime.timedelta(days=2)
        data = {'user': self.user.id, 'kilometres': 20, 'date': twos_days_time}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Mileage.objects.count(), 1)

    # test challenge periods

    def test_start_challenge(self):
        url = reverse('mileage:post-mileage')
        data = {'user': self.user.id, 'kilometres': 200.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # refresh user
        self.user = User.objects.get(id=self.user.id)
        self.assertEqual(self.user.challenge_start_date, datetime.date.today())

    def test_get_challenge_mileages(self):
        url = reverse('mileage:post-mileage')

        # start challenge period
        data = {'user': self.user.id, 'kilometres': 200.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # post mileage before the challenge period
        twos_days_ago = datetime.date.today() - datetime.timedelta(days=2)
        data = {'user': self.user.id, 'kilometres': 200.0, 'date': twos_days_ago}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test only get mileages within challenge period if challenge param in query
        url = reverse('mileage:get-mileage', args=[self.user.id])
        response = self.client.get(url, {'challenge': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

    def test_rollover_challenge(self):
        url = reverse('mileage:post-mileage')

        # start challenge period
        data = {'user': self.user.id, 'kilometres': 200.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # simulate the future and rollover to next challenge period
        self._test_rollover_challenge()

    @freeze_time(datetime.date.today() + datetime.timedelta(days=15))
    def _test_rollover_challenge(self):

        # get mileages after challenge period has ended
        url = reverse('mileage:get-mileage', args=[self.user.id])
        response = self.client.get(url, {'challenge': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        url = reverse('mileage:post-mileage')
        data = {'user': self.user.id, 'kilometres': 5.5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test only gets mileage in new challenge period
        url = reverse('mileage:get-mileage', args=[self.user.id])
        response = self.client.get(url, {'challenge': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

        # refresh user
        self.user = User.objects.get(id=self.user.id)
        self.assertEqual(self.user.challenge_start_date, datetime.date.today())

    def test_leaderboard(self):
        team1 = Team.objects.create(name="team1", bio="we are team 1")
        team2 = Team.objects.create(name="team2", bio="we are team 2")
        user1 = User.objects.create(username='user1', email="user1@eample.com", team_id=team1)
        user2 = User.objects.create(username='user2', email="user2@eample.com", team_id=team1)
        user3 = User.objects.create(username='user3', email="user3@eample.com", team_id=team2)

        # test that total_mileage is initialised to 0
        self.assertEquals(self.user.total_mileage, 0)
        self.assertEquals(user1.total_mileage, 0)
        self.assertEquals(team1.total_mileage, 0)

        url = reverse('mileage:post-mileage')
        self.client.post(url, {'user': user1.id, 'kilometres': 5.0}, format='json')
        self.client.post(url, {'user': user2.id, 'kilometres': 4.0}, format='json')
        self.client.post(url, {'user': user3.id, 'kilometres': 4.0}, format='json')
        self.client.post(url, {'user': user3.id, 'kilometres': 2.0}, format='json')

        # test the user leaderboard
        response = self.client.get(reverse('mileage:get-leaderboard'), {'type': 'users'}, format='json')
        self.assertEquals(response.data, [{'username': 'testuser', 'total_mileage': 100.0},
                                          {'username': 'user3', 'total_mileage': 6.0},
                                          {'username': 'user1', 'total_mileage': 5.0},
                                          {'username': 'user2', 'total_mileage': 4.0}])
        response = self.client.get(reverse('mileage:get-leaderboard'), {'type': 'users'}, format='json')

        # test the team leaderboard
        response = self.client.get(reverse('mileage:get-leaderboard'), {'type': 'team'}, format='json')
        self.assertEquals(response.data, [{'name': 'team1', 'bio': 'we are team 1', 'total_mileage': 9.0},
                                          {'name': 'team2', 'bio': 'we are team 2', 'total_mileage': 6.0}])
