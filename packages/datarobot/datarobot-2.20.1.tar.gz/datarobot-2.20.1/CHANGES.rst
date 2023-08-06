#########
Changelog
#########

2.20.1
======

Bugfixes
********
A missing dependency is now included in the dependency list, which should resolve the issue with
users needing to manually install ``attr``.

2.20.0
======

New Features
************

- There is a new :class:`Dataset<datarobot.Dataset>` object that implements some of the
  public API routes at `api/v2/datasets/`. This also adds two new feature classes and a details
  class.

    - :class:`DatasetFeature<datarobot.models.DatasetFeature>`
    - :class:`DatasetFeatureHistogram<datarobot.models.DatasetFeatureHistogram>`
    - :class:`DatasetDetails<datarobot.DatasetDetails>`

  Functionality:

        - Create a Dataset by uploading from a file, URL or in-memory datasource.

            - :meth:`Dataset.create_from_file<datarobot.Dataset.create_from_file>`
            - :meth:`Dataset.create_from_in_memory_data<datarobot.Dataset.create_from_in_memory_data>`
            - :meth:`Dataset.create_from_url<datarobot.Dataset.create_from_url>`

        - Get Datasets or elements of Dataset with:

            - :meth:`Dataset.list<datarobot.Dataset.list>` lists available Datasets
            - :meth:`Dataset.get<datarobot.Dataset.get>` gets a specified Dataset
            - :meth:`Dataset.update<datarobot.Dataset.get>` updates the Dataset with the latest server information.
            - :meth:`Dataset.get_details<datarobot.Dataset.get_details>` gets the DatasetDetails of the Dataset.
            - :meth:`Dataset.get_all_features<datarobot.Dataset.get_all_features>` gets a list of the Dataset's Features.
            - :meth:`Dataset.get_file<datarobot.Dataset.get_file>` downloads the Dataset as a csv file.
            - :meth:`Dataset.get_projects<datarobot.Dataset.get_projects>` gets a list of Projects that use the Dataset.

        - Modify, delete or un-delete a Dataset:

            - :meth:`Dataset.modify<datarobot.Dataset.modify>` Changes the name and categories of the Dataset
            - :meth:`Dataset.delete<datarobot.Dataset.delete>` soft deletes a Dataset.
            - :meth:`Dataset.un_delete<datarobot.Dataset.un_delete>` un-deletes the Dataset. You cannot retrieve the
              IDs of deleted Datasets, so if you want to un-delete a Dataset, you need to store its ID before deletion.

        - You can also create a Project using a `Dataset` with:

            - :meth:`Project.create_from_dataset<datarobot.models.Project.create_from_dataset>`

- Now it's possible to connect two or more datasets by specifying the relationships between them using Feature Engineering Graph so that DataRobot can automatically generate features based on connection between datasets. The :class:`FeatureEngineeringGraph <datarobot.models.FeatureEngineeringGraph>` class can now create, update, retrieve, list, delete feature engineering graphs call to methods

    - :meth:`FeatureEngineeringGraph.create <datarobot.models.FeatureEngineeringGraph.create>` creates a new feature engineering graph
    - :meth:`FeatureEngineeringGraph.update <datarobot.models.FeatureEngineeringGraph.update>` updates the name and description of the feature engineering graph
    - :meth:`FeatureEngineeringGraph.replace <datarobot.models.FeatureEngineeringGraph.replace>` replace the content of the feature engineering graph
    - :meth:`FeatureEngineeringGraph.delete <datarobot.models.FeatureEngineeringGraph.delete>` delete the feature engineering graph
    - :meth:`FeatureEngineeringGraph.retrieve <datarobot.models.FeatureEngineeringGraph.get>` retrieve the feature engineering graph
    - :meth:`FeatureEngineeringGraph.list <datarobot.models.FeatureEngineeringGraph.list>` list all the feature engineering graphs

- It's possible to share the feature engineering graph with others and list all the users who have access to a given feature engineering graph.

    - :meth:`FeatureEngineeringGraph.share <datarobot.models.FeatureEngineeringGraph.share>` allows to share the given feature engineering graph
      with other users
    - :meth:`FeatureEngineeringGraph.get_access_list <datarobot.models.FeatureEngineeringGraph.get_access_list>` list all the users who have access to the given feature engineering graph

- It is possible to create an alternative configuration for the secondary dataset which can be used during the prediction

    - :meth:`SecondaryDatasetConfigurations.create <datarobot.models.SecondaryDatasetConfigurations.create>` allow to create secondary dataset configuration

- You can now filter the deployments returned by the :meth:`Deployment.list <datarobot.Deployment.list>` command. You can do this by passing an instance of the :class:`~datarobot.models.deployment.DeploymentListFilters` class to the ``filters`` keyword argument. The currently supported filters are:

    - ``role``
    - ``service_health``
    - ``model_health``
    - ``accuracy_health``
    - ``execution_environment_type``
    - ``materiality``

- A new workflow is available for making predictions in time series projects. To that end,
  :class:`PredictionDataset<datarobot.models.PredictionDataset>` objects now contain the following
  new fields:

    - ``forecast_point_range``: The start and end date of the range of dates available for use as the forecast point,
      detected based on the uploaded prediction dataset
    - ``data_start_date``: A datestring representing the minimum primary date of the prediction dataset
    - ``data_end_date``: A datestring representing the maximum primary date of the prediction dataset
    - ``max_forecast_date``: A datestring representing the maximum forecast date of this prediction dataset

  Additionally, users no longer need to specify a ``forecast_point`` or ``predictions_start_date`` and
  ``predictions_end_date`` when uploading datasets for predictions in time series projects. More information can be
  found in the :ref:`time series predictions<new_pred_ux>` documentation.

- Per-class lift chart data is now available for multiclass models using
  :meth:`Model.get_multiclass_lift_chart <datarobot.models.Model.get_multiclass_lift_chart>`.

- Unsupervised projects can now be created using the :meth:`Project.start <datarobot.models.Project.start>`
  and :meth:`Project.set_target <datarobot.models.Project.set_target>` methods by providing ``unsupervised_mode=True``,
  provided that the user has access to unsupervised machine learning functionality. Contact support for more information.

- A new boolean attribute ``unsupervised_mode`` was added to :py:class:`datarobot.DatetimePartitioningSpecification <datarobot.DatetimePartitioningSpecification>`.
  When it is set to True, datetime partitioning for unsupervised time series projects will be constructed for
  nowcasting: ``forecast_window_start=forecast_window_end=0``.

- Users can now configure the start and end of the training partition as well as the end of the validation partition for
  backtests in a datetime-partitioned project. More information and example usage can be found in the
  :ref:`backtesting documentation <backtest_configuration>`.

- Added the :class:`DatasetFeaturelist<datarobot.DatasetFeaturelist>` class to support featurelists
  on datasets in the AI Catalog. DatasetFeaturelists can be updated or deleted. Two new methods were
  also added to :class:`Dataset<datarobot.Dataset>` to interact with DatasetFeaturelists. These are
  :meth:`Dataset.get_featurelists<datarobot.Dataset.get_featurelists>` and
  :meth:`Dataset.create_featurelist<datarobot.Dataset.create_featurelist>` which list existing
  featurelists and create new featurelists on a dataset, respectively.

Enhancements
************

- Updated the user agent header to show which python version.
- :meth:`Model.get_frozen_child_models <datarobot.models.Model.get_frozen_child_models>` can be used to retrieve models that are frozen from a given model
- Added ``datarobot.enums.TS_BLENDER_METHOD`` to make it clearer which blender methods are allowed for use in time
  series projects.
- Made creating projects from a dataset easier through the new
  :meth:`Dataset.create_project<datarobot.Dataset.create_project>`.

Bugfixes
********
- An issue where uploaded CSV's would loose quotes during serialization causing issues when columns containing line terminators where loaded in a dataframe, has been fixed

- :meth:`Project.get_association_featurelists <datarobot.models.Project.get_association_featurelists>` is now using the correct endpoint name, but the old one will continue to work

- Python API :class:`PredictionServer<datarobot.PredictionServer>` supports now on-premise format of API response.

- An issue with input validation of the Batch Prediction module has been resolved.

API Changes
***********
- Three new fields were added to the :class:`Dataset<datarobot.Dataset>` object. This reflects the
  updated fields in the public API routes at `api/v2/datasets/`. The added fields are:

    - processing_state: Current ingestion process state of the dataset
    - row_count: The number of rows in the dataset.
    - size: The size of the dataset as a CSV in bytes.


2.19.0
======

New Features
************

- Projects can be cloned using :meth:`Project.clone_project <datarobot.models.Project.clone_project>`
- Calendars used in time series projects now support having series-specific events, for instance if a holiday only affects some stores. This can be controlled by using new argument of the :meth:`CalendarFile.create <datarobot.CalendarFile.create>` method.
  If multiseries id columns are not provided, calendar is considered to be single series and all events are applied to all series.
