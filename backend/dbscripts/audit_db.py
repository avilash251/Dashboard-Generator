from peewee import SqliteDatabase, Model, TextField, CharField, DateTimeField, BooleanField
from datetime import datetime
import os

os.makedirs("backend/db", exist_ok=True)
db = SqliteDatabase("backend/db/audit_log.db")

class BaseModel(Model):
    class Meta:
        database = db

class AuditLog(BaseModel):
    prompt = TextField()
    source = CharField(default="user")
    timestamp = DateTimeField(default=datetime.utcnow)
    flagged = BooleanField(default=False)

class AnomalyLog(BaseModel):
    metric = CharField()
    severity = CharField()
    timestamp = DateTimeField(default=datetime.utcnow)

def init_db():
    db.connect()
    db.create_tables([AuditLog, AnomalyLog], safe=True)
    db.close()

def save_log(prompt, source="user", flagged=False):
    AuditLog.create(prompt=prompt, source=source, flagged=flagged)
def get_recent_logs(limit=10):
    return AuditLog.select().order_by(AuditLog.timestamp.desc()).limit(limit)

def log_anomaly(metric, severity="warning"):
    AnomalyLog.create(metric=metric, severity=severity)

def get_anomaly_trend(limit=20):
    return AnomalyLog.select().order_by(AnomalyLog.timestamp.desc()).limit(limit)
