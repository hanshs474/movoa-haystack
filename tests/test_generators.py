from unittest import mock

import movoa
import pytest
from haystack.utils import Secret
from movoa_haystack import MovoaVideoGenerator


def test_video_and_roundtrip(monkeypatch):
    monkeypatch.setenv("MOVOA_API_KEY", "test-env-key")
    gen = MovoaVideoGenerator(duration=6, resolution="768p")
    gen2 = MovoaVideoGenerator.from_dict(gen.to_dict())
    with mock.patch.object(movoa, "generate_video", return_value="https://cdn.movoa.ai/v.mp4") as g:
        assert gen2.run(prompt="a paper boat", image_url="https://x/y.png") == {"videos": ["https://cdn.movoa.ai/v.mp4"]}
    assert g.call_args.args[1] == "minimax-h3"
    assert g.call_args.args[2] == "https://x/y.png"
    assert g.call_args.kwargs["api_key"] == "test-env-key"
    assert g.call_args.kwargs["duration"] == 6
    assert "aspect_ratio" not in g.call_args.kwargs


def test_live_auth_error_propagates():
    with pytest.raises(movoa.AuthError):
        MovoaVideoGenerator(api_key=Secret.from_token("invalid-test-fixture-token")).run(prompt="a paper boat")
