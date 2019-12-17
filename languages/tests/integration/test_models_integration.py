from django.test import TestCase, Client
from django.urls import reverse

from languages.models import Language, Paradigm, Programmer, Framework,\
    the_most_popular_language


class ChangesInParadigmUpdatedInLanguageTest(TestCase):
    """
    Integration test module for checking the changes in the paradigm instance
    are updated in the language instance.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        self.valid_update_url = reverse('paradigm-update',
                                        kwargs={'pk': self.test_paradigm.pk})

        self.payload = {'name': 'changed_test_paradigm'}

    def test_changes_in_paradigm_updated_in_language(self):
        # Change the test_paradigm with the put-method.
        self.client.put(self.valid_update_url,
                        data=self.payload,
                        content_type='application/json')
        # Get the changed paradigm from db.
        changed_test_paradigm = Paradigm.objects.get(pk=self.test_paradigm.pk)

        self.assertEqual(changed_test_paradigm.name,
                         self.test_language.paradigm.get().name)


class ChangesInLanguageUpdatedInFrameworkTest(TestCase):
    """
    Integration test module for checking the changes in the language instance
    are updated in the framework instance.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        self.test_framework = Framework.objects.create(name='test_framework',
                                                       languages=self.test_language)
        self.payload = {'name': 'changed_test_language',
                        'paradigm': self.test_paradigm}
        self.valid_update_url = reverse('language-update',
                                        kwargs={'pk': self.test_language.pk})
        self.invalid_update_url = reverse('language-update',
                                          kwargs={'pk': 2000})

    def test_changes_in_language_updated_in_framework(self):
        # Change the test_language with the put-method.
        self.client.put(self.valid_update_url,
                        data=self.payload)

        self.assertEqual(self.test_language, self.test_framework.languages)

    def test_invalid_changes_in_language_not_updated_in_framework(self):
        self.client.put(self.invalid_update_url,
                        data=self.payload)

        self.assertEqual(self.test_language, self.test_framework.languages)


class ChangesInLanguageUpdatedInProgrammerTest(TestCase):
    """
    Integration test module for checking the changes in the language instance
    are updated in the programmer instance.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.update_url = reverse('language-update',
                                  kwargs={'pk': self.test_language.pk})
        self.payload = {'changed_test_language'}
        self.content_type = 'application/json'

    def test_changes_in_language_updated_in_programmer(self):
        # Change the language instance with the put-method.
        self.client.put(self.update_url,
                        data=self.payload,
                        content_type=self.content_type)
        changed_test_language = Language.objects.get(pk=self.test_language.pk)

        self.assertEqual(changed_test_language,
                         self.test_programmer.languages.get())


class ChangesInFrameworkUpdatedInProgrammerTest(TestCase):
    """
    Integration test module for checking the changes in th eframework instance
    are updated in the programmer instance.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        self.test_framework = Framework.objects.create(name='test_framework',
                                                       languages=self.test_language)
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.frameworks.add(self.test_framework)

    def test_changes_in_framework_updated_in_programmer(self):
        self.client.put(reverse('framework-update',
                                kwargs={'pk': self.test_framework.pk}),
                        data={'name': 'changed_test_framework'},
                        content_type='application/json')

        self.assertEqual(self.test_framework, self.test_programmer.frameworks.get())


class NumberAndListOfLanguagesUpdatedWhenChangesTest(TestCase):
    """
    Integration test module for checking number and list of languages
    which support this paradigm is updated when their amount was changed.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')

        self.test_language1 = Language.objects.create(name='test_language1')
        self.test_language2 = Language.objects.create(name='test_language2')
        self.test_language3 = Language.objects.create(name='test_language3')
        self.test_language4 = Language.objects.create(name='test_language4')
        self.test_language5 = Language.objects.create(name='test_language5')
        self.languages = [self.test_language1,
                          self.test_language2,
                          self.test_language3,
                          self.test_language4,
                          self.test_language5]

        for language in self.languages:
            language.paradigm.add(self.test_paradigm)

    def test_check_number_of_languages_if_their_amount_changed(self):
        self.client.delete(reverse('language-delete',
                                   kwargs={'pk': self.test_language1.pk}))

        self.assertEqual(self.test_paradigm.number_of_languages_which_support_this_paradigm, 4)

    def test_check_list_of_languages_if_their_amount_changed(self):
        self.client.delete(reverse('language-delete',
                                   kwargs={'pk': self.test_language1.pk}))
        self.client.delete(reverse('language-delete',
                                   kwargs={'pk': self.test_language4.pk}))

        list_of_languages_after_remove = self.languages[:]
        del list_of_languages_after_remove[0]
        del list_of_languages_after_remove[2]

        self.assertEqual(self.test_paradigm.list_of_languages_which_support_this_paradigm,
                         list_of_languages_after_remove)


class NumberAndListOfProgrammersUpdatedWhenChangesTest(TestCase):
    """
    Integration test module for checking the number and list of the programmers
    who know this language is updated when their amount was changed.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.test_programmer1 = Programmer.objects.create(name='test_programmer1')
        self.test_programmer1.languages.add(self.test_language)
        self.test_programmer2 = Programmer.objects.create(name='test_programmer2')
        self.test_programmer2.languages.add(self.test_language)
        self.test_programmer3 = Programmer.objects.create(name='test_programmer3')
        self.test_programmer3.languages.add(self.test_language)

        self.delete_url = reverse('programmer-delete',
                                   kwargs={'pk': self.test_programmer2.pk})

    def test_check_number_of_programmers_if_their_amount_changed(self):
        self.client.delete(self.delete_url)

        self.assertEqual(self.test_language.number_of_programmers_who_know_this_language, 2)

    def test_check_list_of_programmers_if_their_amount_changed(self):
        self.client.delete(self.delete_url)

        list_of_programmers_after_remove = [self.test_programmer1,
                                            self.test_programmer3]

        self.assertEqual(self.test_language.list_of_programmers_who_know_this_language,
                         list_of_programmers_after_remove)


