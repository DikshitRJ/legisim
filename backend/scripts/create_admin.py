import asyncio
import sys
import argparse
from sqlalchemy import select
from app.core.database import async_session_maker, init_db, engine
from app.models.officer import Officer
from app.core.security import get_password_hash
from app.config import settings

async def create_admin(name: str, email: str, password: str, department: str):
    await init_db()
    async with async_session_maker() as session:
        stmt = select(Officer).where(Officer.email == email)
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            print(f"Error: User {email} already exists.")
            await engine.dispose()
            sys.exit(1)
            
        admin = Officer(
            name=name,
            email=email,
            password_hash=get_password_hash(password),
            department=department,
            role="admin"
        )
        session.add(admin)
        await session.commit()
        print(f"Successfully created admin user: {email}")
        await engine.dispose()

def main():
    parser = argparse.ArgumentParser(description="Create an admin user")
    parser.add_argument("--name", required=True, help="Full Name")
    parser.add_argument("--email", required=True, help="Email address")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--department", required=True, help="Department")
    
    args = parser.parse_args()
    asyncio.run(create_admin(args.name, args.email, args.password, args.department))

if __name__ == "__main__":
    main()
