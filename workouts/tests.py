# workouts/tests.py

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from workouts.models import WorkoutPlan, WorkoutLog
from goals.models import FitnessGoal
from django.urls import reverse
import datetime

User = get_user_model()

class WorkoutsAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Create a fitness goal for testing the GPT plan generator
        self.fitness_goal = FitnessGoal.objects.create(
            user=self.user,
            description="Lose weight",
            target_metric="10 lbs",
            target_date=datetime.date.today() + datetime.timedelta(days=30)
        )
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

    def test_view_workout_plan_generation(self):
        response = self.client.get(reverse("workouts:view_plan"))
        self.assertEqual(response.status_code, 200)
        # Verify that a plan has been generated and rendered
        self.assertContains(response, "Your Workout Plan")

    def test_log_workout(self):
        workout_data = {
            "date": "2025-04-10",
            "exercise": "Push Ups",
            "sets": 3,
            "reps": 12,
            "notes": "Felt great!"
        }
        response = self.client.post(reverse("workouts:log_workout"), workout_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after posting
        self.assertEqual(WorkoutLog.objects.filter(user=self.user).count(), 1)

    def test_exercise_list(self):
        response = self.client.get(reverse("workouts:exercise_list"))
        self.assertEqual(response.status_code, 200)
