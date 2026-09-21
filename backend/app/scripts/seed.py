from app.database.database import SessionLocal
from app.models.user import User

db = SessionLocal()

existing_user = db.query(User).filter(
    User.username == "test_user"
).first()

if existing_user:
    print("User already exists:", existing_user.id)

else:
    test_user = User(
        username="test_user",
        full_name="CyberShield Tester",
        email="tester@cybershield.ai",
        hashed_password="hashed_password_test",
        role="user",
        is_active=True,
        is_verified=True
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    print("User created:", test_user.id)

db.close()
