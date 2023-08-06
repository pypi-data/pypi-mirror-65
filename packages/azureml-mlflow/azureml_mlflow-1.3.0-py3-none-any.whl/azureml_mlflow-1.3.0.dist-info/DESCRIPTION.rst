Microsoft Azure Machine Learning Tracking server plugin for Python
===================================================================
The azureml-mlflow package contains the integration code of AzureML with MLFlow.
MLFlow (https://mlflow.org/) is an open-source platform for tracking machine learning experiments and managing models.
You can use MLFlow logging APIs with Azure Machine Learning service: the metrics and artifacts are logged to your Azure ML Workspace.


With an AzureML Workspace (https://docs.microsoft.com/en-us/python/api/overview/azure/ml/intro?view=azure-ml-py) add the below lines before your MLflow code:

import mlflow
from azureml.core import Workspace

workspace = Workspace.from_config()

mlflow.set_tracking_uri(workspace.get_mlflow_tracking_uri())

# Examples can be found here (https://aka.ms/azureml-mlflow-examples)