class NumberAndListOfFrameworksUpdatedWhenChangesTest(TestCase):
    """
    Integration test module for checking the most popular framework,
    the number and list of the frameworks of this language is updated
    when their amount was changed.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.test_framework1 = Framework.objects.create(name='test_framework1',
                                                        languages=self.test_language)
        self.test_framework2 = Framework.objects.create(name='test_framework2',
                                                        languages=self.test_language)
        self.test_framework3 = Framework.objects.create(name='test_framework3',
                                                        languages=self.test_language)

        # Create programmers.
        self.test_programmer1 = Programmer.objects.create(name='test_programmer1')
        self.test_programmer1.frameworks.add(self.test_framework1)
        self.test_programmer2 = Programmer.objects.create(name='test_programmer2')
        self.test_programmer2.frameworks.add(self.test_framework1)
        self.test_programmer3 = Programmer.objects.create(name='test_programmer3')
        self.test_programmer3.frameworks.add(self.test_framework2)

        self.delete_url = reverse('framework-delete',
                                  kwargs={'pk': self.test_framework2.pk})

    def test_check_number_of_frameworks_if_their_amount_changed(self):
        self.client.delete(self.delete_url)

        self.assertEqual(self.test_language.number_of_frameworks, 2)

    def test_check_list_of_frameworks_if_their_amount_changed(self):
        self.client.delete(self.delete_url)

        list_of_frameworks_after_remove = [self.test_framework1,
                                           self.test_framework3]

        self.assertEqual(self.test_language.list_of_frameworks,
                         list_of_frameworks_after_remove)

    def test_check_the_most_popular_framework_if_amount_of_programmers_changed(self):
        self.test_programmer2.frameworks.set([self.test_framework2])

        self.assertEqual(self.test_language.the_most_popular_framework,
                         self.test_framework2)


class NumberAndListOfProgrammersWhoKnowFrameworkChangesTest(TestCase):
    """
    Integration test module for checking the number and the list of programmers
    who know the framework are updated if amount of programmers was changed.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        self.test_framework = Framework.objects.create(name='test_framework',
                                                       languages=self.test_language)
        self.test_programmer1 = Programmer.objects.create(name='test_programmer1')
        self.test_programmer1.frameworks.add(self.test_framework)
        self.test_programmer2 = Programmer.objects.create(name='test_programmer2')
        self.test_programmer2.frameworks.add(self.test_framework)
        self.test_programmer3 = Programmer.objects.create(name='test_programmer3')
        self.test_programmer3.frameworks.add(self.test_framework)
        self.delete_url = reverse('programmer-delete',
                                   kwargs={'pk': self.test_programmer2.pk})

    def test_number_of_programmers_who_know_this_framework(self):
        self.client.delete(self.delete_url)

        self.assertEqual(self.test_framework.number_of_programmers_who_know_this_framework, 2)

    def test_list_of_programmers_who_know_this_framework(self):
        self.client.delete(self.delete_url)
        list_of_programmers_after_remove = [self.test_programmer1,
                                            self.test_programmer3]

        self.assertEqual(self.test_framework.list_of_programmers_who_know_this_framework,
                         list_of_programmers_after_remove)


class TheMostPopularLanguageChangesTest(TestCase):
    """
    Integration test module for checking the the most popular language was changed
    if amount of programmers was changed.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language1 = Language.objects.create(name='test_language1')
        self.test_language1.paradigm.add(self.test_paradigm)
        self.test_language2 = Language.objects.create(name='test_language2')
        self.test_language2.paradigm.add(self.test_paradigm)
        self.test_language3 = Language.objects.create(name='test_language3')
        self.test_language3.paradigm.add(self.test_paradigm)

        self.test_programmer1 = Programmer.objects.create(name='test_programmer1')
        self.test_programmer1.languages.add(self.test_language1)
        self.test_programmer2 = Programmer.objects.create(name='test_programmer2')
        self.test_programmer2.languages.add(self.test_language1)
        self.test_programmer3 = Programmer.objects.create(name='test_programmer3')
        self.test_programmer3.languages.add(self.test_language2)
        self.test_programmer4 = Programmer.objects.create(name='test_programmer4')
        self.test_programmer4.languages.add(self.test_language3)

    def test_the_most_popular_language(self):
        self.client.delete(reverse('programmer-delete',
                                   kwargs={'pk': self.test_programmer3.pk}))

        self.assertEqual(the_most_popular_language(), self.test_language1)
