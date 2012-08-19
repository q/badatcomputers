from celery.task import task
from django.template.loader import render_to_string
from gungnir.builds.models import BuildConfig, Build

from django.core.mail import send_mail
from django.conf import settings

from datetime import datetime
from functools import partial

BUILD_COMPLETE_SUBJECT = 'email/build_complete_subject.txt'
BUILD_COMPLETE_BODY = 'email/build_complete_body.txt'

BUILD_FAILED_SUBJECT = 'email/build_failed_subject.txt'
BUILD_FAILED_BODY = 'email/build_failed_body.txt'

@task
def build_image(build_id):
    build = Build.objects.get(pk=build_id)

    build_config = build.config

    builder = build_config.get_builder()

    mail_to = build_config.application.owner.email
    mail_context = {'build_config': build_config, 'builder': builder}

    try:
        build.deploy_status = 'IN PROGRESS'
        build.save()
        instance_id, ami_id = builder.build()


    except Exception as e:
        # Does a naked except count as bad practices if it gets reraised? lets hope not.
        mail_context['error'] = e
        fail_mail_subject = render_to_string(BUILD_FAILED_SUBJECT, mail_context)
        fail_mail_body = render_to_string(BUILD_FAILED_BODY, mail_context)

        send_mail(fail_mail_subject, fail_mail_body, settings.DEFAULT_FROM_EMAIL, [mail_to])

        build.deploy_status = 'FAILED'
        build.save()

        raise


    build.instance_id = instance_id
    build.ami_id = ami_id
    build.config = build_config
    build.build_date = datetime.now()
    build.deploy_status = 'COMPLETED'
    build.save(async_task=False)

    mail_context['build'] = build

    mail_subject = render_to_string(BUILD_COMPLETE_SUBJECT, mail_context)
    mail_body = render_to_string(BUILD_COMPLETE_BODY, mail_context)

    send_mail(mail_subject, mail_body, settings.DEFAULT_FROM_EMAIL, [mail_to])

    return build.pk