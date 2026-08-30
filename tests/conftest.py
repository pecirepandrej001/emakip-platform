import os
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_emakip.db")
os.environ.setdefault("SECRET_KEY", "test-secret")
