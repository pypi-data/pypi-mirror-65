#########
ModelJobs
#########

Model creation is asynchronous process. This means than when explicitly invoking
new model creation (with ``project.train`` or ``model.train`` for example) all you get
is id of process, responsible for model creation. With this id you can
get info about model that is being created or the model itself, when
creation process is finished. For this you should use
the ``ModelJob`` class.

Get an existing ModelJob
************************

To retrieve existing ModelJob use ``ModelJob.get`` method.
For this you need id of Project that is used for model
creation and id of ModelJob. Having ModelJob might be useful if you want to
know parameters of model creation, automatically chosen by API backend,
before actual model was created.

If model is already created, ``ModelJob.get`` will raise ``PendingJobFinished``
exception

.. code-block:: python

    import time

    import datarobot as dr

    blueprint_id = '5506fcd38bd88f5953219da0'
    model_job_id = project.train(blueprint_id)
    model_job = dr.ModelJob.get(project_id=project.id,
                                model_job_id=model_job_id)
    model_job.sample_pct
    >>> 64.0

    # wait for model to be created (in a very inefficient way)
    time.sleep(10 * 60)
    model_job = dr.ModelJob.get(project_id=project.id,
                                model_job_id=model_job_id)
    >>> datarobot.errors.PendingJobFinished

    # get the job attached to the model
    model_job.model
    >>> Model('5d518cd3962d741512605e2b')

Get created model
*****************

After model is created, you can use ModelJob.get_model to get newly
created model.

.. code-block:: python

    import datarobot as dr

    model = dr.ModelJob.get_model(project_id=project.id,
                                  model_job_id=model_job_id)

.. _wait_for_async_model_creation-label:

wait_for_async_model_creation function
**************************************
If you just want to get the created model after getting the ModelJob id, you
can use the :ref:`wait_for_async_model_creation<wait_for_async_model_creation-api-label>` function.
It will poll for the status of the model creation process until it's finished, and
then will return the newly created model. Note the differences below between datetime partitioned projects and
non-datetime-partitioned projects.

.. code-block:: python

    from datarobot.models.modeljob import wait_for_async_model_creation

    # used during training based on blueprint
    model_job_id = project.train(blueprint, sample_pct=33)
    new_model = wait_for_async_model_creation(
        project_id=project.id,
        model_job_id=model_job_id,
    )

    # used during training based on existing model
    model_job_id = existing_model.train(sample_pct=33)
    new_model = wait_for_async_model_creation(
        project_id=existing_model.project_id,
        model_job_id=model_job_id,
    )

    # For datetime-partitioned projects, use project.train_datetime. Note that train_datetime returns a ModelJob instead
    # of just an id.
    model_job = project.train_datetime(blueprint)
    new_model = wait_for_async_model_creation(
        project_id=project.id,
        model_job_id=model_job.id
    )
