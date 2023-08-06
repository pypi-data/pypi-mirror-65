import base64
import os
from io import BytesIO

import boto3
import pytest
import requests
from monitaur import Monitaur
from monitaur.exceptions import ClientAuthError, ClientValidationError
from monitaur.virgil.alibi.tabular import AnchorTabular

model_data = {
    "name": "Diabetes Classifier",
    "model_type": "random_forest",
    "model_class": "tabular",
    "library": "scikit_learn",
    "trained_model_hash": "7fa8962a",
    "production_file_hash": "ec9b7a68",
    "feature_number": 8,
    "owner": "Anthony Habayeb",
    "developer": "Andrew Clark",
    "python_version": "1.1.1",
    "ml_library_version": "1.1.1",
    "influences": True,
}

record_training_data = {
    "credentials": {
        "aws_access_key": "some access key",
        "aws_secret_key": "some secret key",
        "aws_region": "us-east-1",
        "aws_bucket_name": "some bucket name",
    },
    "model_set_id": 1,
    "feature_names": [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeF",
        "Age",
    ],
}

record_training_image_data = {
    "credentials": {
        "aws_access_key": "some access key",
        "aws_secret_key": "some secret key",
        "aws_region": "us-east-1",
        "aws_bucket_name": "some bucket name",
    },
    "model_set_id": 1,
}

transaction_data = {
    "credentials": {
        "aws_access_key": "some access key",
        "aws_secret_key": "some secret key",
        "aws_region": "us-east-1",
        "aws_bucket_name": "some bucket name",
    },
    "model_set_id": 1,
    "trained_model_hash": "7fa8962a",
    "production_file_hash": "ec9b7a68",
    "prediction": "",
    "features": {},
}


def test_initialize_session():
    monitaur = Monitaur(client_secret="123")

    assert isinstance(monitaur._session, requests.Session)
    assert monitaur._session.headers["User-Agent"] == "monitaur-client-library"


def test_add_model_returns_model_set_id(mocker):
    monitaur = Monitaur(client_secret="123")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"model_set_id": 111})
    mocker.patch.object(monitaur._session, "post", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    model_set_id = monitaur.add_model(**model_data)

    assert model_set_id == 111


def test_add_model_raises_client_auth_error_given_unauthorized_response(mocker):
    monitaur = Monitaur(client_secret="invalid")
    response = requests.Response()
    response.status_code = 401
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "post", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value=response)

    with pytest.raises(ClientAuthError):
        monitaur.add_model(**model_data)


