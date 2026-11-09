"""Preserve sampled outputs from the pre-migration paper code at 2897abbd61a7.

Both fixed/time-varying and lossless/lossy renders use seed 200, 0.3 seconds,
and source room 1. The fixture was generated with the original pyFDN 0.5 engine.
"""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('migration_export', ROOT/'examples/coupled_rooms/export_paper_figures.py')
paper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paper)
LEGACY = json.loads((ROOT/'tests/data/legacy-render-samples.json').read_text())


@pytest.mark.parametrize('rooms', [2, 3])
@pytest.mark.parametrize('lossy', [False, True])
@pytest.mark.parametrize('varying', [False, True])
def test_current_pyfdn_preserves_published_realizations(rooms, lossy, varying):
    volumes = [160, 80] if rooms == 2 else [160, 80, 120]
    apertures = [[0, 2], [2, 0]] if rooms == 2 else [[0, 2, 0], [2, 0, 1.5], [0, 1.5, 0]]
    model = paper.room_model(volumes, apertures, setting=1000 if rooms == 2 else 2000,
                             matrix_seed=12343 if rooms == 2 else 12314)
    actual = paper.render(model, lossy=lossy, varying=varying, duration=.3)
    expected = LEGACY[f'{rooms}-{lossy}-{varying}']
    np.testing.assert_array_equal(model['delays'], expected['delays'])
    for observable in ['energy', 'microphones']:
        np.testing.assert_allclose(actual[observable][::997], expected[observable], atol=1e-12, rtol=0)
