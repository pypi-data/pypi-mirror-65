.. _deployments_overview:

###########
Deployments
###########

Deployment is the central hub for users to deploy, manage and monitor their models.

Manage Deployments
******************

The following commands can be used to manage deployments.

Create a Deployment
===================

When creating a new deployment, a DataRobot ``model_id`` and ``label`` must be provided.
A ``description`` can be optionally provided to document the purpose of the deployment.

The default prediction server is used when making predictions against the deployment,
and is a requirement for creating a deployment on DataRobot cloud.
For on-prem installations, a user must not provide a default prediction server
and a pre-configured prediction server will be used instead.
Refer to :class:`datarobot.PredictionServer.list` for more information on retrieving available prediction servers.

.. code-block:: python

    import datarobot as dr

    project = dr.Project.get('5506fcd38bd88f5953219da0')
    model = project.get_models()[0]
    prediction_server = dr.PredictionServer.list()[0]

    deployment = dr.Deployment.create_from_learning_model(
        model.id, label='New Deployment', description='A new deployment',
        default_prediction_server_id=prediction_server.id)
    deployment
    >>> Deployment('New Deployment')

List Deployments
================

Use the following command to list deployments a user can view.

.. code-block:: python

    import datarobot as dr

    deployments = dr.Deployment.list()
    deployments
    >>> [Deployment('New Deployment'), Deployment('Previous Deployment')]

Refer to :class:`~datarobot.Deployment` for properties of the deployment object.

You can also filter the deployments that are returned by passing an instance of the
:class:`~datarobot.models.deployment.DeploymentListFilters` class to the ``filters`` keyword argument.

.. code-block:: python

    import datarobot as dr

    filters = dr.models.deployment.DeploymentListFilters(
        role='OWNER',
        accuracy_health=dr.enums.DEPLOYMENT_ACCURACY_HEALTH_STATUS.FAILING
    )
    deployments = dr.Deployment.list(filters=filters)
    deployments
    >>> [Deployment('Deployment Owned by Me w/ Failing Accuracy 1'), Deployment('Deployment Owned by Me w/ Failing Accuracy 2')]


Retrieve a Deployment
=====================

It is possible to retrieve a single deployment with its identifier,
rather than list all deployments.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.id
    >>> '5c939e08962d741e34f609f0'
    deployment.label
    >>> 'New Deployment'

Refer to :class:`~datarobot.Deployment` for properties of the deployment object.

Update a Deployment
===================

Deployment's label and description can be updated.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.update(label='new label')

Delete a Deployment
===================

To mark a deployment as deleted, use the following command.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.delete()


Model Replacement
*****************

The model of a deployment can be replaced effortlessly with zero interruption of predictions.

Model replacement is an asynchronous process, which means there are some
preparatory works to complete before the process is fully finished.
However, predictions made against this deployment will start
using the new model as soon as you initiate the process.
The :meth:`~datarobot.Deployment.replace_model` function won't return until this asynchronous process is fully finished.

Alongside the identifier of the new model, a ``reason`` is also required.
The reason is stored in model history of the deployment for bookkeeping purpose.
An enum `MODEL_REPLACEMENT_REASON` is provided for convenience, all possible values are documented below:

- MODEL_REPLACEMENT_REASON.ACCURACY
- MODEL_REPLACEMENT_REASON.DATA_DRIFT
- MODEL_REPLACEMENT_REASON.ERRORS
- MODEL_REPLACEMENT_REASON.SCHEDULED_REFRESH
- MODEL_REPLACEMENT_REASON.SCORING_SPEED
- MODEL_REPLACEMENT_REASON.OTHER

Here is an example of model replacement:

.. code-block:: python

    import datarobot as dr
    from datarobot.enums import MODEL_REPLACEMENT_REASON

    project = dr.Project.get('5cc899abc191a20104ff446a')
    model = project.get_models()[0]

    deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.model['id'], deployment.model['type']
    >>> ('5c0a979859b00004ba52e431', 'Decision Tree Classifier (Gini)')

    deployment.replace_model('5c0a969859b00004ba52e41b', MODEL_REPLACEMENT_REASON.ACCURACY)
    deployment.model['id'], deployment.model['type']
    >>> ('5c0a969859b00004ba52e41b', 'Support Vector Classifier (Linear Kernel)')

Validation
==========

