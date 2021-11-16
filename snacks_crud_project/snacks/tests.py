from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

        self.Snack = Snack.objects.create(
            title="Yogurt",
            description="Yogurt is delicious",
            purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.Snack), "Yogurt")

    def test_Snack_content(self):
        self.assertEqual(f"{self.Snack.title}", "Yogurt")
        self.assertEqual(f"{self.Snack.description}", "Yogurt is delicious")
        self.assertEqual(f"{self.Snack.purchaser}", "tester")

    def test_Snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yogurt")
        self.assertTemplateUsed(response, "snack_list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_Snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, f"{self.Snack.description}")
        self.assertTemplateUsed(response, "snack_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_Snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "White rice",
                "description": " Rice is full of starches",
                "purchaser": self.user.pk,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Details about  White rice")
        self.assertTemplateUsed(response, "snack_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {
                "title": "Updated Yogurt",
                "description": "Yogurt is not delicious",
                "purchaser": self.user.id,
            },
        )
        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)
