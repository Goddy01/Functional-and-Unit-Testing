from django.test import TestCase
from budget.models import Project, Category, Expense


class TestModels(TestCase):
    def setUp(self):
        # Creates a project instance that can be used functions in the class
        self.project1 = Project.objects.create(
            name='project 1',
            budget=10000
        )

    def test_project_is_assigned_slug_on_creation(self):
        # Ensures that a project is assigned a slug upon creation
        self.assertEquals(self.project1.slug, 'project-1')

    def test_budget_left(self):
        # Ensures that the calculation done by the budget_left method is correct
        category1 = Category.objects.create(
            project=self.project1,
            name = 'development'
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = category1
        )

        Expense.objects.create(
            project=self.project1,
            title = 'expense2',
            amount = 2000,
            category = category1
        )

        self.assertEquals(self.project1.budget_left, 7000)

    def test_total_transactions(self):
        # Ensures that the caluclation done by the total_transaction model is correct
        project2 = Project.objects.create(
            name='Project 2',
            budget = 20000
        )
        category1 = Category.objects.create(
            project=self.project1,
            name = 'development'
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = category1
        )

        Expense.objects.create(
            project = project2,
            title = 'expense2',
            amount = 2000,
            category = category1
        )

        self.assertEquals(project2.total_transactions, 1
        )

    # def test_absolute_url(self):
    #     print('THIS: ', self.project1.get_absolute_url)
    #     self.assertEquals(self.project1.get_absolute_url, '/project-1')