Before initiating the model replacement request, it is usually a good idea to use
the :meth:`~datarobot.Deployment.validate_replacement_model` function to validate if the new model can be used as a replacement.

The :meth:`~datarobot.Deployment.validate_replacement_model` function returns the validation status, a message and a checks dictionary.
If the status is 'passing' or 'warning', use :meth:`~datarobot.Deployment.replace_model` to perform model the replacement.
If status is 'failing', refer to the `checks` dict for more details on why the new model cannot be used as a replacement.

.. code-block:: python

    import datarobot as dr

    project = dr.Project.get('5cc899abc191a20104ff446a')
    model = project.get_models()[0]
    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    status, message, checks = deployment.validate_replacement_model(new_model_id=model.id)
    status
    >>> 'passing'

    # `checks` can be inspected for detail, showing two examples here:
    checks['target']
    >>> {'status': 'passing', 'message': 'Target is compatible.'}
    checks['permission']
    >>> {'status': 'passing', 'message': 'User has permission to replace model.'}

.. _deployment_monitoring:

Monitoring
**********

Deployment monitoring can be categorized into several area of concerns:

- Service Stats & Service Stats Over Time
- Accuracy & Accuracy Over Time

With a :class:`~datarobot.Deployment` object, get functions are provided to allow querying of the monitoring data.
Alternatively, it is also possible to retrieve monitoring data directly using a deployment ID. For example:

.. code-block:: python

    from datarobot.models import Deployment, ServiceStats

    deployment_id = '5c939e08962d741e34f609f0'

    # call `get` functions on a `Deployment` object
    deployment = Deployment.get(deployment_id)
    service_stats = deployment.get_service_stats()

    # directly fetch without a `Deployment` object
    service_stats = ServiceStats.get(deployment_id)

When querying monitoring data, a start and end time can be optionally provided, will accept either a datetime object or a string.
Note that only top of the hour datetimes are accepted, for example: ``2019-08-01T00:00:00Z``.
By default, the end time of the query will be the next top of the hour, the start time will be 7 days before the end time.

In the over time variants, an optional ``bucket_size`` can be provided to specify the resolution of time buckets.
For example, if start time is `2019-08-01T00:00:00Z`, end time is ``2019-08-02T00:00:00Z`` and ``bucket_size`` is ``T1H``,
then 24 time buckets will be generated, each providing data calculated over one hour.
Use :func:`~datarobot.helpers.partitioning_methods.construct_duration_string` to help construct a bucket size string.

    .. note:: The minimum bucket size is one hour.

Service Stats
=============

Service stats are metrics tracking deployment utilization and how well deployments respond to prediction requests.
Use ``SERVICE_STAT_METRIC.ALL`` to retrieve a list of supported metrics.

:class:`~datarobot.models.ServiceStats` retrieves values for all service stats metrics;
:class:`~datarobot.models.ServiceStatsOverTime` can be used to fetch how one single metric changes over time.

.. code-block:: python

    from datetime import datetime
    from datarobot.enums import SERVICE_STAT_METRIC
    from datarobot.helpers.partitioning_methods import construct_duration_string
    from datarobot.models import Deployment

    deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    service_stats = deployment.get_service_stats(
        start_time=datetime(2019, 8, 1, hour=15),
        end_time=datetime(2019, 8, 8, hour=15)
    )
    service_stats[SERVICE_STAT_METRIC.TOTAL_PREDICTIONS]
    >>> 12597

    total_predictions = deployment.get_service_stats_over_time(
        start_time=datetime(2019, 8, 1, hour=15),
        end_time=datetime(2019, 8, 8, hour=15),
        bucket_size=construct_duration_string(days=1),
        metric=SERVICE_STAT_METRIC.TOTAL_PREDICTIONS
    )
    total_predictions.bucket_values
    >>> OrderedDict([(datetime.datetime(2019, 8, 1, 15, 0, tzinfo=tzutc()), 1610),
                     (datetime.datetime(2019, 8, 2, 15, 0, tzinfo=tzutc()), 2249),
                     (datetime.datetime(2019, 8, 3, 15, 0, tzinfo=tzutc()), 254),
                     (datetime.datetime(2019, 8, 4, 15, 0, tzinfo=tzutc()), 943),
                     (datetime.datetime(2019, 8, 5, 15, 0, tzinfo=tzutc()), 1967),
                     (datetime.datetime(2019, 8, 6, 15, 0, tzinfo=tzutc()), 2810),
                     (datetime.datetime(2019, 8, 7, 15, 0, tzinfo=tzutc()), 2775)])

