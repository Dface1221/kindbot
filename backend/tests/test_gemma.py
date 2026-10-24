from unittest.mock import patch, MagicMock
import pytest
from app.services.gemma import generate_json, _clean_json_text, get_model_name, is_api_configured


def test_clean_json_text_markdown_block():
    raw = "```json\n{\"title\": \"Test\", \"purpose\": \"Testing\"}\n```"
    assert _clean_json_text(raw) == '{"title": "Test", "purpose": "Testing"}'


def test_clean_json_text_plain():
    raw = '{"title": "Test"}'
    assert _clean_json_text(raw) == '{"title": "Test"}'


def test_missing_api_key_raises_value_error(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")
    with pytest.raises(ValueError, match="GEMINI_API_KEY is not configured"):
        generate_json("Test prompt")


def test_generate_json_mocked_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-mock-key")
    mock_response = MagicMock()
    mock_response.text = '{"title": "Mock Skill", "purpose": "Testing mock", "steps": []}'

    with patch("google.genai.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_client_cls.return_value = mock_client

        data = generate_json("Test prompt")
        assert data["title"] == "Mock Skill"
        assert data["purpose"] == "Testing mock"


def test_generate_json_mocked_malformed_json(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-mock-key")
    mock_response = MagicMock()
    mock_response.text = 'NOT_JSON'

    with patch("google.genai.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_client_cls.return_value = mock_client

        with pytest.raises(RuntimeError, match="malformed JSON"):
            generate_json("Test prompt")