- We have expanded prediction intervals availability to the following use-cases:

    - Time series model deployments now support prediction intervals. See
      :meth:`Deployment.get_prediction_intervals_settings<datarobot.Deployment.get_prediction_intervals_settings>`
      and :meth:`Deployment.update_prediction_intervals_settings<datarobot.Deployment.update_prediction_intervals_settings>` for usage.
    - Prediction intervals are now supported for model exports for time series. To that end, a new optional parameter
      ``prediction_intervals_size`` has been added to :meth:`Model.request_transferable_export <datarobot.models.Model.request_transferable_export>`.

  More details on prediction intervals can be found in the :ref:`prediction intervals documentation <prediction_intervals>`.
- Allowed pairwise interaction groups can now be specified in :py:class:`AdvancedOptions <datarobot.helpers.AdvancedOptions>`.
  They will be used in GAM models during training.
- New deployments features:

    - Update the label and description of a deployment using :meth:`Deployment.update<datarobot.Deployment.update>`.
    - :ref:`Association ID setting<deployment_association_id>` can be retrieved and updated.
    - Regression deployments now support :ref:`prediction warnings<deployment_prediction_warning>`.

- For multiclass models now it's possible to get feature impact for each individual target class using
  :meth:`Model.get_multiclass_feature_impact <datarobot.models.Model.get_multiclass_feature_impact>`
- Added support for new :ref:`Batch Prediction API <batch_predictions>`.
- It is now possible to create and retrieve basic, oauth and s3 credentials with
  :py:class:`Credential <datarobot.models.Credential>`.


- It's now possible to get feature association statuses for featurelists using
  :meth:`Project.get_association_featurelists <datarobot.models.Project.get_association_featurelists>`

- You can also pass a specific featurelist_id into
  :meth:`Project.get_associations <datarobot.models.Project.get_associations>`

Enhancements
************

- Added documentation to :meth:`Project.get_metrics <datarobot.models.Project.get_metrics>` to detail the new ``ascending`` field that
  indicates how a metric should be sorted.

- Retraining of a model is processed asynchronously and returns a  ``ModelJob`` immediately.

- Blender models can be retrained on a different set of data or a different feature list.

- Word cloud ngrams now has ``variable`` field representing the source of the ngram.

- Method :meth:`WordCloud.ngrams_per_class <datarobot.models.word_cloud.WordCloud.ngrams_per_class>` can be used to
  split ngrams for better usability in multiclass projects.

- Method :meth:`Project.set_target <datarobot.models.Project.set_target>` support new optional parameters ``featureEngineeringGraphs`` and ``credentials``.

- Method :py:meth:`Project.upload_dataset <datarobot.models.Project.upload_dataset>` and :py:meth:`Project.upload_dataset_from_data_source <datarobot.models.Project.upload_dataset_from_data_source>` support new optional parameter ``credentials``.

- Series accuracy retrieval methods (:meth:`DatetimeModel.get_series_accuracy_as_dataframe <datarobot.models.DatetimeModel.get_series_accuracy_as_dataframe>`
  and :meth:`DatetimeModel.download_series_accuracy_as_csv <datarobot.models.DatetimeModel.download_series_accuracy_as_csv>`)
  for multiseries time series projects now support additional parameters for specifying what data to retrieve, including:

    - ``metric``: Which metric to retrieve scores for
    - ``multiseries_value``: Only returns series with a matching multiseries ID
    - ``order_by``: An attribute by which to sort the results


Bugfixes
********
- An issue when using :meth:`Feature.get <datarobot.models.Feature.get>` and :meth:`ModelingFeature.get <datarobot.models.ModelingFeature.get>` to retrieve summarized categorical feature has been fixed.

API Changes
***********
- The datarobot package is now no longer a
  `namespace package <https://packaging.python.org/guides/packaging-namespace-packages/>`_.
- ``datarobot.enums.BLENDER_METHOD.FORECAST_DISTANCE`` is removed (deprecated in 2.18.0).

Documentation Changes
*********************

- Updated :ref:`Residuals charts <residuals_chart>` documentation to reflect that the data rows include row numbers from the source dataset for projects
  created in DataRobot 5.3 and newer.

2.18.0
======

New Features
************
- :ref:`Residuals charts <residuals_chart>` can now be retrieved for non-time-aware regression models.

- :ref:`Deployment monitoring <deployment_monitoring>` can now be used to retrieve service stats, service health, accuracy info, permissions, and feature lists for deployments.

- :ref:`Time series <time_series>` projects now support the Average by Forecast Distance blender, configured with more than one Forecast Distance. The blender blends the selected models, selecting the best three models based on the backtesting score for each Forecast Distance and averaging their predictions. The new blender method ``FORECAST_DISTANCE_AVG`` has beed added to ``datarobot.enums.BLENDER_METHOD``.

- :py:meth:`Deployment.submit_actuals <datarobot.Deployment.submit_actuals>` can now be used to submit data about actual results from a deployed model, which can be used to calculate accuracy metrics.

Enhancements
************
- Monotonic constraints are now supported for OTV projects. To that end, the parameters ``monotonic_increasing_featurelist_id`` and ``monotonic_decreasing_featurelist_id`` can be specified in calls to :meth:`Model.train_datetime <datarobot.models.Model.train_datetime>` or :meth:`Project.train_datetime <datarobot.models.Project.train_datetime>`.

- When :py:meth:`retrieving information about features <datarobot.models.Feature.get>`, information about summarized categorical variables is now available in a new ``keySummary``.

- For :py:class:`Word Clouds <datarobot.models.word_cloud.WordCloud>` in multiclass projects, values of the target class for corresponding word or ngram can now be passed using the new ``class`` parameter.

- Listing deployments using :py:meth:`Deployment.list <datarobot.Deployment.list>` now support sorting and searching the results using the new ``order_by`` and ``search`` parameters.

- You can now get the model associated with a model job by getting the ``model`` variable on the :py:class:`model job object <datarobot.models.ModelJob>`.

- The :class:`Blueprint <datarobot.models.Blueprint>` class can now retrieve the ``recommended_featurelist_id``, which indicates which feature list is recommended for this blueprint. If the field is not present, then there is no recommended feature list for this blueprint.

- The :class:`Model <datarobot.models.Model>` class now can be used to retrieve the ``model_number``.

- The method :py:meth:`Model.get_supported_capabilities <datarobot.models.Model.get_supported_capabilities>` now has an extra field ``supportsCodeGeneration`` to explain whether the model supports code generation.

- Calls to :py:meth:`Project.start <datarobot.models.Project.start>` and :py:meth:`Project.upload_dataset <datarobot.models.Project.upload_dataset>` now support uploading data via S3 URI and `pathlib.Path` objects.

- Errors upon connecting to DataRobot are now clearer when an incorrect API Token is used.

- The datarobot package is now a `namespace package <https://packaging.python.org/guides/packaging-namespace-packages/>`_.

Deprecation Summary
*******************

- ``datarobot.enums.BLENDER_METHOD.FORECAST_DISTANCE`` is deprecated and will be removed in 2.19. Use ``FORECAST_DISTANCE_ENET`` instead.

Documentation Changes
*********************
- Various typo and wording issues have been addressed.

- A new notebook showing regression-specific features is now been added to the :ref:`examples<examples_index>`.

- Documentation for :ref:`Access lists <sharing>` has been added.

2.17.0
======

New Features
************
- :ref:`Deployments <deployments_overview>` can now be managed via the API by using the new :py:class:`Deployment <datarobot.Deployment>` class.

- Users can now list available prediction servers using :meth:`PredictionServer.list <datarobot.PredictionServer.list>`.

- When :class:`specifying datetime partitioning <datarobot.DatetimePartitioningSpecification>` settings , :ref:`time series <time_series>` projects can now mark individual features as excluded from feature derivation using the
  :py:class:`FeatureSettings.do_not_derive <datarobot.FeatureSettings>` attribute. Any features not specified will be assigned according to the :py:class:`DatetimePartitioningSpecification.default_to_do_not_derive <datarobot.DatetimePartitioning>` value.

- Users can now submit multiple feature type transformations in a single batch request using :py:meth:`Project.batch_features_type_transform <datarobot.models.Project.batch_features_type_transform>`.

- :ref:`Advanced Tuning <advanced_tuning>` for non-Eureqa models (beta feature) is now enabled by default for all users.
  As of v2.17, all models are now supported other than blenders, open source, prime, scaleout, baseline and user-created.

- Information on feature clustering and the association strength between pairs of numeric or categorical features is now available.
  :py:meth:`Project.get_associations <datarobot.models.Project.get_associations>` can be used to retrieve pairwise feature association statistics and
  :py:meth:`Project.get_association_matrix_details <datarobot.models.Project.get_association_matrix_details>` can be used to get a sample of the actual values used to measure association strength.

