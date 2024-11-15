from __future__ import unicode_literals

from django.test import TestCase

from waffle.models import Sample, Switch
from waffle.utils import get_flag_model, get_setting


class ModelsTests(TestCase):
    def test_natural_keys(self):
        flag = get_flag_model().objects.create(name='test-flag')
        switch = Switch.objects.create(name='test-switch')
        sample = Sample.objects.create(name='test-sample', percent=0)

        self.assertEqual(flag.natural_key(), ('test-flag',))
        self.assertEqual(switch.natural_key(), ('test-switch',))
        self.assertEqual(sample.natural_key(), ('test-sample',))

        self.assertEqual(get_flag_model().objects.get_by_natural_key('test-flag'), flag)
        self.assertEqual(Switch.objects.get_by_natural_key('test-switch'), switch)
        self.assertEqual(Sample.objects.get_by_natural_key('test-sample'), sample)