def test_add_model_raises_client_validation_error_when_400_response_received(mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 400
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "post", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    with pytest.raises(ClientValidationError):
        monitaur.add_model(**model_data)


def test_record_transaction_returns_response_json_given_success_response(mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(
        response, "json", return_value={"version": 1, "influences": True}
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mock_explain_transaction = mocker.patch(
        "monitaur.client.get_influences",
        return_value=["Glucose <= 99.00", "BMI <= 27.35"],
    )
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"id": 1})
    mocker.patch.object(monitaur._session, "post", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    transaction_details = monitaur.record_transaction(**transaction_data)

    assert transaction_details["id"] is not None
    assert mock_explain_transaction.call_count == 1


def test_when_influences_false_record_transaction_skips_explain_transaction(mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(
        response, "json", return_value={"version": 1, "influences": False}
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mock_explain_transaction = mocker.patch("monitaur.client.get_influences")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"id": 1})
    mocker.patch.object(monitaur._session, "post", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    transaction_details = monitaur.record_transaction(**transaction_data)

    assert transaction_details["id"] is not None
    assert mock_explain_transaction.call_count == 0


def test_record_transaction_raises_client_auth_error_given_unauthorized_response(
    mocker,
):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 401
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value=response)

    with pytest.raises(ClientAuthError):
        monitaur.record_transaction(**transaction_data)


def test_record_transaction_on_image_model_raise_client_validation_error_if_no_image(
    mocker,
):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(
        response,
        "json",
        return_value={"version": 1, "influences": True, "model_class": "image"},
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    mock_explain_transaction = mocker.patch(
        "monitaur.client.get_influences",
        return_value=["Glucose <= 99.00", "BMI <= 27.35"],
    )
    response = requests.Response()
    response.status_code = 400
    mocker.patch.object(response, "json", return_value={"id": 1})
    mocker.patch.object(monitaur._session, "post", return_value=response)

    with pytest.raises(ClientValidationError):
        monitaur.record_transaction(**transaction_data)

    assert mock_explain_transaction.call_count == 0


def test_record_transaction_on_image_model_raise_client_validation_error_if_invalid_image_path(
    mocker,
):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    image_tran_data = transaction_data.copy()
    image_tran_data["image"] = "Invalid Image path"

    response.status_code = 200
    mocker.patch.object(
        response,
        "json",
        return_value={"version": 1, "influences": True, "model_class": "image"},
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    mock_explain_transaction = mocker.patch(
        "monitaur.client.get_influences",
        return_value=["Glucose <= 99.00", "BMI <= 27.35"],
    )
    response = requests.Response()
    response.status_code = 400
    mocker.patch.object(response, "json", return_value={"id": 1})
    mocker.patch.object(monitaur._session, "post", return_value=response)

    with pytest.raises(ClientValidationError):
        monitaur.record_transaction(**image_tran_data)

    assert mock_explain_transaction.call_count == 0


def test_record_transaction_on_image_model_raise_client_validation_error_if_image_not_exists(
    mocker,
):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    image_tran_data = transaction_data.copy()
    image_tran_data["image"] = "image.png"

    response.status_code = 200
    mocker.patch.object(
        response,
        "json",
        return_value={"version": 1, "influences": True, "model_class": "image"},
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    mock_explain_transaction = mocker.patch(
        "monitaur.client.get_influences",
        return_value=["Glucose <= 99.00", "BMI <= 27.35"],
    )

    mocker.patch.object(os.path, "exists", return_value=False)

    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"id": 1})
    mocker.patch.object(monitaur._session, "post", return_value=response)

    with pytest.raises(ClientValidationError):
        monitaur.record_transaction(**image_tran_data)

    assert mock_explain_transaction.call_count == 0


def test_record_transaction_on_image_model_raise_client_validation_error_if_invalid_file(
    mocker,
):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    image_tran_data = transaction_data.copy()
    image_tran_data["image"] = "image.pdf"

    response.status_code = 200
    mocker.patch.object(
        response,
        "json",
        return_value={"version": 1, "influences": True, "model_class": "image"},
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    mock_explain_transaction = mocker.patch(
        "monitaur.client.get_influences",
        return_value=["Glucose <= 99.00", "BMI <= 27.35"],
    )

    mocker.patch.object(os.path, "exists", return_value=True)

    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"id": 1})
    mocker.patch.object(monitaur._session, "post", return_value=response)

    with pytest.raises(ClientValidationError):
        monitaur.record_transaction(**image_tran_data)

    assert mock_explain_transaction.call_count == 0


def test_record_transaction_on_image_model_raise_client_validation_error_if_image_greater_1mb(
    mocker,
):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    image_tran_data = transaction_data.copy()
    image_tran_data["image"] = "image.png"

    response.status_code = 200
    mocker.patch.object(
        response,
        "json",
        return_value={"version": 1, "influences": True, "model_class": "image"},
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    mock_explain_transaction = mocker.patch(
        "monitaur.client.get_influences",
        return_value=["Glucose <= 99.00", "BMI <= 27.35"],
    )

    mocker.patch.object(os.path, "exists", return_value=True)
    mocker.patch.object(os.path, "getsize", return_value=2097152)

    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"id": 1})
    mocker.patch.object(monitaur._session, "post", return_value=response)

    with pytest.raises(ClientValidationError):
        monitaur.record_transaction(**image_tran_data)

    assert mock_explain_transaction.call_count == 0


def test_record_transaction_on_image_model_success(mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    image_tran_data = transaction_data.copy()
    image_tran_data["image"] = "image.png"

    response.status_code = 200
    mocker.patch.object(
        response,
        "json",
        return_value={"version": 1, "influences": True, "model_class": "image"},
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    mock_explain_transaction = mocker.patch(
        "monitaur.client.get_influences",
        return_value=["Glucose <= 99.00", "BMI <= 27.35"],
    )

    mocker.patch.object(os.path, "exists", return_value=True)
    mocker.patch.object(os.path, "getsize", return_value=7094)
    mock_open = mocker.patch("builtins.open")
    mock_open.return_value = BytesIO(b"12345")
    mocker.patch.object(
        base64, "b64encode", return_value=b"Image-Base-64-encoded-return-data"
    )

    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"id": 1})
    mocker.patch.object(monitaur._session, "post", return_value=response)

    transaction_details = monitaur.record_transaction(**image_tran_data)

    assert mock_explain_transaction.call_count == 0
    assert transaction_details is not None
    mock_open.assert_called_once_with("image.png", "rb")


def test_record_transaction_raises_client_validation_error_given_bad_request(mocker):
    monitaur = Monitaur(client_secret="secret")
    invalid_data = transaction_data.copy()
    invalid_data["features"] = "invalid features"
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(
        response, "json", return_value={"version": 1, "influences": True}
    )
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    mock_explain_transaction = mocker.patch(
        "monitaur.client.get_influences",
        return_value=["Glucose <= 99.00", "BMI <= 27.35"],
    )
    response = requests.Response()
    response.status_code = 400
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "post", return_value=response)

    with pytest.raises(ClientValidationError):
        monitaur.record_transaction(**invalid_data)

    assert mock_explain_transaction.call_count == 1

    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 400
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    with pytest.raises(ClientValidationError):
        monitaur.record_transaction(**invalid_data)