Enhancements
************
- `number_of_do_not_derive_features` has been added to the :py:class:`datarobot.DatetimePartitioning <datarobot.DatetimePartitioning>` class to specify the number of features that are marked as excluded from derivation.
- Users with PyYAML>=5.1 will no longer receive a warning when using the `datarobot` package
- It is now possible to use files with unicode names for creating projects and prediction jobs.
- Users can now embed DataRobot-generated content in a :class:`ComplianceDocTemplate <datarobot.models.compliance_doc_template.ComplianceDocTemplate>` using keyword tags. :ref:`See here <compliance_doc_template_overview>` for more details.
- The field ``calendar_name`` has been added to :py:class:`datarobot.DatetimePartitioning <datarobot.DatetimePartitioning>` to display the name of the calendar used for a project.
- :ref:`Prediction intervals <prediction_intervals>` are now supported for start-end retrained models in a time series project.
- Previously, all backtests had to be run before :ref:`prediction intervals <prediction_intervals>` for a time series project could be requested with predictions.
  Now, backtests will be computed automatically if needed when prediction intervals are requested.

Bugfixes
********
- An issue affecting time series project creation for irregularly spaced dates has been fixed.
- :class:`ComplianceDocTemplate <datarobot.models.compliance_doc_template.ComplianceDocTemplate>` now supports empty text blocks in user sections.
- An issue when using :meth:`Predictions.get <datarobot.models.Predictions.get>` to retrieve predictions metadata has been fixed.

Documentation Changes
*********************
- An overview on working with :class:`ComplianceDocumentation <datarobot.models.compliance_documentation.ComplianceDocumentation>` and :class:`ComplianceDocTemplate <datarobot.models.compliance_doc_template.ComplianceDocTemplate>` has been created. :ref:`See here <compliance_documentation_overview>` for more details.


2.16.0
======

New Features
************
- Three new methods for Series Accuracy have been added to the :class:`DatetimeModel <datarobot.models.DatetimeModel>` class.

    - Start a request to calculate Series Accuracy with
      :meth:`DatetimeModel.compute_series_accuracy <datarobot.models.DatetimeModel.compute_series_accuracy>`
    - Once computed, Series Accuracy can be retrieved as a pandas.DataFrame using
      :meth:`DatetimeModel.get_series_accuracy_as_dataframe <datarobot.models.DatetimeModel.get_series_accuracy_as_dataframe>`
    - Or saved as a CSV using
      :meth:`DatetimeModel.download_series_accuracy_as_csv <datarobot.models.DatetimeModel.download_series_accuracy_as_csv>`

- Users can now access :ref:`prediction intervals <prediction_intervals>` data for each prediction with a :class:`DatetimeModel <datarobot.models.DatetimeModel>`.
  For each model, prediction intervals estimate the range of values DataRobot expects actual values of the target to fall within.
  They are similar to a confidence interval of a prediction, but are based on the residual errors measured during the
  backtesting for the selected model.

Enhancements
************
- Information on the effective feature derivation window is now available for :ref:`time series projects <time_series>` to specify the full span of historical data
  required at prediction time. It may be longer than the feature derivation window of the project depending on the differencing settings used.

  Additionally, more of the project partitioning settings are also available on the
  :class:`DatetimeModel <datarobot.models.DatetimeModel>` class.  The new attributes are:

    - ``effective_feature_derivation_window_start``
    - ``effective_feature_derivation_window_end``
    - ``forecast_window_start``
    - ``forecast_window_end``
    - ``windows_basis_unit``

- Prediction metadata is now included in the return of :meth:`Predictions.get <datarobot.models.Predictions.get>`

Documentation Changes
*********************
- Various typo and wording issues have been addressed.
- The example data that was meant to accompany the Time Series examples has been added to the
  zip file of the download in the :ref:`examples<examples_index>`.

2.15.1
======

Enhancements
************
- :meth:`CalendarFile.get_access_list <datarobot.CalendarFile.get_access_list>` has been added to the :class:`CalendarFile <datarobot.CalendarFile>` class to return a list of users with access to a calendar file.
- A ``role`` attribute has been added to the :class:`CalendarFile <datarobot.CalendarFile>` class to indicate the access level a current user has to a calendar file. For more information on the specific access levels, see the :ref:`sharing <sharing>` documentation.

Bugfixes
********
- Previously, attempting to retrieve the ``calendar_id`` of a project without a set target would result in an error.
  This has been fixed to return ``None`` instead.


2.15.0
======

New Features
************
- Previously available for only Eureqa models, Advanced Tuning methods and objects, including
  :meth:`Model.start_advanced_tuning_session <datarobot.models.Model.start_advanced_tuning_session>`,
  :meth:`Model.get_advanced_tuning_parameters <datarobot.models.Model.get_advanced_tuning_parameters>`,
  :meth:`Model.advanced_tune <datarobot.models.Model.advanced_tune>`, and
  :class:`AdvancedTuningSession <datarobot.models.advanced_tuning.AdvancedTuningSession>`,
  now support all models other than blender, open source, and user-created models.  Use of
  Advanced Tuning via API for non-Eureqa models is in beta and not available by default, but can be
  enabled.
- Calendar Files for time series projects can now be created and managed through the :class:`CalendarFile <datarobot.CalendarFile>` class.

Enhancements
************
* The dataframe returned from
  :py:meth:`datarobot.PredictionExplanations.get_all_as_dataframe` will now have
  each class label `class_X` be the same from row to row.
* The client is now more robust to networking issues by default. It will retry on more errors and respects `Retry-After` headers in HTTP 413, 429, and 503 responses.
* Added Forecast Distance blender for Time-Series projects configured with more than one Forecast
  Distance. It blends the selected models creating separate linear models for each Forecast Distance.
* :py:class:`Project <datarobot.models.Project>` can now be :ref:`shared <sharing>` with other users.
* :py:meth:`Project.upload_dataset <datarobot.models.Project.upload_dataset>` and :py:meth:`Project.upload_dataset_from_data_source <datarobot.models.Project.upload_dataset_from_data_source>` will return a :py:class:`PredictionDataset <datarobot.models.PredictionDataset>` with ``data_quality_warnings`` if potential problems exist around the uploaded dataset.
* ``relax_known_in_advance_features_check`` has been added to :py:meth:`Project.upload_dataset <datarobot.models.Project.upload_dataset>` and :py:meth:`Project.upload_dataset_from_data_source <datarobot.models.Project.upload_dataset_from_data_source>` to allow missing values from the known in advance features in the forecast window at prediction time.
* ``cross_series_group_by_columns`` has been added to :py:class:`datarobot.DatetimePartitioning <datarobot.DatetimePartitioning>` to allow users the ability to indicate how to further split series into related groups.
* Information retrieval for :py:class:`ROC Curve <datarobot.models.roc_curve.RocCurve>` has been extended to include ``fraction_predicted_as_positive``, ``fraction_predicted_as_negative``, ``lift_positive`` and ``lift_negative``

Bugfixes
********
* Fixes an issue where the client would not be usable if it could not be sure it was compatible with the configured
  server

API Changes
***********
- Methods for creating :py:class:`datarobot.models.Project`: `create_from_mysql`, `create_from_oracle`, and `create_from_postgresql`, deprecated in 2.11, have now been removed.
  Use :py:meth:`datarobot.models.Project.create_from_data_source` instead.
- :py:class:`datarobot.FeatureSettings <datarobot.FeatureSettings>` attribute `apriori`, deprecated in 2.11, has been removed.
  Use :py:class:`datarobot.FeatureSettings.known_in_advance <datarobot.FeatureSettings>` instead.
- :py:class:`datarobot.DatetimePartitioning <datarobot.DatetimePartitioning>` attribute `default_to_a_priori`, deprecated in 2.11, has been removed. Use
  :py:class:`datarobot.DatetimePartitioning.known_in_advance <datarobot.DatetimePartitioning>` instead.
- :py:class:`datarobot.DatetimePartitioningSpecification <datarobot.DatetimePartitioning>` attribute `default_to_a_priori`, deprecated in 2.11, has been removed.
  Use :py:class:`datarobot.DatetimePartitioningSpecification.known_in_advance <datarobot.DatetimePartitioning>`
  instead.

Deprecation Summary
*******************

Configuration Changes
*********************
- Now requires dependency on package `requests <https://pypi.org/project/requests/>`_  to be at least version 2.21.
- Now requires dependency on package `urllib3 <https://pypi.org/project/urllib3/>`_  to be at least version 1.24.

Documentation Changes
*********************
- Advanced model insights notebook extended to contain information on visualisation of cumulative gains and lift charts.

2.14.2
======

