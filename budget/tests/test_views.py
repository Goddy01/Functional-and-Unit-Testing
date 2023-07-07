from django.test import TestCase, Client
from budget.views import project_detail, project_list, ProjectCreateView
from django.urls import reverse
from budget.models import Project, Expense, Category
import json


class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.detail_url = reverse('detail', args=['project1'])
        self.list_url = reverse('list')
        self.add_url = reverse('add')
        self.project1 = Project.objects.create(
            name='project1',
            budget=10000
        )

    def test_project_list_GET(self):
        response = self.client.get(self.list_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')

    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    def test_project_detail_POST_add_new_expense(self):
        category = Category.objects.create(
            project=self.project1,
            name='design'
        )

        response = self.client.post(self.detail_url, {
            'project': self.project1,
            'title': 'frontend-expense',
            'amount': 2000,
            'category': Category.objects.all().first().name
            # print('FIRST:', Category.objects.all().first().name)
            # print('LAST:', Category.objects.all().last().name)
            # print('ITEM: ', Category.objects.get(id=1).name)
        })


        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.first().title, 'frontend-expense')

    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_an_expense(self):
        category = Category.objects.create(
            project=self.project1,
            name='development'
        )

        Expense.objects.create(
            project=self.project1,
            title='backend-expense',
            amount=5000,
            category=category
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id': 1
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.project1.expenses.count(), 0)


    def test_project_detail_DELETE_no_id(self):
         catgeory = Category.objects.create(
             project=self.project1,
             name='product-mgmt'
         )

         Expense.objects.create(
             project=self.project1,
             title='product-mgmt-expense',
             amount='4000',
             category=catgeory
         )

         response = self.client.delete(self.detail_url)

         self.assertEquals(response.status_code, 404)
         self.assertEquals(self.project1.expenses.count(), 1)


    def test_project_create_new_project_POST(self):
        categories = Category.objects.all()
        response = self.client.post(self.add_url, {
            'name': 'project2',
            'budget': 20000,
            'categoriesString': 'design,product-mgmt,development,product scaling'
        })
        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name, 'project2')

        category1 = Category.objects.get(id=1)
        self.assertEquals(category1.project, project2)
        self.assertEquals(category1.name, 'design')

        category2 = Category.objects.get(id=2)
        self.assertEquals(category2.project, project2)
        self.assertEquals(category2.name, 'product-mgmt')

        category4 = categories.last()
        self.assertEquals(category4.project, project2)
        self.assertEquals(category4.name, 'product scaling')
        self.assertEquals((*categories, ).index(category4), 3)