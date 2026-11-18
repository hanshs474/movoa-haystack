"""Movoa video generation as a Haystack component.

Unlimited AI video generator with sound: on paid plans the tenth take of a shot
costs what the first did, and your first clip is free to make right now.

Runs cost credits on a Movoa account: pass ``api_key`` (a Haystack ``Secret``)
or set ``MOVOA_API_KEY``. Create a key at https://movoa.ai/settings/apikeys.
"""

from typing import Any, Dict, List, Optional

import movoa
from haystack import component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace


def _params(**kw: Any) -> Dict[str, Any]:
    return {k: v for k, v in kw.items() if v is not None}


@component
class MovoaVideoGenerator:
    """Generates a clip with sound from a prompt, or animates a photo, and returns its URL.

    ``model`` defaults to ``minimax-h3``; other ids: ``veo-3-1-fast``,
    ``seedance-2-5``, ``seedance-2``, ``seedance-2-fast``, ``seedance-2-mini``.
    """

    def __init__(
        self,
        model: str = movoa.DEFAULT_MODEL,
        duration: Optional[int] = None,
        resolution: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        sound: Optional[bool] = None,
        api_key: Secret = Secret.from_env_var("MOVOA_API_KEY"),
        timeout: float = 900.0,
    ):
        self.model = model
        self.duration = duration
        self.resolution = resolution
        self.aspect_ratio = aspect_ratio
        self.sound = sound
        self.api_key = api_key
        self.timeout = timeout

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(
            self,
            model=self.model,
            duration=self.duration,
            resolution=self.resolution,
            aspect_ratio=self.aspect_ratio,
            sound=self.sound,
            api_key=self.api_key.to_dict(),
            timeout=self.timeout,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MovoaVideoGenerator":
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

    @component.output_types(videos=List[str])
    def run(self, prompt: str, image_url: Optional[str] = None) -> Dict[str, List[str]]:
        """Generate one clip with sound, or animate the image at ``image_url`` as the first frame."""
        url = movoa.generate_video(
            prompt,
            self.model,
            image_url,
            api_key=self.api_key.resolve_value(),
            timeout=self.timeout,
            **_params(
                duration=self.duration,
                resolution=self.resolution,
                aspect_ratio=self.aspect_ratio,
                sound=self.sound,
            ),
        )
        return {"videos": [url]}