Bugfixes
********
- Fixed an issue where searches of the HTML documentation would sometimes hang indefinitely

Documentation Changes
*********************
- Python3 is now the primary interpreter used to build the docs (this does not affect the ability to use the
  package with Python2)

2.14.1
======

Documentation Changes
*********************
 - Documentation for the Model Deployment interface has been removed after the corresponding interface was removed in 2.13.0.

2.14.0
======
New Features
************
- The new method :meth:`Model.get_supported_capabilities <datarobot.models.Model.get_supported_capabilities>`
  retrieves a summary of the capabilities supported by a particular model,
  such as whether it is eligible for Prime and whether it has word cloud data available.
- New class for working with model compliance documentation feature of DataRobot:
  :class:`ComplianceDocumentation <datarobot.models.compliance_documentation.ComplianceDocumentation>`
- New class for working with compliance documentation templates:
  :class:`ComplianceDocTemplate <datarobot.models.compliance_doc_template.ComplianceDocTemplate>`
- New class :py:class:`FeatureHistogram <datarobot.models.FeatureHistogram>` has been added to
  retrieve feature histograms for a requested maximum bin count
- Time series projects now support binary classification targets.
- Cross series features can now be created within time series multiseries projects using the
  ``use_cross_series_features`` and ``aggregation_type`` attributes of the
  :py:class:`datarobot.DatetimePartitioningSpecification
  <datarobot.DatetimePartitioningSpecification>`.
  See the :ref:`Time Series <time_series>` documentation for more info.


Enhancements
************
- Client instantiation now checks the endpoint configuration and provides more informative error messages.
  It also automatically corrects HTTP to HTTPS if the server responds with a redirect to HTTPS.
- :meth:`Project.upload_dataset <datarobot.models.Project.upload_dataset>` and :meth:`Project.create <datarobot.models.Project.create>`
  now accept an optional parameter of ``dataset_filename`` to specify a file name for the dataset.
  This is ignored for url and file path sources.
- New optional parameter `fallback_to_parent_insights` has been added to :meth:`Model.get_lift_chart <datarobot.models.Model.get_lift_chart>`,
  :meth:`Model.get_all_lift_charts <datarobot.models.Model.get_all_lift_charts>`, :meth:`Model.get_confusion_chart <datarobot.models.Model.get_confusion_chart>`,
  :meth:`Model.get_all_confusion_charts <datarobot.models.Model.get_all_confusion_charts>`, :meth:`Model.get_roc_curve <datarobot.models.Model.get_roc_curve>`,
  and :meth:`Model.get_all_roc_curves <datarobot.models.Model.get_all_roc_curves>`.  When `True`, a frozen model with
  missing insights will attempt to retrieve the missing insight data from its parent model.
- New ``number_of_known_in_advance_features`` attribute has been added to the
  :py:class:`datarobot.DatetimePartitioning <datarobot.DatetimePartitioning>` class.
  The attribute specifies number of features that are marked as known in advance.
- :meth:`Project.set_worker_count <datarobot.models.Project.set_worker_count>` can now update the worker count on
  a project to the maximum number available to the user.
- :ref:`Recommended Models API <recommended_models>` can now be used to retrieve
  model recommendations for datetime partitioned projects
- Timeseries projects can now accept feature derivation and forecast windows intervals in terms of
  number of the rows rather than a fixed time unit. :class:`DatetimePartitioningSpecification <datarobot.DatetimePartitioningSpecification>`
  and :meth:`Project.set_target <datarobot.models.Project.set_target>` support new optional parameter `windowsBasisUnit`, either 'ROW' or detected time unit.
- Timeseries projects can now accept feature derivation intervals, forecast windows, forecast points and prediction start/end dates in milliseconds.
- :class:`DataSources <datarobot.DataSource>` and :class:`DataStores <datarobot.DataStore>` can now
  be :ref:`shared <sharing>` with other users.
- Training predictions for datetime partitioned projects now support the new data subset
  `dr.enums.DATA_SUBSET.ALL_BACKTESTS` for requesting the predictions for all backtest validation
  folds.

API Changes
*******************
- The model recommendation type "Recommended" (deprecated in version 2.13.0) has been removed.

Documentation Changes
*********************

- Example notebooks have been updated:
    - Notebooks now work in Python 2 and Python 3
    - A notebook illustrating time series capability has been added
    - The financial data example has been replaced with an updated introductory example.
- To supplement the embedded Python notebooks in both the PDF and HTML docs bundles, the notebook files and supporting data can now be downloaded from the HTML docs bundle.
- Fixed a minor typo in the code sample for ``get_or_request_feature_impact``

2.13.0
======

New Features
************
- The new method :meth:`Model.get_or_request_feature_impact <datarobot.models.Model.get_or_request_feature_impact>` functionality will attempt to request feature impact
  and return the newly created feature impact object or the existing object so two calls are no longer required.
- New methods and objects, including
  :meth:`Model.start_advanced_tuning_session <datarobot.models.Model.start_advanced_tuning_session>`,
  :meth:`Model.get_advanced_tuning_parameters <datarobot.models.Model.get_advanced_tuning_parameters>`,
  :meth:`Model.advanced_tune <datarobot.models.Model.advanced_tune>`, and
  :class:`AdvancedTuningSession <datarobot.models.advanced_tuning.AdvancedTuningSession>`,
  were added to support the setting of Advanced Tuning parameters. This is currently supported for
  Eureqa models only.
- New ``is_starred`` attribute has been added to the :py:class:`Model <datarobot.models.Model>` class. The attribute
  specifies whether a model has been marked as starred by user or not.
- Model can be marked as starred or being unstarred with :meth:`Model.star_model <datarobot.models.Model.star_model>` and :meth:`Model.unstar_model <datarobot.models.Model.unstar_model>`.
- When listing models with :meth:`Project.get_models <datarobot.models.Project.get_models>`, the model list can now be filtered by the ``is_starred`` value.
- A custom prediction threshold may now be configured for each model via :meth:`Model.set_prediction_threshold <datarobot.models.Model.set_prediction_threshold>`.  When making
  predictions in binary classification projects, this value will be used when deciding between the positive and negative classes.
- :meth:`Project.check_blendable <datarobot.models.Project.check_blendable>` can be used to confirm if a particular group of models are eligible for blending as
  some are not, e.g. scaleout models and datetime models with different training lengths.
- Individual cross validation scores can be retrieved for new models using :meth:`Model.get_cross_validation_scores <datarobot.models.Model.get_cross_validation_scores>`.

Enhancements
************
- Python 3.7 is now supported.
- Feature impact now returns not only the impact score for the features but also whether they were
  detected to be redundant with other high-impact features.
- A new ``is_blocked`` attribute has been added to the :py:class:`Job <datarobot.models.Job>`
  class, specifying whether a job is blocked from execution because one or more dependencies are not
  yet met.
- The :py:class:`Featurelist <datarobot.models.Featurelist>` object now has new attributes reporting
  its creation time, whether it was created by a user or by DataRobot, and the number of models
  using the featurelist, as well as a new description field.
- Featurelists can now be renamed and have their descriptions updated with
  :py:meth:`Featurelist.update <datarobot.models.Featurelist.update>` and
  :py:meth:`ModelingFeaturelist.update <datarobot.models.ModelingFeaturelist.update>`.
- Featurelists can now be deleted with
  :py:meth:`Featurelist.delete <datarobot.models.Featurelist.delete>`
  and :py:meth:`ModelingFeaturelist.delete <datarobot.models.ModelingFeaturelist.delete>`.
- :meth:`ModelRecommendation.get <datarobot.models.ModelRecommendation.get>` now accepts an optional
  parameter of type ``datarobot.enums.RECOMMENDED_MODEL_TYPE`` which can be used to get a specific
  kind of recommendation.
- Previously computed predictions can now be listed and retrieved with the
  :class:`Predictions <datarobot.models.Predictions>` class, without requiring a
  reference to the original :py:class:`PredictJob <datarobot.models.PredictJob>`.

Bugfixes
********
- The Model Deployment interface which was previously visible in the client has been removed to
  allow the interface to mature, although the raw API is available as a "beta" API without full
  backwards compatibility support.

API Changes
***********
- Added support for retrieving the Pareto Front of a Eureqa model. See
  :py:class:`ParetoFront <datarobot.models.pareto_front.ParetoFront>`.
- A new recommendation type "Recommended for Deployment" has been added to
  :py:class:`ModelRecommendation <datarobot.models.ModelRecommendation>` which is now returns as the
  default recommended model when available. See :ref:`model_recommendation`.

Deprecation Summary
*******************
- The feature previously referred to as "Reason Codes" has been renamed to "Prediction
  Explanations", to provide increased clarity and accessibility. The old
  :py:class:`ReasonCodes <datarobot.ReasonCodes>` interface has been deprecated and replaced with
  :py:class:`PredictionExplanations <datarobot.PredictionExplanations>`.