def test_record_training_tabular(trained_model, training_data, mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"version": 1})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(AnchorTabular, "__init__", return_value=None)
    mocker.patch.object(AnchorTabular, "fit")
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    boto3_client_mock = mocker.patch.object(boto3, "client")
    upload_fileobj_mock = boto3_client_mock.return_value.upload_fileobj

    result = monitaur.record_training_tabular(
        trained_model=trained_model, training_data=training_data, **record_training_data
    )

    assert result is True
    assert upload_fileobj_mock.call_count == 2

    filename = f"{record_training_data['model_set_id']}.joblib"
    filename_anchors = f"{record_training_data['model_set_id']}.anchors"
    os.remove(filename)
    os.remove(filename_anchors)


def test_record_training_tabular_with_re_train_true(
    trained_model, training_data, mocker
):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"version": 1})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur._session, "post", return_value=response)
    mocker.patch.object(AnchorTabular, "__init__", return_value=None)
    mocker.patch.object(AnchorTabular, "fit")
    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    boto3_client_mock = mocker.patch.object(boto3, "client")
    upload_fileobj_mock = boto3_client_mock.return_value.upload_fileobj
    increase_model_version_mock = mocker.patch.object(
        monitaur, "_increase_model_version"
    )

    result = monitaur.record_training_tabular(
        trained_model=trained_model,
        training_data=training_data,
        re_train=True,
        **record_training_data,
    )

    assert result is True
    increase_model_version_mock.assert_called_with(1, major=True)
    assert upload_fileobj_mock.call_count == 2

    filename = f"{record_training_data['model_set_id']}.joblib"
    filename_anchors = f"{record_training_data['model_set_id']}.anchors"
    os.remove(filename)
    os.remove(filename_anchors)


def test_record_training_image(trained_model, mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"version": 1})
    mocker.patch.object(monitaur._session, "get", return_value=response)

    mocker.patch.object(monitaur, "authenticate", return_value="Token")
    boto3_client_mock = mocker.patch.object(boto3, "client")
    upload_fileobj_mock = boto3_client_mock.return_value.upload_fileobj

    result = monitaur.record_training_image(
        trained_model=trained_model, **record_training_image_data
    )

    assert result is True
    assert upload_fileobj_mock.call_count == 1

    filename = f"{record_training_image_data['model_set_id']}.joblib"
    os.remove(filename)


