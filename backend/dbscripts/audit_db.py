import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, desc, func
from sqlalchemy.orm import sessionmaker
from .base import Base
from .models import AuditLog

# DB setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "../../dbscripts/audit_log.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

engine = create_engine(
    f"sqlite:///{db_path}",
    connect_args={"check_same_thread": False},
    echo=False,
)
SessionLocal = sessionmaker(bind=engine)

# --- Utility Methods ---
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Failed to initialize DB: {e}")
        
def save_log(prompt: str, response_type: str, user_type: str = "user"):
    try:
        db = SessionLocal()
        entry = AuditLog(
            prompt=prompt,
            response_type=response_type,
            user_type=user_type,
            timestamp=datetime.utcnow(),
        )
        db.add(entry)
        db.commit()
        db.close()
    except Exception as e:
        print(f"[❌ Error in save_log]: {e}")


def get_recent_logs(limit: int = 50):
    try:
        db = SessionLocal()
        logs = db.query(AuditLog).order_by(desc(AuditLog.timestamp)).limit(limit).all()
        db.close()
        return logs
    except Exception as e:
        print(f"[❌ Error in get_recent_logs]: {e}")
        return []


def get_anomaly_trend(days: int = 7):
    try:
        db = SessionLocal()
        today = datetime.utcnow().date()
        start_date = today - timedelta(days=days)

        trend = (
            db.query(func.date(AuditLog.timestamp), func.count())
            .filter(
                AuditLog.timestamp >= start_date,
                AuditLog.response_type == "anomaly"
            )
            .group_by(func.date(AuditLog.timestamp))
            .order_by(func.date(AuditLog.timestamp))
            .all()
        )
        db.close()
        return trend
    except Exception as e:
        print(f"[❌ Error in get_anomaly_trend]: {e}")
        return []