- The recommendation type "Recommended" is deprecated and  will no longer be returned
  in v2.14 of the API.

Documentation Changes
*********************

- Added a new documentation section :ref:`model_recommendation`.
- Time series projects support multiseries as well as single series data. They are now documented in
  the :ref:`Time Series Projects <time_series>` documentation.

2.12.0
======

New Features
************
- Some models now have Missing Value reports allowing users with access to uncensored blueprints to
  retrieve a detailed breakdown of how numeric imputation and categorical converter tasks handled
  missing values. See the :ref:`documentation <missing_values_report>` for more information on the
  report.

2.11.0
======

New Features
************
- The new ``ModelRecommendation`` class can be used to retrieve the recommended models for a
  project.
- A new helper method cross_validate was added to class Model. This method can be used to request
  Model's Cross Validation score.
- Training a model with monotonic constraints is now supported. Training with monotonic
  constraints allows users to force models to learn monotonic relationships with respect to some features and the target. This helps users create accurate models that comply with regulations (e.g. insurance, banking). Currently, only certain blueprints (e.g. xgboost) support this feature, and it is only supported for regression and binary classification projects.
- DataRobot now supports "Database Connectivity", allowing databases to be used
  as the source of data for projects and prediction datasets. The feature works
  on top of the JDBC standard, so a variety of databases conforming to that standard are available;
  a list of databases with tested support for DataRobot is available in the user guide
  in the web application. See :ref:`Database Connectivity <database_connectivity_overview>`
  for details.
- Added a new feature to retrieve feature logs for time series projects. Check
  :py:meth:`datarobot.DatetimePartitioning.feature_log_list` and
  :py:meth:`datarobot.DatetimePartitioning.feature_log_retrieve` for details.

API Changes
***********
- New attributes supporting monotonic constraints have been added to the
  :py:class:`AdvancedOptions <datarobot.helpers.AdvancedOptions>`,
  :py:class:`Project <datarobot.models.Project>`,
  :py:class:`Model <datarobot.models.Model>`, and :py:class:`Blueprint <datarobot.models.Blueprint>`
  classes. See :ref:`monotonic constraints<monotonic_constraints>` for more information on how to
  configure monotonic constraints.
- New parameters `predictions_start_date` and `predictions_end_date` added to
  :py:meth:`Project.upload_dataset <datarobot.models.Project.upload_dataset>` to support bulk
  predictions upload for time series projects.

Deprecation Summary
*******************
- Methods for creating :py:class:`datarobot.models.Project`: `create_from_mysql`, `create_from_oracle`, and `create_from_postgresql`, have been deprecated and will be removed in 2.14.
  Use :py:meth:`datarobot.models.Project.create_from_data_source` instead.
- :py:class:`datarobot.FeatureSettings <datarobot.FeatureSettings>` attribute `apriori`, has been deprecated and will be removed in 2.14.
  Use :py:class:`datarobot.FeatureSettings.known_in_advance <datarobot.FeatureSettings>` instead.
- :py:class:`datarobot.DatetimePartitioning <datarobot.DatetimePartitioning>` attribute `default_to_a_priori`, has been deprecated and will be removed in 2.14.
  :py:class:`datarobot.DatetimePartitioning.known_in_advance <datarobot.DatetimePartitioning>` instead.
- :py:class:`datarobot.DatetimePartitioningSpecification <datarobot.DatetimePartitioning>` attribute `default_to_a_priori`, has been deprecated and will be removed in 2.14.
  Use :py:class:`datarobot.DatetimePartitioningSpecification.known_in_advance <datarobot.DatetimePartitioning>`
  instead.

Configuration Changes
*********************
- Retry settings compatible with those offered by urllib3's `Retry <https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.retry.Retry>`_
  interface can now be configured. By default, we will now retry connection errors that prevented requests from arriving at the server.

Documentation Changes
*********************
- "Advanced Model Insights" example has been updated to properly handle bin weights when rebinning.

2.9.0
=====

New Features
************
- New ``ModelDeployment`` class can be used to track status and health of models deployed for
  predictions.

Enhancements
************
- DataRobot API now supports creating 3 new blender types - Random Forest, TensorFlow, LightGBM.
- Multiclass projects now support blenders creation for 3 new blender types as well as Average
  and ENET blenders.
- Models can be trained by requesting a particular row count using the new ``training_row_count``
  argument with `Project.train`, `Model.train` and `Model.request_frozen_model` in non-datetime
  partitioned projects, as an alternative to the previous option of specifying a desired
  percentage of the project dataset. Specifying model size by row count is recommended when
  the float precision of ``sample_pct`` could be problematic, e.g. when training on a small
  percentage of the dataset or when training up to partition boundaries.
- New attributes ``max_train_rows``, ``scaleout_max_train_pct``, and ``scaleout_max_train_rows``
  have been added to :py:class:`Project <datarobot.models.Project>`. ``max_train_rows`` specified the equivalent
  value to the existing ``max_train_pct`` as a row count. The scaleout fields can be used to see how
  far scaleout models can be trained on projects, which for projects taking advantage of scalable
  ingest may exceed the limits on the data available to non-scaleout blueprints.
- Individual features can now be marked as a priori or not a priori using the new `feature_settings`
  attribute when setting the target or specifying datetime partitioning settings on time
  series projects. Any features not specified in the `feature_settings` parameter will be
  assigned according to the `default_to_a_priori` value.
- Three new options have been made available in the
  :py:class:`datarobot.DatetimePartitioningSpecification` class to fine-tune how time-series projects
  derive modeling features. `treat_as_exponential` can control whether data is analyzed as
  an exponential trend and transformations like log-transform are applied.
  `differencing_method` can control which differencing method to use for stationary data.
  `periodicities` can be used to specify periodicities occuring within the data.
  All are optional and defaults will be chosen automatically if they are unspecified.

API Changes
***********
- Now ``training_row_count`` is available on non-datetime models as well as "rowCount" based
  datetime models. It reports the number of rows used to train the model (equivalent to
  ``sample_pct``).
- Features retrieved from ``Feature.get`` now include ``target_leakage``.

2.8.1
=====

Bugfixes
********
- The documented default connect_timeout will now be correctly set for all configuration mechanisms,
  so that requests that fail to reach the DataRobot server in a reasonable amount of time will now
  error instead of hanging indefinitely. If you observe that you have started seeing
  ``ConnectTimeout`` errors, please configure your connect_timeout to a larger value.
- Version of ``trafaret`` library this package depends on is now pinned to ``trafaret>=0.7,<1.1``
  since versions outside that range are known to be incompatible.


2.8.0
=====

New Features
************
- The DataRobot API supports the creation, training, and predicting of multiclass classification
  projects. DataRobot, by default, handles a dataset with a numeric target column as regression.
  If your data has a numeric cardinality of fewer than 11 classes, you can override this behavior to
  instead create a multiclass classification project from the data. To do so, use the set_target
  function, setting target_type='Multiclass'. If DataRobot recognizes your data as categorical, and
  it has fewer than 11 classes, using multiclass will create a project that classifies which label
  the data belongs to.
- The DataRobot API now includes Rating Tables. A rating table is an exportable csv representation
  of a model. Users can influence predictions by modifying them and creating a new model with the
  modified table. See the :ref:`documentation<rating_table>` for more information on how to use
  rating tables.
- `scaleout_modeling_mode` has been added to the `AdvancedOptions` class
  used when setting a project target. It can be used to control whether
  scaleout models appear in the autopilot and/or available blueprints.
  Scaleout models are only supported in the Hadoop enviroment with
  the corresponding user permission set.
- A new premium add-on product, Time Series, is now available. New projects can be created as time series
  projects which automatically derive features from past data and forecast the future. See the
  :ref:`time series documentation<time_series>` for more information.
- The `Feature` object now returns the EDA summary statistics (i.e., mean, median, minum, maximum,
  and standard deviation) for features where this is available (e.g., numeric, date, time,
  currency, and length features). These summary statistics will be formatted in the same format
  as the data it summarizes.
- The DataRobot API now supports Training Predictions workflow. Training predictions are made by a
  model for a subset of data from original dataset. User can start a job which will make those
  predictions and retrieve them. See the :ref:`documentation<training_predictions>`
  for more information on how to use training predictions.
- DataRobot now supports retrieving a :ref:`model blueprint chart<model_blueprint_chart>` and a
  :ref:`model blueprint docs<model_blueprint_doc>`.
- With the introduction of Multiclass Classification projects, DataRobot needed a better way to
  explain the performance of a multiclass model so we created a new Confusion Chart. The API
  now supports retrieving and interacting with confusion charts.

