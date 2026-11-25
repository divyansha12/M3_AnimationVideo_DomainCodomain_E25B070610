# M3 Animation Video: Domain, Codomain and Range

Internal Assessment, Linear Algebra and Calculus (M3), Option 1: Animation Video.

**Student:** Divyansha Singh (E25B070610)
**Concept:** Domain, codomain and range, taught through mapping diagrams (one-variable and two-variable examples).
**Learning objective:** By the end of the video, the viewer will be able to identify the domain, codomain and range of a function and explain how they differ.

## Watch the video

[Watch the final video (DomainCodomain_Video.mp4)](DomainCodomain_Video.mp4)

Click the link to play it in your browser. It is about 5 minutes long, 1080p, with voice-over.

## What is in this repository

| File / folder | What it is |
|---|---|
| `DomainCodomain_Video.mp4` | Final video, 16:9, 1080p, with an opening frame and a closing thank-you frame |
| `DomainCodomain_Code/` | All animation source code (Manim) plus helper scripts |
| `Storyboard.pdf` | The 6-scene storyboard |

Inside `DomainCodomain_Code/`:
- `domain_codomain.py`: the whole animation (one scene class, one method per storyboard scene)
- `config.py`: name, ID and music credit used by the video and the storyboard
- `math_check.py`: independent numerical check of every example
- `make_storyboard.py`: builds `Storyboard.pdf`
- `requirements.txt`

## Run it yourself

```bash
cd DomainCodomain_Code
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python math_check.py                                         # checks the maths
manim -qh --fps 30 domain_codomain.py DomainCodomainVideo     # renders the silent 1080p video
```

The output appears in `media/videos/domain_codomain/1080p30/`. No LaTeX is needed. The script was tested with Manim Community 0.22.1.

## Credits and disclosure

- Animation: [Manim Community Edition](https://www.manim.community/)
- Voice-over: recorded by me
- Background music: none (update this line if you add one)
- **AI disclosure:** I used Claude (Anthropic) to help draft the storyboard, the narration script and the Manim code. I checked all the mathematics myself and I can explain the concepts and the code.
