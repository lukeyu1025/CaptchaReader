import os
import builtins
import pytest

np = pytest.importorskip('numpy')

import process_manage


def test_show_rate(monkeypatch, tmp_path, capsys):
    # create dummy png files
    (tmp_path / "111111.png").write_text("data")
    (tmp_path / "222222.png").write_text("data")

    # fake get_image returning the label as image as well
    def fake_get_image(path):
        label = os.path.splitext(os.path.basename(path))[0]
        return label, label

    monkeypatch.setattr('load.get_image', fake_get_image)

    # choose_process returns simple order
    monkeypatch.setattr(process_manage, 'choose_process', lambda: [])

    # replace process to just echo label as text
    def fake_process(original_image, order):
        return process_manage.Result(order, [original_image]*5, original_image)

    monkeypatch.setattr(process_manage, 'process', fake_process)

    inputs = iter([str(tmp_path), ''])
    monkeypatch.setattr(builtins, 'input', lambda: next(inputs))

    process_manage.show_rate()
    out = capsys.readouterr().out
    assert 'Out of 12 letters 12 were correctly read.' in out
    assert 'Out of 2 captcha images, 2 were correctly read.' in out
