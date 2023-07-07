from django.test import SimpleTestCase
from budget.forms import ExpenseForm


class TestForms(SimpleTestCase):
    def test_expense_form_is_valid(self):
        # Enusres that the form is valid when the right data are passed to the ExpensFform
        form = ExpenseForm(data={
            'title': 'Devops-expense',
            'amount': 3000,
            'category': 'design&development'
        })

        self.assertTrue(form.is_valid())

    def test_expense_form_no_data(self):
        # Ensures that the form is not valid when no data is passed
        form = ExpenseForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2+1)