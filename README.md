# movoa-haystack

Unlimited AI video generator with sound: on paid plans the tenth take of a shot costs what the first did, and your first clip is free to make right now. Haystack component for [Movoa](https://movoa.ai/?utm_source=pypi-haystack&utm_medium=package): generate video clips with sound from text or animate a photo as the first frame inside a Haystack pipeline.

## Install

```bash
pip install movoa-haystack
```

Set `MOVOA_API_KEY` from [movoa.ai/settings/apikeys](https://movoa.ai/settings/apikeys), or pass `Secret.from_token(...)`. Runs cost credits on your Movoa account at the prices on [movoa.ai/pricing](https://movoa.ai/pricing).

## Usage

```python
from movoa_haystack import MovoaVideoGenerator

gen = MovoaVideoGenerator(duration=6, aspect_ratio="16:9")
videos = gen.run(prompt="a paper boat drifting down a rain gutter, low angle")["videos"]
```

To animate a photo, pass `image_url`:

```python
videos = gen.run(
    prompt="the camera slowly orbits the statue while soft light sweeps across it",
    image_url="https://example.com/statue.jpg",
)["videos"]
```

## Links

- [Movoa](https://movoa.ai/?utm_source=pypi-haystack&utm_medium=package)
- [Text to video](https://movoa.ai/video/text-to-video)
- [API keys](https://movoa.ai/settings/apikeys)
- [Pricing](https://movoa.ai/pricing)
