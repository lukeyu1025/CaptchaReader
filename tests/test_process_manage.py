import os
import pytest
np = pytest.importorskip('numpy')
cv2 = pytest.importorskip('cv2')

import process_manage
import Preprocessing


def test_show_rate(tmp_path, monkeypatch, capsys):
    img = np.full((10, 10), 255, dtype=np.uint8)
    labels = ['111111', '222222']
    for lab in labels:
        cv2.imwrite(str(tmp_path / f"{lab}.png"), img)

    monkeypatch.setattr(process_manage, 'choose_process', lambda order_str=None: [Preprocessing.return_image]*4)
    calls = {'i': 0}
    def fake_tesseract(_):
        val = labels[calls['i']]
        calls['i'] += 1
        return val
    monkeypatch.setattr(Preprocessing, 'tesseract', fake_tesseract)

    process_manage.show_rate(str(tmp_path), order_str='1111', pause=False)
    out, _ = capsys.readouterr()
    assert 'Success Rate' in out