Enhancements
************
- `DatetimePartitioningSpecification` now includes the optional `disable_holdout` flag that can
  be used to disable the holdout fold when creating a project with datetime partitioning.
- When retrieving reason codes on a project using an exposure column, predictions that are adjusted
  for exposure can be retrieved.
- File URIs can now be used as sourcedata when creating a project or uploading a prediction dataset.
  The file URI must refer to an allowed location on the server, which is configured as described in
  the user guide documentation.
- The advanced options available when setting the target have been extended to include the new
  parameter 'events_count' as a part of the AdvancedOptions object to allow specifying the
  events count column. See the user guide documentation in the webapp for more information
  on events count.
- PredictJob.get_predictions now returns predicted probability for each class in the dataframe.
- PredictJob.get_predictions now accepts prefix parameter to prefix the classes name returned in the
  predictions dataframe.

API Changes
***********
- Add `target_type` parameter to set_target() and start(), used to override the project default.

2.7.2
=====

Documentation Changes
*********************

- Updated link to the publicly hosted documentation.

2.7.1
=====

Documentation Changes
*********************

- Online documentation hosting has migrated from PythonHosted to Read The Docs. Minor code changes
  have been made to support this.

2.7.0
=====

New Features
************
- Lift chart data for models can be retrieved using the `Model.get_lift_chart` and
  `Model.get_all_lift_charts` methods.
- ROC curve data for models in classification projects can be retrieved using the
  `Model.get_roc_curve` and `Model.get_all_roc_curves` methods.
- Semi-automatic autopilot mode is removed.
- Word cloud data for text processing models can be retrieved using `Model.get_word_cloud` method.
- Scoring code JAR file can be downloaded for models supporting code generation.

Enhancements
************
- A `__repr__` method has been added to the `PredictionDataset` class to improve readability when
  using the client interactively.
- `Model.get_parameters` now includes an additional key in the derived features it includes,
  showing the coefficients for individual stages of multistage models (e.g. Frequency-Severity
  models).
- When training a `DatetimeModel` on a window of data, a `time_window_sample_pct` can be specified
  to take a uniform random sample of the training data instead of using all data within the window.
- Installing of DataRobot package now has an "Extra Requirements" section that will install all of
  the dependencies needed to run the example notebooks.

Documentation Changes
*********************
- A new example notebook describing how to visualize some of the newly available model insights
  including lift charts, ROC curves, and word clouds has been added to the examples section.
- A new section for `Common Issues` has been added to `Getting Started` to help debug issues related to client installation and usage.


2.6.1
=====

Bugfixes
********

- Fixed a bug with `Model.get_parameters` raising an exception on some valid parameter values.

Documentation Changes
*********************

- Fixed sorting order in Feature Impact example code snippet.

2.6.0
=====

New Features
************
- A new partitioning method (datetime partitioning) has been added. The recommended workflow is to
  preview the partitioning by creating a `DatetimePartitioningSpecification` and passing it into
  `DatetimePartitioning.generate`, inspect the results and adjust as needed for the specific project
  dataset by adjusting the `DatetimePartitioningSpecification` and re-generating, and then set the
  target by passing the final `DatetimePartitioningSpecification` object to the partitioning_method
  parameter of `Project.set_target`.
- When interacting with datetime partitioned projects, `DatetimeModel` can be used to access more
  information specific to models in datetime partitioned projects. See
  :ref:`the documentation<datetime_modeling_workflow>` for more information on differences in the
  modeling workflow for datetime partitioned projects.
- The advanced options available when setting the target have been extended to include the new
  parameters 'offset' and 'exposure' (part of the AdvancedOptions object) to allow specifying
  offset and exposure columns to apply to predictions generated by models within the project.
  See the user guide documentation in the webapp for more information on offset
  and exposure columns.
- Blueprints can now be retrieved directly by project_id and blueprint_id via `Blueprint.get`.
- Blueprint charts can now be retrieved directly by project_id and blueprint_id via
  `BlueprintChart.get`. If you already have an instance of `Blueprint` you can retrieve its
  chart using `Blueprint.get_chart`.
- Model parameters can now be retrieved using `ModelParameters.get`. If you already have an
  instance of `Model` you can retrieve its parameters using `Model.get_parameters`.
- Blueprint documentation can now be retrieved using `Blueprint.get_documents`. It will contain
  information about the task, its parameters and (when available) links and references to
  additional sources.
- The DataRobot API now includes Reason Codes. You can now compute reason codes for prediction
  datasets. You are able to specify thresholds on which rows to compute reason codes for to speed
  up computation by skipping rows based on the predictions they generate. See the reason codes
  :ref:`documentation<reason_codes>` for more information.

Enhancements
************

- A new parameter has been added to the `AdvancedOptions` used with `Project.set_target`. By
  specifying `accuracyOptimizedMb=True` when creating `AdvancedOptions`, longer-running models
  that may have a high accuracy will be included in the autopilot and made available to run
  manually.
- A new option for `Project.create_type_transform_feature` has been added which explicitly
  truncates data when casting numerical data as categorical data.
- Added 2 new blenders for projects that use MAD or Weighted MAD as a metric. The MAE blender uses
  BFGS optimization to find linear weights for the blender that minimize mean absolute error
  (compared to the GLM blender, which finds linear weights that minimize RMSE), and the MAEL1
  blender uses BFGS optimization to find linear weights that minimize MAE + a L1 penalty on the
  coefficients (compared to the ENET blender, which minimizes RMSE + a combination of the L1 and L2
  penalty on the coefficients).

Bugfixes
********

- Fixed a bug (affecting Python 2 only) with printing any model (including frozen and prime models)
  whose model_type is not ascii.
- FrozenModels were unable to correctly use methods inherited from Model. This has been fixed.
- When calling `get_result` for a Job, ModelJob, or PredictJob that has errored, `AsyncProcessUnsuccessfulError` will now be raised instead of `JobNotFinished`, consistently with the behaviour of `get_result_when_complete`.

Deprecation Summary
*******************

- Support for the experimental Recommender Problems projects has been removed. Any code relying on
  `RecommenderSettings` or the `recommender_settings` argument of `Project.set_target` and
  `Project.start` will error.
- ``Project.update``, deprecated in v2.2.32, has been removed in favor of specific updates:
  ``rename``, ``unlock_holdout``, ``set_worker_count``.

Documentation Changes
*********************

- The link to Configuration from the Quickstart page has been fixed.

2.5.1
=====

Bugfixes
********

- Fixed a bug (affecting Python 2 only) with printing blueprints  whose names are
  not ascii.
- Fixed an issue where the weights column (for weighted projects) did not appear
  in the `advanced_options` of a `Project`.


2.5.0
=====

New Features
************

- Methods to work with blender models have been added. Use `Project.blend` method to create new blenders,
  `Project.get_blenders` to get the list of existing blenders and `BlenderModel.get` to retrieve a model
  with blender-specific information.
- Projects created via the API can now use smart downsampling when setting the target by passing
  `smart_downsampled` and `majority_downsampling_rate` into the `AdvancedOptions` object used with
  `Project.set_target`. The smart sampling options used with an existing project will be available
  as part of `Project.advanced_options`.
- Support for frozen models, which use tuning parameters from a parent model for more efficient
  training, has been added. Use `Model.request_frozen_model` to create a new frozen model,
  `Project.get_frozen_models` to get the list of existing frozen models and `FrozenModel.get` to
  retrieve a particular frozen model.

Enhancements
************

- The inferred date format (e.g. "%Y-%m-%d %H:%M:%S") is now included in the Feature object. For
  non-date features, it will be None.
- When specifying the API endpoint in the configuration, the client will now behave correctly for
  endpoints with and without trailing slashes.


2.4.0
=====

New Features
************

- The premium add-on product `DataRobot Prime` has been added. You can now approximate a model
  on the leaderboard and download executable code for it. See documentation for further details, or
  talk to your account representative if the feature is not available on your account.
- (Only relevant for on-premise users with a Standalone Scoring cluster.) Methods
  (`request_transferable_export` and `download_export`) have been added to the `Model` class for exporting models (which will only work if model export is turned on). There is a new class `ImportedModel` for managing imported models on a Standalone
  Scoring cluster.
- It is now possible to create projects from a WebHDFS, PostgreSQL, Oracle or MySQL data source. For more information see the
  documentation for the relevant `Project` classmethods: `create_from_hdfs`, `create_from_postgresql`,
  `create_from_oracle` and `create_from_mysql`.
- `Job.wait_for_completion`, which waits for a job to complete without returning anything, has been added.

Enhancements
************

- The client will now check the API version offered by the server specified in configuration, and
  give a warning if the client version is newer than the server version. The DataRobot server is
  always backwards compatible with old clients, but new clients may have functionality that is
  not implemented on older server versions. This issue mainly affects users with on-premise deployments
  of DataRobot.

Bugfixes
********

