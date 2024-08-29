# from collections import defaultdict
# from typing import Tuple

import supervisely as sly

# import src.globals as g
from src.cache import get_annotation_info, get_project_info, get_project_meta
from src.test import Test  # AllObjectsCase, AverageLabelAreaCase, NoObjectsCase
from src.ui.settings import card

app = sly.Application(layout=card)


# region list of checks
# 1. Check if annotaion on image does not contain any objects.
# 2. Check if annotation on image does not contain all objects from the project meta.

# endregion


@app.event(sly.Event.JobEntity.StatusChanged)
@sly.timeit
def job_status_changed(api: sly.Api, event: sly.Event.JobEntity.StatusChanged):
    # If job status is not "done", skip the event.
    if not event.job_entity_status == "done":
        return

    annotation_info = get_annotation_info(event.image_id)
    project_meta = get_project_meta(event.project_id)
    project_info = get_project_info(event.project_id)

    test = Test(project_info.name, project_meta, annotation_info)
    test.run()

    # annotation, project_meta = get_annotation_and_meta(event.image_id, event.project_id)
    # sly.logger.debug("Annotation for image_id=%s was obtained.", event.image_id)

    # test = Test(
    #     [NoObjectsCase, AllObjectsCase, AverageLabelAreaCase], project_meta, annotation
    # )
    # test.run()
