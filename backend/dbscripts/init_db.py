from .audit_db import Base, engine
from .models import AuditLog

def init_db():
    Base.metadata.create_all(bind=engine)
