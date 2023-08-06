.. _batch_predictions:

#################
Batch Predictions
#################

The Batch Prediction API provides a way to score large datasets using flexible options
for intake and output on the Prediction Servers you have already deployed.

The main features are:

* Flexible options for intake and output.
* Stream local files and start scoring while still uploading - while simultaneously downloading the results.
* Score large datasets from and to S3.
* Connect to your database using JDBC with bidirectional streaming of scoring data and results.
* Intake and output options can be mixed and doesn’t need to match. So scoring from a JDBC source to an S3 target is also an option.
* Protection against overloading your prediction servers with the option to control the concurrency level for scoring.
* Prediction Explanations can be included (with option to add thresholds).
* Passthrough Columns are supported to correlate scored data with source data.
* Prediction Warnings can be included in the output.

To interact with Batch Predictions, you should use the :ref:`BatchPredictionJob <batch_prediction_api>`. class.

***********************
Scoring local CSV files
***********************

We provide a small utility function for scoring from/to local CSV files:
``BatchPredictionJob.score_to_file()``. The first parameter can be either:

* Path to a CSV dataset
* File-like object
* Pandas DataFrame

For larger datasets, you should avoid using a DataFrame, as that will load
the entire dataset into memory. The other options don't.

.. code-block:: python

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    dr.BatchPredictionJob.score_to_file(
        deployment_id,
        './data_to_predict.csv',
        './predicted.csv',
    )

The input file will be streamed to our API and scoring will start immediately.
As soon as results start coming in, we will initiate the download concurrently.
The entire call will block until the file has been scored.

**********************
Scoring from and to S3
**********************

We provide a small utility function for scoring from/to CSV files hosted on S3:
``BatchPredictionJob.score_s3()``. This requires that the intake and output
buckets share the same credentials (see :ref:`Credentials <credentials_api_doc>`) or are public:

.. code-block:: python

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    cred = dr.Credential.get('5a8ac9ab07a57a0001be501f')

    dr.BatchPredictionJob.score_s3(
        deployment_id=deployment_id,
        's3://mybucket/data_to_predict.csv',
        's3://mybucket/predicted.csv',
        credential=cred,
   )

.. note:: The S3 output functionality has a limit of 100 GB.

**************************************
Wiring a Batch Prediction Job manually
**************************************

If you can't use any of the utilities above, you are also free to configure
your job manually. This requires configuring an intake and output option:

.. code-block:: python

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    dr.BatchPredictionJob.score(
        deployment_id,
        intake_settings={
            'type': 's3',
            'url': 's3://public-bucket/data_to_predict.csv',
            'credential_id': '5a8ac9ab07a57a0001be501f',
        },
        output_settings={
            'type': 'local_file',
            'path': './predicted.csv',
        },
    )

Credentials may be created with :ref:`Credentials API <credentials_api_doc>`.

Supported intake types
----------------------

These are the supported intake types and descriptions of their configuration parameters:

Local file intake
^^^^^^^^^^^^^^^^^

This requires you to pass either a path to a CSV dataset, file-like object or a Pandas
DataFrame as the ``file`` parameter:

.. code-block:: python

    intake_settings={
        'type': 'local_file',
        'file': './data_to_predict.csv',
    }

S3 CSV intake
^^^^^^^^^^^^^

This requires you to pass an S3 URL to the CSV file your scoring in the ``url`` parameter:

.. code-block:: python

    intake_settings={
        'type': 's3',
        'url': 's3://public-bucket/data_to_predict.csv',
    }

.. _batch_predictions_s3_creds_usage:

If the bucket is not publicly accessible, you can supply AWS credentials using the three
parameters:

* ``aws_access_key_id``
* ``aws_secret_access_key``
* ``aws_session_token``

And save it to the :ref:`Credential API <s3_creds_usage>`. Here is an example:

.. code-block:: python

    import datarobot as dr

    # get to make sure it's exists
    cred = dr.Credential.get(credential_id)

    intake_settings={
        'type': 's3',
        'url': 's3://private-bucket/data_to_predict.csv',
        'credential_id': cred.credential_id,
    }


JDBC intake
^^^^^^^^^^^

This requires you to create a :ref:`DataStore <database_connectivity_overview>` and
:ref:`Credential <basic_creds_usage>` for your database:

.. code-block:: python

    # get to make sure it's exists
    data_store = dr.DataStore.get(datastore_id)
    cred = dr.Credential.get(credential_id)

    intake_settings = {
        'type': 'jdbc',
        'table': 'table_name',
        'schema': 'public',
        'dataStoreId': data_store.id,
        'credentialId': cred.credential_id,
    }


Supported output types
----------------------

These are the supported output types and descriptions of their configuration parameters:

Local file output
^^^^^^^^^^^^^^^^^

For local file output you have two options. You can either pass a ``path`` parameter and
have the client block and download the scored data concurrently. This is the fastest way
to get predictions as it will upload, score and download concurrently:

.. code-block:: python

    output_settings={
        'type': 'local_file',
        'path': './predicted.csv',
    }

Another option is to leave out the parameter and subsequently call ``BatchPredictionJob.download()``
at your own convenience. The ``score()`` call will then return as soon as the upload is complete.

If the job is not finished scoring, the call to ``BatchPredictionJob.download()`` will start
streaming the data that has been scored so far and block until more data is available.

You can poll for job completion using ``BatchPredictionJob.get_status()`` or use
``BatchPredictionJob.wait_for_completion()`` to wait.

.. code-block:: python

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    job = dr.BatchPredictionJob.score(
        deployment_id,
        intake_settings={
            'type': 'local_file',
            'file': './data_to_predict.csv',
        },
        output_settings={
            'type': 'local_file',
        },
    )

    job.wait_for_completion()

    with open('./predicted.csv', 'wb') as f:
        job.download(f)

S3 CSV output
^^^^^^^^^^^^^

This requires you to pass an S3 URL to the CSV file where the scored data should be saved
to in the ``url`` parameter:

.. code-block:: python

    output_settings={
        'type': 's3',
        'url': 's3://public-bucket/predicted.csv',
    }

Most likely, the bucket is not publically accessible for writes, but you can supply AWS
credentials using the three parameters:

* ``aws_access_key_id``
* ``aws_secret_access_key``
* ``aws_session_token``

And save it to the :ref:`Credential API <s3_creds_usage>`. Here is an example:

.. code-block:: python

    # get to make sure it's exists
    cred = dr.Credential.get(credential_id)

    output_settings={
        'type': 's3',
        'url': 's3://private-bucket/predicted.csv',
        'credential_id': cred.credential_id,
    }

JDBC output
^^^^^^^^^^^

Same as for the input, this requires you to create a :ref:`DataStore <database_connectivity_overview>` and
:ref:`Credential <basic_creds_usage>` for your database, but for `output_settings` you also need to specify
`statementType`, which should be one of ``datarobot.enums.AVAILABLE_STATEMENT_TYPES``:

.. code-block:: python

    # get to make sure it's exists
    data_store = dr.DataStore.get(datastore_id)
    cred = dr.Credential.get(credential_id)

    output_settings = {
        'type': 'jdbc',
        'table': 'table_name',
        'schema': 'public',
        'statementType': 'insert',
        'dataStoreId': data_store.id,
        'credentialId': cred.credential_id,
    }
