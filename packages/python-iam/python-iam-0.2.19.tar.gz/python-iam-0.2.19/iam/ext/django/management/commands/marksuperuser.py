"""Declares :class:`MarkSuperuserCommand`."""
from django.core.management.base import BaseCommand

from iam.ext.django.models import Subject


class Command(BaseCommand):
    help = 'Marks the subject as a super user.'

    def add_arguments(self, parser):
        parser.add_argument('subject_id')

    def handle(self, *args, **options):
        subject = Subject.objects.get(pk=options['subject_id'])
        subject.marksuperuser(True)
