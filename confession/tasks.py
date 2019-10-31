from celery import shared_task


@shared_task
def name_of_your_function(optional_param):
    pass  # do something heavy
