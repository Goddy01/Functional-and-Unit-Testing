from django.test import SimpleTestCase
from budget.forms import ExpenseForm


class TestForms(SimpleTestCase):
    def test_expense_form_is_valid(self):
        form = ExpenseForm(data={
            'title': 'Devops-expense',
            'amount': 3000,
            'category': 'design&development'
        })

        self.assertTrue(form.is_valid())

    def test_expense_form_no_data(self):
        form = ExpenseForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2+1)