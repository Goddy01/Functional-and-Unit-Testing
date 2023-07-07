import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from budget.models import Project, Expense, Category


class TestProjectListPage(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.close()

    def test_no_project_page_is_displayed(self):
        # When user has no project
        self.browser.get(self.live_server_url)
        # time.sleep(30)
        alertParent = self.browser.find_element(By.CLASS_NAME, 'noproject-wrapper')
        alertMessage = alertParent.find_element(By.TAG_NAME, 'h3')

        self.assertEquals(alertMessage.text, "Sorry, you don't have any projects, yet.")

    def test_no_project_buttons_redirects_to_add_page(self):
        self.browser.get(self.live_server_url)

        add_url = self.live_server_url + reverse('add')
        alertParent = self.browser.find_element(By.CLASS_NAME, 'noproject-wrapper')
        alertParent.find_element(By.TAG_NAME, 'a').click()

        self.assertEquals(self.browser.current_url, add_url)

    def test_user_sees_project_list(self):
        project = Project.objects.create(
            name='project1',
            budget=10000
        )
        self.browser.get(self.live_server_url)
        parentClass = self.browser.find_element(By.CLASS_NAME, 'card-panel')
        text = parentClass.find_element(By.TAG_NAME, 'h5').text

        self.assertEquals(text, 'project1')

    def test_user_is_redirected_to_project_detail_page(self):
        project = Project.objects.create(
            name='project1',
            budget=20000
        )

        self.browser.get(self.live_server_url)
        detail_url = self.live_server_url + reverse('detail', args=[project.slug])
        parentClass = self.browser.find_element(By.CLASS_NAME, 'card-panel')
        parentClass.find_element(By.TAG_NAME, 'a').click()

        self.assertEquals(self.browser.current_url, detail_url)