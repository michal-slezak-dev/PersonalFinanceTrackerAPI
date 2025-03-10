from database import SessionLocal

try:
    db = SessionLocal()
    print("✅ Database connection successful!")
    db.close()
except Exception as e:
    print("❌ Database connection failed:", e)