- Fixed an issue where `Model.request_predictions` might raise an error when predictions finished
  very quickly instead of returning the job.

API Changes
***********

- To set the target with quickrun autopilot, call `Project.set_target` with `mode=AUTOPILOT_MODE.QUICK` instead of
  specifying `quickrun=True`.

Deprecation Summary
*******************

- Semi-automatic mode for autopilot has been deprecated and will be removed in 3.0.
  Use manual or fully automatic instead.
- Use of the `quickrun` argument in `Project.set_target` has been deprecated and will be removed in
  3.0. Use `mode=AUTOPILOT_MODE.QUICK` instead.

Configuration Changes
*********************

- It is now possible to control the SSL certificate verification by setting the parameter
  `ssl_verify` in the config file.

Documentation Changes
*********************

- The "Modeling Airline Delay" example notebook has been updated to work with the new 2.3
  enhancements.
- Documentation for the generic `Job` class has been added.
- Class attributes are now documented in the `API Reference` section of the documentation.
- The changelog now appears in the documentation.
- There is a new section dedicated to configuration, which lists all of the configuration
  options and their meanings.


2.3.0
=====

New Features
************

- The DataRobot API now includes Feature Impact, an approach to measuring the relevance of each feature
  that can be applied to any model. The `Model` class now includes methods `request_feature_impact`
  (which creates and returns a feature impact job) and `get_feature_impact` (which can retrieve completed feature impact results).
- A new improved workflow for predictions now supports first uploading a dataset via `Project.upload_dataset`,
  then requesting predictions via `Model.request_predictions`. This allows us to better support predictions on
  larger datasets and non-ascii files.
- Datasets previously uploaded for predictions (represented by the `PredictionDataset` class) can be listed from
  `Project.get_datasets` and retrieve and deleted via `PredictionDataset.get` and `PredictionDataset.delete`.
- You can now create a new feature by re-interpreting the type of an existing feature in a project by
  using the `Project.create_type_transform_feature` method.
- The `Job` class now includes a `get` method for retrieving a job and a `cancel` method for
  canceling a job.
- All of the jobs classes (`Job`, `ModelJob`, `PredictJob`) now include the following new methods:
  `refresh` (for refreshing the data in the job object), `get_result` (for getting the
  completed resource resulting from the job), and `get_result_when_complete` (which waits until the job
  is complete and returns the results, or times out).
- A new method `Project.refresh` can be used to update
  `Project` objects with the latest state from the server.
- A new function `datarobot.async.wait_for_async_resolution` can be
  used to poll for the resolution of any generic asynchronous operation
  on the server.


Enhancements
************

- The `JOB_TYPE` enum now includes `FEATURE_IMPACT`.
- The `QUEUE_STATUS` enum now includes `ABORTED` and `COMPLETED`.
- The `Project.create` method now has a `read_timeout` parameter which can be used to
  keep open the connection to DataRobot while an uploaded file is being processed.
  For very large files this time can be substantial. Appropriately raising this value
  can help avoid timeouts when uploading large files.
- The method `Project.wait_for_autopilot` has been enhanced to error if
  the project enters a state where autopilot may not finish. This avoids
  a situation that existed previously where users could wait
  indefinitely on their project that was not going to finish. However,
  users are still responsible to make sure a project has more than
  zero workers, and that the queue is not paused.
- Feature.get now supports retrieving features by feature name. (For backwards compatibility,
  feature IDs are still supported until 3.0.)
- File paths that have unicode directory names can now be used for
  creating projects and PredictJobs. The filename itself must still
  be ascii, but containing directory names can have other encodings.
- Now raises more specific JobAlreadyRequested exception when we refuse a model fitting request as a duplicate.
  Users can explicitly catch this exception if they want it to be ignored.
- A `file_name` attribute has been added to the `Project` class, identifying the file name
  associated with the original project dataset. Note that if the project was created from
  a data frame, the file name may not be helpful.
- The connect timeout for establishing a connection to the server can now be set directly. This can be done in the
  yaml configuration of the client, or directly in the code. The default timeout has been lowered from 60 seconds
  to 6 seconds, which will make detecting a bad connection happen much quicker.

Bugfixes
********

- Fixed a bug (affecting Python 2 only) with printing features and featurelists whose names are
  not ascii.

API Changes
***********

- Job class hierarchy is rearranged to better express the relationship between these objects. See
  documentation for `datarobot.models.job` for details.
- `Featurelist` objects now have a `project_id` attribute to indicate which project they belong
  to. Directly accessing the `project` attribute of a `Featurelist` object is now deprecated
- Support INI-style configuration, which was deprecated in v2.1, has been removed. yaml is the only supported
  configuration format.
- The method `Project.get_jobs` method, which was deprecated in v2.1, has been removed. Users should use
  the `Project.get_model_jobs` method instead to get the list of model jobs.

Deprecation Summary
*******************

- `PredictJob.create` has been deprecated in favor of the alternate workflow using `Model.request_predictions`.
- Feature.converter (used internally for object construction) has been made private.
- Model.fetch_resource_data has been deprecated and will be removed in 3.0. To fetch a model from
   its ID, use Model.get.
- The ability to use Feature.get with feature IDs (rather than names) is deprecated and will
  be removed in 3.0.
- Instantiating a `Project`, `Model`, `Blueprint`, `Featurelist`, or `Feature` instance from a `dict`
  of data is now deprecated. Please use the `from_data` classmethod of these classes instead. Additionally,
  instantiating a `Model` from a tuple or by using the keyword argument `data` is also deprecated.
- Use of the attribute `Featurelist.project` is now deprecated. You can use the `project_id`
  attribute of a `Featurelist` to instantiate a `Project` instance using `Project.get`.
- Use of the attributes `Model.project`, `Model.blueprint`, and `Model.featurelist` are all deprecated now
  to avoid use of partially instantiated objects. Please use the ids of these objects instead.
- Using a `Project` instance as an argument in `Featurelist.get` is now deprecated.
  Please use a project_id instead. Similarly, using a `Project` instance in `Model.get` is also deprecated,
  and a project_id should be used in its place.

Configuration Changes
*********************

- Previously it was possible (though unintended) that the client configuration could be mixed through
  environment variables, configuration files, and arguments to `datarobot.Client`. This logic is now
  simpler - please see the `Getting Started` section of the documentation for more information.


2.2.33
======

Bugfixes
********

- Fixed a bug with non-ascii project names using the package with Python 2.
- Fixed an error that occurred when printing projects that had been constructed from an ID only or
  printing printing models that had been constructed from a tuple (which impacted printing PredictJobs).
- Fixed a bug with project creation from non-ascii file names. Project creation from non-ascii file names
  is not supported, so this now raises a more informative exception. The project name is no longer used as
  the file name in cases where we do not have a file name, which prevents non-ascii project names from
  causing problems in those circumstances.
- Fixed a bug (affecting Python 2 only) with printing projects, features, and featurelists whose names are
  not ascii.


2.2.32
======

New Features
************

- ``Project.get_features`` and ``Feature.get`` methods have been added for feature retrieval.
- A generic ``Job`` entity has been added for use in retrieving the entire queue at once. Calling
  ``Project.get_all_jobs`` will retrieve all (appropriately filtered) jobs from the queue. Those
  can be cancelled directly as generic jobs, or transformed into instances of the specific
  job class using ``ModelJob.from_job`` and ``PredictJob.from_job``, which allow all functionality
  previously available via the ModelJob and PredictJob interfaces.
- ``Model.train`` now supports ``featurelist_id`` and ``scoring_type`` parameters, similar to
  ``Project.train``.

Enhancements
************

- Deprecation warning filters have been updated. By default, a filter will be added ensuring that
  usage of deprecated features will display a warning once per new usage location. In order to
  hide deprecation warnings, a filter like
  `warnings.filterwarnings('ignore', category=DataRobotDeprecationWarning)`
  can be added to a script so no such warnings are shown. Watching for deprecation warnings
  to avoid reliance on deprecated features is recommended.
- If your client is misconfigured and does not specify an endpoint, the cloud production server is
  no longer used as the default as in many cases this is not the correct default.
- This changelog is now included in the distributable of the client.

Bugfixes
********

- Fixed an issue where updating the global client would not affect existing objects with cached clients.
  Now the global client is used for every API call.
- An issue where mistyping a filepath for use in a file upload has been resolved. Now an error will be
  raised if it looks like the raw string content for modeling or predictions is just one single line.

API Changes
***********

- Use of username and password to authenticate is no longer supported - use an API token instead.
- Usage of ``start_time`` and ``finish_time`` parameters in ``Project.get_models`` is not
  supported both in filtering and ordering of models
- Default value of ``sample_pct`` parameter of ``Model.train`` method is now ``None`` instead of ``100``.
  If the default value is used, models will be trained with all of the available *training* data based on
  project configuration, rather than with entire dataset including holdout for the previous default value
  of ``100``.
