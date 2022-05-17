from datetime import datetime

from yacut import db

from .contants import SHORT_LINK_MAX_LENGTH


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(SHORT_LINK_MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data):
        for field in ('original', 'short'):
            if field in data:
                setattr(self, field, data[field])