Accuracy
========

A collection of metrics are provided to measure the accuracy of a deployment's predictions.
For deployments with classification model, use ``ACCURACY_METRIC.ALL_CLASSIFICATION`` for all supported metrics;
in the case of deployment with regression model, use ``ACCURACY_METRIC.ALL_REGRESSION`` instead.

Similarly with Service Stats, :class:`~datarobot.models.Accuracy` and :class:`~datarobot.models.AccuracyOverTime`
are provided to retrieve all default accuracy metrics and how one single metric change over time.

.. code-block:: python

    from datetime import datetime
    from datarobot.enums import ACCURACY_METRIC
    from datarobot.helpers.partitioning_methods import construct_duration_string
    from datarobot.models import Deployment

    deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    accuracy = deployment.get_accuracy(
        start_time=datetime(2019, 8, 1, hour=15),
        end_time=datetime(2019, 8, 1, 15, 0)
    )
    accuracy[ACCURACY_METRIC.RMSE]
    >>> 943.225

    rmse = deployment.get_accuracy_over_time(
        start_time=datetime(2019, 8, 1),
        end_time=datetime(2019, 8, 3),
        bucket_size=construct_duration_string(days=1),
        metric=ACCURACY_METRIC.RMSE
    )
    rmse.bucket_values
    >>> OrderedDict([(datetime.datetime(2019, 8, 1, 15, 0, tzinfo=tzutc()), 1777.190657),
                     (datetime.datetime(2019, 8, 2, 15, 0, tzinfo=tzutc()), 1613.140772)])

It is also possible to retrieve how multiple metrics changes over the same period of time,
enabling easier side by side comparison across different metrics.

.. code-block:: python

    from datarobot.enums import ACCURACY_METRIC
    from datarobot.models import Deployment

    accuracy_over_time = AccuracyOverTime.get_as_dataframe(
        ram_app.id, [ACCURACY_METRIC.RMSE, ACCURACY_METRIC.GAMMA_DEVIANCE, ACCURACY_METRIC.MAD])

Settings
********

Drift Tracking Settings
=======================

Drift tracking is used to help analyze and monitor the performance of a model after it is deployed.
When the model of a deployment is replaced drift tracking status will not be altered.

Use :meth:`~datarobot.Deployment.get_drift_tracking_settings` to retrieve the current tracking status for target drift and feature drift.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    settings = deployment.get_drift_tracking_settings()
    settings
    >>> {'target_drift': {'enabled': True}, 'feature_drift': {'enabled': True}}

Use :meth:`~datarobot.Deployment.update_drift_tracking_settings` to update target drift and feature drift tracking status.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.update_drift_tracking_settings(target_drift_enabled=True, feature_drift_enabled=True)

.. _deployment_association_id:

Association ID Settings
=======================

Association ID is used to identify predictions, so that when actuals are acquired, accuracy can be calculated.

Use :meth:`~datarobot.Deployment.get_association_id_settings` to retrieve current association ID settings.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    settings = deployment.get_association_id_settings()
    settings
    >>> {'column_names': ['application_id'], 'required_in_prediction_requests': True}

Use :meth:`~datarobot.Deployment.update_association_id_settings` to update association ID settings.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.update_association_id_settings(column_names=['application_id'], required_in_prediction_requests=True)

.. _deployment_prediction_warning:

Prediction Warning Settings
===========================

Prediction Warning is used to enable Humble AI for a deployment which determines if a
model is misbehaving when a prediction goes outside of the calculated boundaries.

Use :meth:`~datarobot.Deployment.get_prediction_warning_settings` to retrieve the current prediction warning settings.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    settings = deployment.get_prediction_warning_settings()
    settings
    >>> {{'enabled': True}, 'custom_boundaries': {'upper': 1337, 'lower': 0}}

Use :meth:`~datarobot.Deployment.update_prediction_warning_settings` to update current prediction warning settings.

.. code-block:: python

    import datarobot as dr

    # Set custom boundaries
    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.update_prediction_warning_settings(
        prediction_warning_enabled=True,
        use_default_boundaries=False,
        lower_boundary=1337,
        upper_boundary=2000,
    )

    # Reset boundaries
    deployment.update_prediction_warning_settings(
        prediction_warning_enabled=True,
        use_default_boundaries=True,
    )
