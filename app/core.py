import json
import tempfile
import uuid
from pathlib import Path
from sqlalchemy import String, select, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base, database

LABELS = {"urgent", "billing", "general"}


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    text: Mapped[str]
    final_label: Mapped[str | None]


class Annotation(Base):
    __tablename__ = "annotations"
    __table_args__ = (UniqueConstraint("task_id", "annotator"),)
    id: Mapped[str] = mapped_column(String, primary_key=True)
    task_id: Mapped[str]
    annotator: Mapped[str]
    label: Mapped[str]


class Decision(Base):
    __tablename__ = "decisions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    task_id: Mapped[str]
    label: Mapped[str]
    reviewer: Mapped[str]
    reason: Mapped[str]


class Studio:
    def __init__(self, url=None):
        self.engine, self.sessions = database(url)
        with self.sessions.begin() as s:
            for t in json.loads(Path("data/tasks.json").read_text()):
                if not s.get(Task, t["id"]):
                    s.add(Task(**t, final_label=None))

    def annotate(self, tid, annotator, label):
        if label not in LABELS or not annotator.strip():
            raise ValueError("valid label and annotator required")
        with self.sessions.begin() as s:
            task = s.get(Task, tid)
            if not task or task.final_label:
                raise ValueError("task unavailable or already adjudicated")
            old = s.scalar(
                select(Annotation).where(Annotation.task_id == tid, Annotation.annotator == annotator)
            )
            if old:
                if old.label != label:
                    raise ValueError("annotation immutable; ask reviewer to adjudicate")
                return {"replayed": True}
            s.add(Annotation(id=str(uuid.uuid4()), task_id=tid, annotator=annotator, label=label))
            return {"recorded": True}

    def adjudicate(self, tid, label, reviewer, reason):
        if label not in LABELS or not reviewer.strip() or not reason.strip():
            raise ValueError("label, reviewer and reason required")
        with self.sessions.begin() as s:
            task = s.get(Task, tid)
            annotations = list(s.scalars(select(Annotation).where(Annotation.task_id == tid)))
            if not task or len(annotations) < 2:
                raise ValueError("two independent annotations required")
            if reviewer in {a.annotator for a in annotations}:
                raise ValueError("reviewer must be independent")
            task.final_label = label
            s.add(Decision(id=str(uuid.uuid4()), task_id=tid, label=label, reviewer=reviewer, reason=reason))
            return {"final_label": label}

    def tasks(self):
        with self.sessions() as s:
            rows = []
            for t in s.scalars(select(Task).order_by(Task.id)):
                labels = [
                    dict(annotator=a.annotator, label=a.label)
                    for a in s.scalars(select(Annotation).where(Annotation.task_id == t.id))
                ]
                decisions = [
                    dict(label=d.label, reviewer=d.reviewer, reason=d.reason)
                    for d in s.scalars(select(Decision).where(Decision.task_id == t.id))
                ]
                rows.append(
                    dict(
                        id=t.id,
                        text=t.text,
                        annotations=labels,
                        disagreement=len({a["label"] for a in labels}) > 1,
                        final_label=t.final_label,
                        decisions=decisions,
                    )
                )
            return rows

    def export(self):
        return [
            dict(id=t["id"], text=t["text"], label=t["final_label"]) for t in self.tasks() if t["final_label"]
        ]


def demo(mode="fixture"):
    with tempfile.TemporaryDirectory() as d:
        s = Studio("sqlite:///" + str(Path(d) / "labels.sqlite"))
        s.annotate("t1", "A", "urgent")
        s.annotate("t1", "B", "general")
        before = s.tasks()[0]
        s.adjudicate("t1", "urgent", "Reviewer", "All customers are affected by an outage.")
        return dict(disagreement=before, resolved=s.tasks()[0], export=s.export())


def evaluate(mode="fixture"):
    r = demo(mode)
    return dict(passed=r["disagreement"]["disagreement"] and r["export"][0]["label"] == "urgent", scenario=r)
