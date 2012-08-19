from celery.task import task

from gungnir.builds.models import BuildConfig


@task
def build_image(build_config_id):
    build_config = BuildConfig.objects.get(pk=build_config_id)

    builder = build_config.get_builder()
    builder.deploy()

    instance = builder.instance.id

    return instance