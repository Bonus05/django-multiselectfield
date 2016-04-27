from django.test import TestCase
from models import TestModelWithOptgroup
from models import TestModel
from models import TestValueTypeModel
from django.forms.models import modelform_factory

class MultiSelectFieldTest(TestCase):
    fixtures = ['fixtures.json']

    def test_single_select_on_db_field(self):
        TestModelForm = modelform_factory(TestModel)
        form = TestModelForm()
        model = TestModel()
        form = TestModelForm({"multivaluefield": [1,2]}, instance=model)
        self.assertTrue(form.is_valid(), msg=MultiSelectFieldTest.pretty_field_errors(form))
        self.assertEquals(model.multivaluefield, [u'1',u'2'])

    def test_single_select_on_db_field_with_optgroup(self):
        TestOptGroupModelForm = modelform_factory(TestModelWithOptgroup, fields=('optgroup_multivaluefield',))
        model = TestModelWithOptgroup()
        form = TestOptGroupModelForm({"optgroup_multivaluefield": [u'2',u'1']}, instance=model)
        self.assertTrue(form.is_valid(), msg=MultiSelectFieldTest.pretty_field_errors(form))

    def test_single_select_on_db_field_with_value_type(self):
        TestValueTypeModelForm = modelform_factory(TestValueTypeModel)
        form = TestValueTypeModelForm()
        model = TestValueTypeModel()
        form = TestValueTypeModelForm({"value_type_multivaluefield": [1,2]}, instance=model)
        self.assertTrue(form.is_valid(), msg=MultiSelectFieldTest.pretty_field_errors(form))
        self.assertEquals(model.value_type_multivaluefield, [1, 2])

    def test_load_fixture_multivaluefield_with_value_type(self):
        self.assertEquals(TestValueTypeModel.objects.count(), 1)
        model = TestValueTypeModel.objects.first()
        self.assertEquals(model.value_type_multivaluefield, [1, 2])

    def test_save_multivaluefield_with_value_type(self):
        model = TestValueTypeModel()
        model.value_type_multivaluefield = [1, 2]
        model.save()
        self.assertEquals(model.value_type_multivaluefield, [1, 2])

    def test_load_fixture_multivaluefield_with_empty_and_null(self):
        self.assertEquals(TestModel.objects.count(), 1)
        model = TestModel.objects.first()
        self.assertEquals(model.multivaluefield, [u"1", u"2"])
        self.assertEquals(model.blank_multivaluefield, [])
        self.assertEquals(model.null_multivaluefield, [])

    def test_save_multivaluefield_with_empty_and_null(self):
        model = TestModel()
        model.multivaluefield = ["1"]
        model.save()
        self.assertEquals(model.multivaluefield, [u"1"])
        self.assertEquals(model.blank_multivaluefield, [])
        self.assertEquals(model.null_multivaluefield, [])

    @staticmethod
    def pretty_field_errors(form):
        pretty_msg = "Validation errors: "
        for field in form:
            pretty_msg += "field %s with value %s says: %s.\n" % (field.name, field.value(), field.errors.as_text())
        return pretty_msg
