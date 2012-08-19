from celery.task import task
from django.template.loader import render_to_string
from gungnir.builds.models import BuildConfig, Build

from django.core.mail import send_mail

BUILD_COMPLETE_SUBJECT = 'email/build_complete_subject.txt'
BUILD_COMPLETE_BODY = 'email/build_complete_body.txt'

BUILD_FAILED_SUBJECT = 'email/build_failed_subject.txt'
BUILD_FAILED_BODY = 'email/build_failed_body.txt'

@task
def build_image(build_config_id):
    build_config = BuildConfig.objects.get(pk=build_config_id)

    builder = build_config.get_builder()

    mail_to = build_config.application.owner.email
    mail_context = {'build_config': build_config, 'builder': builder}
    try:
        ami_id = builder.build()
    except Exception as e:
        # Does a naked except count as bad practices if it gets reraised? lets hope not.
        mail_context['error'] = e
        fail_mail_subject = render_to_string(BUILD_FAILED_SUBJECT, mail_context)
        fail_mail_body = render_to_string(BUILD_FAILED_BODY, mail_context)

        send_mail(subject, body, mail_to)

        raise
    instance_id = builder.instance.id

    build = Build()
    build.instance_id = instance_id
    build.ami_id = ami_id
    build.config = build_config
    build.save()

    mail_context['build'] = build

    mail_subject = render_to_string(BUILD_COMPLETE_SUBJECT, mail_context)
    mail_body = render_to_string(BUILD_COMPLETE_BODY, mail_context)

    send_mail(mail_subject, mail_body, mail_context)

    return build.pk