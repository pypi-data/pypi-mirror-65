import base64
import json
import os

import boto3
import dill
import requests
from joblib import dump
from monitaur.exceptions import ClientAuthError, ClientValidationError
from monitaur.utils import get_influences
from monitaur.virgil.alibi.tabular import AnchorTabular

base_url = "https://api.monitaur.ai"


class Monitaur:
    def __init__(self, client_secret, base_url=base_url):
        self._session = requests.Session()

        self._session.headers["User-Agent"] = "monitaur-client-library"

        self.client_secret = client_secret

        self.base_url = base_url
        self.transaction_url = f"{self.base_url}/api/transactions/"
        self.models_url = f"{self.base_url}/api/models/"
        self.credentials_url = f"{self.base_url}/api/credentials/"
        self.login_url = f"{self.base_url}/api/auth/?grant_type=client_credentials"

    def authenticate(self, client_secret: str) -> str:
        """
        Authenticates the user from the API
        Parameters
        ----------
        client_secret

        Returns
            access: Access token for authentication
            refresh: Refresh token to renew access
        -------

        """
        json = {"client_secret": client_secret}
        response = self._session.post(self.login_url, json=json)

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid client secret", response.json())

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response.json())

        return response.json()["access"]

    def add_model(
        self,
        name: str,
        model_type: str,
        model_class: str,
        library: str,
        trained_model_hash: str,
        production_file_hash: str,
        feature_number: int,
        owner: str,
        developer: str,
        python_version: str,
        ml_library_version: str,
        version: float = 0.1,
        influences: bool = True,
    ) -> str:
        """
        Adds metadata about the machine learning model to the system.

        Args:
            name: Unique name for what this model is predicting.
            model_type: Type of model
              (linear_regression, logistic_regression, decision_tree, svm, naive_bayes, knn,
                k_means, random_forest, gmb, xgboost, lightgbm, catboost, recurrent_neural_network,
                convolutional_neural_network, generative_adversarial_network, recursive_neural_network,
                long_short_term_memory)
            model_class: This field can contain one of these values: tabular, image, nlp.
            library: Machine learning library
              (tensorflow, pytorch, apache_spark, scikit_learn, xg_boost, light_gbm,
                keras, statsmodels, caffe)
            trained_model_hash:
              Trained model file hash. Must be a joblib. None is also allowed.
            production_file_hash:
              Production file that uses the trained model for prediction.
              This should also have the logic that converts the prediction into something humanreadable.
              None is allowed.
              Example:
              ```
              def get_prediction(data_array):
                  diabetes_model = load("./_example/data.joblib")
                  data = array([data_array])
                  result = diabetes_model.predict(data)

                  prediction = "You do not have diabetes"
                  if result[0] == 1:
                      prediction = "You have diabetes"

                  return prediction
              ```
            feature_number: Number of inputs.
            owner: Name of the model owner.
            developer: Name of the data scientist.
            python_version: Stores python version. Ensure the data follows semver - major.minor.release
            ml_library_version: Stores ML library version. Ensure the data follows semver - major.minor.release
            image: Is it an image model? Defaults to False.
            version: Monitaur model version. Defaults to 0.1.
            influences: Obtain decision influences from anchors library.

        Returns:
            model_set_id: A UUID string for the monitaur model set.
        """

        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        json = {
            "name": name,
            "model_type": model_type.lower(),
            "model_class": model_class,
            "library": library.lower(),
            "trained_model_hash": trained_model_hash,
            "production_file_hash": production_file_hash,
            "feature_number": feature_number,
            "owner": owner,
            "developer": developer,
            "version": version,
            "python_version": python_version,
            "ml_library_version": ml_library_version,
            "influences": influences,
        }
        response = self._session.post(self.models_url, json=json)

        print(response.status_code)
        print(response.__dict__)

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid token", response.json())

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response.json())

        return response.json().get("model_set_id")

    def get_credentials(self, model_set_id: str) -> dict:
        """
        Retrieves AWS credentials.

        Args:
            model_set_id: A UUID string for the monitaur model set received from the API.

        Returns:
            credentials:
                {
                    "aws_access_key": "123",
                    "aws_secret_key": "456",
                    "aws_region": "us-east-1",
                    "aws_bucket_name": "bucket name"
                }
        """
        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        response = self._session.get(f"{self.credentials_url}{model_set_id}/")

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid token", response.json())

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response.json())

        return response.json().get("credentials")

    def record_training_tabular(
        self,
        credentials: dict,
        model_set_id: str,
        trained_model,  # instantiated model
        training_data,  # numpy array
        feature_names: list,
        re_train: bool = False,
    ):
        """
        Sends trained model and anchors data to S3.
        Currently works only for traditional, tabular machine learning models.

        Args:
            credentials: S3 credentials received from the API
                {
                    "aws_access_key": "123",
                    "aws_secret_key": "456",
                    "aws_region": "us-east-1",
                    "aws_bucket_name": "bucket name"
                }
            model_set_id: A UUID string for the monitaur model set received from the API.
            trained_model: Instantiated model (scikit-learn, xgboost).
            training_data: Training data (x training).
            feature_names: Model inputs.
            re_train: Model version will be increased by 0.1 when it is True.

        Returns:
            True
        """

        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        response = self._session.get(f"{self.models_url}set/{model_set_id}/")
        version = response.json()["version"]

        if re_train:
            version = self._increase_model_version(version, major=True)

        predict_fn = lambda x: trained_model.predict_proba(x)  # NOQA
        explainer = AnchorTabular(predict_fn, feature_names)
        explainer.fit(training_data)

        filename = f"{model_set_id}.joblib"
        filename_anchors = f"{model_set_id}.anchors"
        with open(filename, "wb") as f:
            dump(trained_model, f)
        with open(filename_anchors, "wb") as f:
            dill.dump(explainer, f)

        # connect to s3 and upload trained model and anchor files
        client = boto3.client(
            "s3",
            aws_access_key_id=credentials["aws_access_key"],
            aws_secret_access_key=credentials["aws_secret_key"],
            region_name=credentials["aws_region"],
        )
        with open(filename, "rb") as f:
            client.upload_fileobj(
                f,
                credentials["aws_bucket_name"],
                f"{model_set_id}/{version}/{filename}",
            )
        with open(filename_anchors, "rb") as f:
            client.upload_fileobj(
                f,
                credentials["aws_bucket_name"],
                f"{model_set_id}/{version}/{filename_anchors}",
            )

        # Update Training Version
        payload = {"model_set_id": model_set_id, "version": version}

        initial_data = response.json()

        response = self._session.post(
            f"{self.models_url}set/{model_set_id}/", json=payload
        )
        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", initial_data)

        print(f"Training recording: model_set_id {model_set_id}, version {version}")
        return True

    def record_training_image(
        self,
        credentials: dict,
        model_set_id: str,
        trained_model,  # instantiated model
        re_train: bool = False,
    ):
        """
        Sends trained model to S3.

        Args:
            credentials: S3 credentials received from the API
                {
                    "aws_access_key": "123",
                    "aws_secret_key": "456",
                    "aws_region": "us-east-1",
                    "aws_bucket_name": "bucket name"
                }
            model_set_id: A UUID string for the monitaur model set received from the API.
            trained_model: Instantiated model (scikit-learn, xgboost).
            re_train: Model version will be increased by 0.1 when it is True.

        Returns:
            True
        """

        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        response = self._session.get(f"{self.models_url}set/{model_set_id}/")
        version = response.json()["version"]

        if re_train:
            version = self._increase_model_version(version)

        filename = f"{model_set_id}.joblib"
        with open(filename, "wb") as f:
            dump(trained_model, f)

        # connect to s3 and upload trained model and anchor files
        client = boto3.client(
            "s3",
            aws_access_key_id=credentials["aws_access_key"],
            aws_secret_access_key=credentials["aws_secret_key"],
            region_name=credentials["aws_region"],
        )
        with open(filename, "rb") as f:
            client.upload_fileobj(
                f,
                credentials["aws_bucket_name"],
                f"{model_set_id}/{version}/{filename}",
            )

        print(f"Training recording: model_set_id {model_set_id}, version {version}")
        return True

    def _increase_model_version(self, version, major=False):
        if isinstance(version, str):
            version = float(version)

        if major:
            return version + 1.0

        return version + 0.1

    def record_transaction(
        self,
        credentials: dict,
        model_set_id: str,
        trained_model_hash: str,
        production_file_hash: str,
        prediction: str,
        features: dict,
        native_transaction_id: str = None,
        image: str = None,
    ) -> dict:
        """
        Sends transaction details to the server.

        Args:
            credentials: S3 credentials received from the API
                {
                    "aws_access_key": "123",
                    "aws_secret_key": "456",
                    "aws_region": "us-east-1",
                    "aws_bucket_name": "bucket name"
                }
            model_set_id: A UUID string for the monitaur model set received from the API.
            trained_model_hash: Trained model file hash. Must be a joblib.
            production_file_hash:
              Production file that uses the trained model for prediction.
              This should also have the logic that converts the prediction into something humanreadable.
              Example:
              ```
              def get_prediction(data_array):
                  diabetes_model = load("./_example/data.joblib")
                  data = array([data_array])
                  result = diabetes_model.predict(data)

                  prediction = "You do not have diabetes"
                  if result[0] == 1:
                      prediction = "You have diabetes"

                  return prediction
              ```
            prediction: Outcome from the production prediction file.
            features: key/value pairs of the feature names and values.
            native_transaction_id: Unique identifier for the customer (optional).
            image: file path to the image to be uploaded if the model_class is an image

        Returns:
            Transaction details from the server
        """

        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        response = self._session.get(f"{self.models_url}set/{model_set_id}/")
        response_data = response.json()

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid token", response_data)

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response_data)

        version = response_data["version"]
        influences = response_data.get("influences", False)

        if "model_class" in response_data and response_data["model_class"] == "image":
            if image is None:
                raise ClientValidationError("No Image")

        transaction_data = {
            "model": model_set_id,
            "trained_model_hash": trained_model_hash,
            "production_file_hash": production_file_hash,
            "prediction": prediction,
            "features": features,
            "influences": None,
            "native_transaction_id": native_transaction_id,
        }

        if influences and image is None:
            influences = get_influences(model_set_id, version, features, credentials,)
            transaction_data.update({"influences": json.dumps(influences)})

        if image is not None:
            transaction_data.update({"influences": "N/A"})
            if not os.path.exists(image):
                raise ClientValidationError("Image File path not valid")

            # Check the file extension
            extension = os.path.splitext(image)[-1].lower()
            if extension not in (".png", ".jpg", ".jpeg"):
                raise ClientValidationError("Invalid Image provided")

            file_size = float(os.path.getsize(image)) / (1024.0 ** 2)
            if file_size > 1:
                raise ClientValidationError(
                    "Image Size greater than One (1) Megabyte. Choose a file with a lesser size"
                )

            with open(image, "rb") as img:
                image_byte = (base64.b64encode(img.read())).decode("utf-8")

            transaction_data.update({"image": image_byte})

        response = self._session.post(self.transaction_url, json=transaction_data,)

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response_data)

        return response.json()

    def read_transactions(self, model_id: int = None, model_set_id: str = None) -> list:
        """
        Retrieves transactions.

        Args:
            model_id: An int for the monitaur model received from the API. (optional)
            model_set_id: A UUID string for the monitaur model set received from the API. (optional)

        Returns:
            List of transactions
        """

        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        querystring = {}
        if model_id:
            querystring.update({"model": model_id})
        if model_set_id:
            querystring.update({"model_set_id": model_set_id})

        response = self._session.get(self.transaction_url, params=querystring)

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid token", response.json())

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response.json())

        return response.json()
