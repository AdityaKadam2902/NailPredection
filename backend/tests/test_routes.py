"""Route Tests."""

import json
from io import BytesIO

from PIL import Image


class TestHealth:
    def test_health(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "success" in data
        assert "mock_mode" in data["data"]
        assert "has_tensorflow" in data["data"]
        assert "model_path" in data["data"]


class TestVersion:
    def test_version(self, client):
        response = client.get("/api/version")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["data"]["name"] == "NailCareAI"


class TestModelInfo:
    def test_model_info(self, client):
        response = client.get("/api/model-info")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["data"]["num_classes"] == 17
        assert len(data["data"]["classes"]) == 17
        assert "model_path" in data["data"]["model"]
        assert "mock_mode" in data["data"]["model"]


class TestPages:
    def test_index(self, client):
        assert client.get("/").status_code == 200
    def test_about(self, client):
        assert client.get("/about.html").status_code == 200
    def test_nailhome(self, client):
        assert client.get("/nailhome.html").status_code == 200
    def test_nailpred(self, client):
        assert client.get("/nailpred.html").status_code == 200


class TestPredict:
    def test_no_file(self, client):
        response = client.post("/api/predict")
        assert response.status_code == 400

    def test_predict_response_shape(self, client):
        image = Image.new("RGB", (224, 224), color=(120, 120, 120))
        buf = BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)

        response = client.post(
            "/api/predict",
            data={"file": (buf, "test.png")},
            content_type="multipart/form-data",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "data" in data
        assert "prediction" in data["data"]
        assert "top_predictions" in data["data"]
        assert len(data["data"]["top_predictions"]) > 0
        assert "meta" in data
        assert "mock_mode" in data["meta"]
