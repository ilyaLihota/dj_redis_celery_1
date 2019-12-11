from django.test import TestCase

from languages.models import Paradigm


class ParadigmTest(TestCase):
    """
    Test module for Paradigm model.
    """
    def setUp(self):
        Paradigm.objects.create(name='procedure')
        Paradigm.objects.create(name='object-oriented')
        Paradigm.objects.create(name='functional')

    def test_paradigm(self):
        procedure = Paradigm.objects.get(name='procedure')
        object_oriented = Paradigm.objects.get(name='object-oriented')
        functional = Paradigm.objects.get(name='functional')

        self.assertEqual(procedure.__str__(), 'procedure')
        self.assertEqual(object_oriented.__str__(), 'object-oriented')
        self.assertEqual(functional.__str__(), 'functional')
