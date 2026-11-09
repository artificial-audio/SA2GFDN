# SA2GFDN

Code for the statistical-acoustics coupled-room GFDN paper. The acoustic coupling construction, energy observables, and experiments live here; the DSP engine and general matrix utilities come from **pyFDN 0.7.0** on PyPI. This repository does not ship its own pyFDN copy.

## Install and test

Python 3.10 or newer:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest -q
```

The pyFDN dependency is pinned so updates do not silently change the paper results. Its FLAMO dependency also installs PyTorch; allow sufficient disk space. Record the installed environment with `python -m pip freeze` alongside exported results.

## Current manuscript figures

Run from the checkout root after installation:

```sh
python examples/coupled_rooms/revise_two_room_figures.py --output outputs/two-room
python examples/coupled_rooms/revise_three_room_evaluation.py --output outputs/three-room
python examples/coupled_rooms/export_paper_figures.py --output outputs/validation
python examples/coupled_rooms/validate_sa_assumptions.py --output outputs/validation
```

The first command exports the two-room impulse responses and four-way energy comparisons. The second exports the three-room four-way comparisons (0–3 seconds, absorption coefficients 0.06/0.02/0.005), static coupling spectra, and door-closing/reopening **closed energy-model** trajectories. It does not render pressure signals with a moving door. Each command writes numerical results and provenance alongside figures; runs can take several minutes. Generated output is ignored by Git.

`export_paper_figures.py` is the original baseline exporter, retained for the underlying model and earlier figures. `compare_static_coupling.py` and `compare_channel_coupling.py` reproduce the additional coupling ablations. Use each program's `--help` for output/worker options. Noise-start SA comparisons and impulse-start mixing transients are separate experiments.

## Contents and scope

- `src/sa2gfdn/physics_based_coupling.py`: physical rate matching, orthogonal coupling, room modulation, and energy ledgers.
- `src/sa2gfdn/geometry.py`: aperture/source/receiver geometry for exploratory external-data comparisons.
- `src/sa2gfdn/acoustics.py`: the envelope observable used only by those comparisons.
- `examples/coupled_rooms/`: current figure exporters, validation, ablations, and five exploratory marimo notebooks.
- `tests/`: tests of paper-specific physics, observables, and experiment helpers.

The five original notebooks remain as paper-related exploratory material. Install `.[notebooks]` to open them with marimo. `match_to_ertd.py` and `match_to_treble_three_room.py` additionally require external datasets under the paths stated in their source; these data are not supplied or validated by this repository. Some exploratory notebooks write figures/audio and run large sweeps. They are not the canonical manuscript exporters.

The migration removes the general pyFDN library, unrelated example gallery, Sphinx documentation, preset/audio assets, and library release/packaging configuration. Those belong to [pyFDN](https://github.com/artificial-audio/pyFDN). The original snapshot remains in Git history. No manuscript source or private measurement dataset is included.

## Provenance and attribution

The latest paper experiments were imported from `artificial-audio/pyFDN` commit `2897abbd61a7d08f0fae0c10b2cfa322de4f8ede`, originally proposed against Orchi's coupled-room branch. Imports and rendering calls have been migrated to current pyFDN's public `dss_to_td`, `td.RecursionState`, and matrix utilities. The paper's coupling/geometry helpers remain local because pyFDN 0.7.0 does not provide them.

MIT license; see LICENSE. Code retains the original pyFDN project attribution. The inherited coupled-room reference is Schlecht, *Delay Network Architectures for Room and Coupled Space Modeling*; this repository contains new paper-specific experiments rather than the upstream packaged reference audio.

The published baseline mixing matrices are stored in `paper_mixers.json`, and the original modulation draws are retained explicitly. This preserves the manuscript realizations across pyFDN’s RNG API change; new configurations use the current matrix generator. The stored matrices are experiment inputs, not a vendored DSP implementation.
