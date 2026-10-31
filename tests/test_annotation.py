import pytest
from app.core import Studio


def test_disagreement_independence_and_export(tmp_path):
    s = Studio("sqlite:///" + str(tmp_path / "s.sqlite"))
    s.annotate("t1", "A", "urgent")
    with pytest.raises(ValueError):
        s.adjudicate("t1", "urgent", "R", "reason")
    s.annotate("t1", "B", "general")
    assert s.tasks()[0]["disagreement"]
    with pytest.raises(ValueError):
        s.adjudicate("t1", "urgent", "A", "reason")
    s.adjudicate("t1", "urgent", "R", "outage")
    assert s.export()[0]["label"] == "urgent"
    with pytest.raises(ValueError):
        s.annotate("t1", "C", "billing")
    s.adjudicate("t1", "general", "R2", "Second review")
    assert len(s.tasks()[0]["decisions"]) == 2