- ``order_by`` parameter of ``Project.list`` which was deprecated in v2.0 has been removed.
- ``recommendation_settings`` parameter of ``Project.start`` which was deprecated in v0.2 has been removed.
- ``Project.status`` method which was deprecated in v0.2 has been removed.
- ``Project.wait_for_aim_stage`` method which was deprecated in v0.2 has been removed.
- ``Delay``, ``ConstantDelay``, ``NoDelay``, ``ExponentialBackoffDelay``, ``RetryManager``
  classes from ``retry`` module which were deprecated in v2.1 were removed.
- Package renamed to ``datarobot``.

Deprecation Summary
*******************

- ``Project.update`` deprecated in favor of specific updates:
  ``rename``, ``unlock_holdout``, ``set_worker_count``.

Documentation Changes
*********************

- A new use case involving financial data has been added to the ``examples`` directory.
- Added documentation for the partition methods.

2.1.31
======

Bugfixes
********

- In Python 2, using a unicode token to instantiate the client will
  now work correctly.


2.1.30
======

Bugfixes
********

- The minimum required version of ``trafaret`` has been upgraded to 0.7.1
  to get around an incompatibility between it and ``setuptools``.


2.1.29
======

Enhancements
************

- Minimal used version of ``requests_toolbelt`` package changed from 0.4 to 0.6


2.1.28
======

New Features
************

- Default to reading YAML config file from `~/.config/datarobot/drconfig.yaml`
- Allow `config_path` argument to client
- ``wait_for_autopilot`` method added to Project. This method can be used to
  block execution until autopilot has finished running on the project.
- Support for specifying which featurelist to use with initial autopilot in
  ``Project.set_target``
- ``Project.get_predict_jobs`` method has been added, which looks up all prediction jobs for a
  project
- ``Project.start_autopilot`` method has been added, which starts autopilot on
  specified featurelist
- The schema for ``PredictJob`` in DataRobot API v2.1 now includes a ``message``. This attribute has
  been added to the PredictJob class.
- ``PredictJob.cancel`` now exists to cancel prediction jobs, mirroring ``ModelJob.cancel``
- ``Project.from_async`` is a new classmethod that can be used to wait for an async resolution
  in project creation. Most users will not need to know about it as it is used behind the scenes
  in ``Project.create`` and ``Project.set_target``, but power users who may run
  into periodic connection errors will be able to catch the new ProjectAsyncFailureError
  and decide if they would like to resume waiting for async process to resolve

Enhancements
************

- ``AUTOPILOT_MODE`` enum now uses string names for autopilot modes instead of numbers

Deprecation Summary
*******************

- ``ConstantDelay``, ``NoDelay``, ``ExponentialBackoffDelay``, and ``RetryManager`` utils are now deprecated
- INI-style config files are now deprecated (in favor of YAML config files)
- Several functions in the `utils` submodule are now deprecated (they are
  being moved elsewhere and are not considered part of the public interface)
- ``Project.get_jobs`` has been renamed ``Project.get_model_jobs`` for clarity and deprecated
- Support for the experimental date partitioning has been removed in DataRobot API,
  so it is being removed from the client immediately.

API Changes
***********

- In several places where ``AppPlatformError`` was being raised, now ``TypeError``, ``ValueError`` or
  ``InputNotUnderstoodError`` are now used. With this change, one can now safely assume that when
  catching an ``AppPlatformError`` it is because of an unexpected response from the server.
- ``AppPlatformError`` has gained a two new attributes, ``status_code`` which is the HTTP status code
  of the unexpected response from the server, and ``error_code`` which is a DataRobot-defined error
  code. ``error_code`` is not used by any routes in DataRobot API 2.1, but will be in the future.
  In cases where it is not provided, the instance of ``AppPlatformError`` will have the attribute
  ``error_code`` set to ``None``.
- Two new subclasses of ``AppPlatformError`` have been introduced, ``ClientError`` (for 400-level
  response status codes) and ``ServerError`` (for 500-level response status codes). These will make
  it easier to build automated tooling that can recover from periodic connection issues while polling.
- If a ``ClientError`` or ``ServerError`` occurs during a call to ``Project.from_async``, then a
  ``ProjectAsyncFailureError`` (a subclass of AsyncFailureError) will be raised. That exception will
  have the status_code of the unexpected response from the server, and the location that was being
  polled to wait for the asynchronous process to resolve.


2.0.27
======

New Features
************

- ``PredictJob`` class was added to work with prediction jobs
- ``wait_for_async_predictions`` function added to `predict_job` module

Deprecation Summary
*******************

- The `order_by` parameter of the ``Project.list`` is now deprecated.


0.2.26
======

Enhancements
************

- ``Projet.set_target`` will re-fetch the project data after it succeeds,
  keeping the client side in sync with the state of the project on the
  server
- ``Project.create_featurelist`` now throws ``DuplicateFeaturesError``
  exception if passed list of features contains duplicates
- ``Project.get_models`` now supports snake_case arguments to its
  order_by keyword

Deprecation Summary
*******************

- ``Project.wait_for_aim_stage`` is now deprecated, as the REST Async
  flow is a more reliable method of determining that project creation has
  completed successfully
- ``Project.status`` is deprecated in favor of ``Project.get_status``
- ``recommendation_settings`` parameter of ``Project.start`` is
  deprecated in favor of ``recommender_settings``

Bugfixes
********

- ``Project.wait_for_aim_stage`` changed to support Python 3
- Fixed incorrect value of ``SCORING_TYPE.cross_validation``
- Models returned by ``Project.get_models`` will now be correctly
  ordered when the order_by keyword is used


0.2.25
======

- Pinned versions of required libraries

0.2.24
======

Official release of v0.2

0.1.24
======

- Updated documentation
- Renamed parameter `name` of `Project.create` and `Project.start` to `project_name`
- Removed `Model.predict` method
- `wait_for_async_model_creation` function added to `modeljob` module
- `wait_for_async_status_service` of `Project` class renamed to `_wait_for_async_status_service`
- Can now use auth_token in config file to configure SDK


0.1.23
======

- Fixes a method that pointed to a removed route


0.1.22
======

- Added `featurelist_id` attribute to `ModelJob` class


0.1.21
======

- Removes `model` attribute from `ModelJob` class


0.1.20
======

- Project creation raises `AsyncProjectCreationError` if it was unsuccessful
- Removed `Model.list_prime_rulesets` and `Model.get_prime_ruleset` methods
- Removed `Model.predict_batch` method
- Removed `Project.create_prime_model` method
- Removed `PrimeRuleSet` model
- Adds backwards compatibility bridge for ModelJob async
- Adds ModelJob.get and ModelJob.get_model


0.1.19
======

- Minor bugfixes in `wait_for_async_status_service`


0.1.18
======

- Removes `submit_model` from Project until serverside implementation is improved
- Switches training URLs for new resource-based route at /projects/<project_id>/models/
- Job renamed to ModelJob, and using modelJobs route
- Fixes an inconsistency in argument order for `train` methods


0.1.17
======

- `wait_for_async_status_service` timeout increased from 60s to 600s


0.1.16
======

- `Project.create` will now handle both async/sync project creation


0.1.15
======

- All routes pluralized to sync with changes in API
- `Project.get_jobs` will request all jobs when no param specified
- dataframes from `predict` method will have pythonic names
- `Project.get_status` created, `Project.status` now deprecated
- `Project.unlock_holdout` created.
- Added `quickrun` parameter to `Project.set_target`
- Added `modelCategory` to Model schema
- Add `permalinks` featrue to Project and Model objects.
- `Project.create_prime_model` created


0.1.14
======

- `Project.set_worker_count` fix for compatibility with API change in project update.


0.1.13
======

- Add positive class to `set_target`.
- Change attributes names of `Project`, `Model`, `Job` and `Blueprint`
    - `features` in `Model`, `Job` and `Blueprint` are now `processes`
    - `dataset_id` and `dataset_name` migrated to `featurelist_id` and `featurelist_name`.
    - `samplepct` -> `sample_pct`
- `Model` has now `blueprint`, `project`, and `featurlist` attributes.
- Minor bugfixes.


0.1.12
======

- Minor fixes regarding rename `Job` attributes. `features` attributes now named `processes`, `samplepct` now is `sample_pct`.


0.1.11
======

(May 27, 2015)

- Minor fixes regarding migrating API from under_score names to camelCase.


0.1.10
======

(May 20, 2015)

- Remove `Project.upload_file`, `Project.upload_file_from_url` and `Project.attach_file` methods. Moved all logic that uploading file to `Project.create` method.


0.1.9
=====

(May 15, 2015)

- Fix uploading file causing a lot of memory usage. Minor bugfixes.
