# backend/seed.py
from app import db, Project
import json

def seed():
    db.create_all()
    p1 = Project(
        title="E-commerce UI Redesign",
        description="Redesign for ecom checkout flow.",
        category="UI Design",
        tools=json.dumps(["Figma", "Photoshop"]),
        imageUrls=json.dumps(["/static/img/ecom1.png"]),
        projectUrl="https://example.com/ecom",
        clientName="Acme Corp",
        completionYear=2024,
        tags=json.dumps(["checkout","ecommerce"]),
        isFeatured=True
    )
    p2 = Project(
        title="Mobile Banking UX",
        description="Onboarding flow improvements.",
        category="Mobile Design",
        tools=json.dumps(["Figma", "Illustrator"]),
        imageUrls=json.dumps(["/static/img/bank1.png"]),
        projectUrl="",
        clientName="BankX",
        completionYear=2023,
        tags=json.dumps(["onboarding","finance"]),
        isFeatured=False
    )
    db.session.add_all([p1,p2])
    db.session.commit()
    print("Seeded.")

if __name__ == '__main__':
    seed()
