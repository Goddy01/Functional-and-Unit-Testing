from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import project_detail, project_list, ProjectCreateView


class TestUrls(SimpleTestCase):

    def test_project_list_url_is_resolved(self):
        # Ensures that the list url directs exactly where it is supposed to
        url = reverse('list')
        self.assertEquals(resolve(url).func, project_list)

    def test_project_detail_url_is_resolved(self):
        # Ensures that the detail url directs exactly where it is supposed to
        url = reverse('detail', args=['some-args'])
        self.assertEquals(resolve(url).func, project_detail)

    def test_project_create_url_is_resolved(self):
        # Ensures that the add url directs exactly where it is supposed to
        url = reverse('add')
        self.assertEquals(resolve(url).func.view_class, ProjectCreateView)