def test_record_training_image_with_re_train_true(trained_model, mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 200
    mocker.patch.object(response, "json", return_value={"version": 1})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    boto3_client_mock = mocker.patch.object(boto3, "client")
    upload_fileobj_mock = boto3_client_mock.return_value.upload_fileobj
    increase_model_version_mock = mocker.patch.object(
        monitaur, "_increase_model_version"
    )

    result = monitaur.record_training_image(
        trained_model=trained_model, re_train=True, **record_training_image_data,
    )

    assert result is True
    increase_model_version_mock.assert_called_with(1)
    assert upload_fileobj_mock.call_count == 1

    filename = f"{record_training_image_data['model_set_id']}.joblib"
    os.remove(filename)


@pytest.mark.parametrize("version, expected_result", [("1.2", 1.3), (2, 2.1)])
def test_eval(version, expected_result):
    monitaur = Monitaur(client_secret="secret")

    assert monitaur._increase_model_version(version) == expected_result


def test_get_credentials_returns_credentials(mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 200
    credentials = {
        "aws_access_key": "foo",
        "aws_secret_key": "bar",
        "aws_region": "us-east-1",
        "aws_bucket_name": "monitaur-demo",
    }
    mocker.patch.object(response, "json", return_value={"credentials": credentials})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    results = monitaur.get_credentials(1)

    assert results == {
        "aws_access_key": "foo",
        "aws_bucket_name": "monitaur-demo",
        "aws_region": "us-east-1",
        "aws_secret_key": "bar",
    }


def test_get_credentials_raises_client_auth_error_given_unauthorized_response(mocker,):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = 401
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value=response)

    with pytest.raises(ClientAuthError):
        monitaur.get_credentials(1)


def test_get_credentials_raises_client_validation_error_given_bad_request(mocker):
    monitaur = Monitaur(client_secret="secret")
    invalid_data = transaction_data.copy()
    invalid_data["features"] = "invalid features"
    response = requests.Response()
    response.status_code = 400
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    with pytest.raises(ClientValidationError):
        monitaur.get_credentials("bad")


def test_read_transactions_as_unauthorized_client(mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = requests.status_codes.codes.unauthorized
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value=response)

    with pytest.raises(ClientAuthError):
        monitaur.read_transactions(model_id=1, model_set_id="12-123")


def test_read_transactions_for_bad_request(mocker):
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = requests.status_codes.codes.bad_request
    mocker.patch.object(response, "json", return_value={})
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    with pytest.raises(ClientValidationError):
        monitaur.read_transactions(model_id=0, model_set_id="$%^")


def test_read_transactions(mocker):
    response_data = [
        {
            "id": 1,
            "model_set_id": "711945cc-5edb-49f6-aeee-ef1557b9103a",
            "features": {
                "age": 100,
                "bmi": 22,
                "glucose": 176,
                "insulin": 170,
                "pregnancies": 100,
                "bloodpressure": 80,
                "skinthickness": 18,
                "diabetespedigreef": 0.1,
            },
            "influences": "N/A",
            "trained_model_hash": "191953485533775893111981513100739685667",
            "production_file_hash": "295271162841296919015553875344047845893",
            "prediction": "You have diabetes",
            "created_date": "2020-02-10T13:54:11.345600Z",
            "updated_date": "2020-02-10T13:54:11.345657Z",
            "model": 1,
        }
    ]
    monitaur = Monitaur(client_secret="secret")
    response = requests.Response()
    response.status_code = requests.status_codes.codes.ok
    mocker.patch.object(response, "json", return_value=response_data)
    mocker.patch.object(monitaur._session, "get", return_value=response)
    mocker.patch.object(monitaur, "authenticate", return_value="Token")

    transactions = monitaur.read_transactions(
        model_id=1, model_set_id="711945cc-5edb-49f6-aeee-ef1557b9103a"
    )
    assert transactions == response_data
