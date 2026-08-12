from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.heritage_site import HeritageSite


HERITAGE_SITES = [
    {
        "name": "Brihadeeswarar Temple",
        "slug": "brihadeeswarar-temple",
        "short_description": "A monumental Chola-era temple celebrated for its Dravidian architecture and cultural significance.",
        "description": "Brihadeeswarar Temple at Thanjavur is one of the outstanding monuments of Chola architecture and forms part of the UNESCO World Heritage property known as the Great Living Chola Temples.",
        "category": "Temple",
        "country": "India",
        "state": "Tamil Nadu",
        "city": "Thanjavur",
        "latitude": 10.7828,
        "longitude": 79.1318,
        "established_year": 1010,
        "architectural_style": "Dravidian",
        "historical_period": "Chola Period",
        "significance": "A major achievement of Chola architecture and a landmark of South Indian cultural heritage.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Taj Mahal",
        "slug": "taj-mahal",
        "short_description": "An iconic Mughal monument in Agra renowned for its white marble architecture.",
        "description": "The Taj Mahal is a monumental complex in Agra built during the Mughal period and widely recognized for its architectural composition, craftsmanship, and cultural significance.",
        "category": "Monument",
        "country": "India",
        "state": "Uttar Pradesh",
        "city": "Agra",
        "latitude": 27.1751,
        "longitude": 78.0421,
        "established_year": 1653,
        "architectural_style": "Mughal",
        "historical_period": "Mughal Period",
        "significance": "One of the world's most recognized examples of Mughal architecture and a major cultural heritage landmark.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Ajanta Caves",
        "slug": "ajanta-caves",
        "short_description": "Rock-cut Buddhist caves containing remarkable ancient paintings and sculptures.",
        "description": "The Ajanta Caves in Maharashtra form a historic Buddhist cave complex known for its rock-cut architecture, sculptures, and surviving paintings.",
        "category": "Cave",
        "country": "India",
        "state": "Maharashtra",
        "city": "Aurangabad",
        "latitude": 20.5519,
        "longitude": 75.7033,
        "established_year": -200,
        "architectural_style": "Rock-cut",
        "historical_period": "Ancient India",
        "significance": "An exceptional record of ancient Buddhist art, architecture, and religious culture.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Ellora Caves",
        "slug": "ellora-caves",
        "short_description": "A monumental rock-cut complex representing Buddhist, Hindu, and Jain traditions.",
        "description": "The Ellora Caves comprise a major rock-cut architectural complex in Maharashtra containing monuments associated with Buddhism, Hinduism, and Jainism.",
        "category": "Cave",
        "country": "India",
        "state": "Maharashtra",
        "city": "Aurangabad",
        "latitude": 20.0268,
        "longitude": 75.1790,
        "established_year": 600,
        "architectural_style": "Rock-cut",
        "historical_period": "Early Medieval India",
        "significance": "A remarkable expression of religious diversity and rock-cut architectural achievement.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Hampi",
        "slug": "hampi",
        "short_description": "The monumental remains of the former Vijayanagara capital in Karnataka.",
        "description": "Hampi contains extensive archaeological remains associated with the Vijayanagara Empire, including temples, markets, fortifications, and monumental structures.",
        "category": "Archaeological Site",
        "country": "India",
        "state": "Karnataka",
        "city": "Vijayanagara",
        "latitude": 15.3350,
        "longitude": 76.4600,
        "established_year": 1336,
        "architectural_style": "Vijayanagara",
        "historical_period": "Medieval India",
        "significance": "A major archaeological landscape representing the cultural and architectural achievements of the Vijayanagara Empire.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Konark Sun Temple",
        "slug": "konark-sun-temple",
        "short_description": "A monumental 13th-century temple designed as the chariot of the Sun God.",
        "description": "The Konark Sun Temple in Odisha is a monumental temple complex renowned for its architectural design, stone carvings, and representation of a colossal chariot.",
        "category": "Temple",
        "country": "India",
        "state": "Odisha",
        "city": "Konark",
        "latitude": 19.8876,
        "longitude": 86.0945,
        "established_year": 1250,
        "architectural_style": "Kalinga",
        "historical_period": "Eastern Ganga Period",
        "significance": "A major achievement of medieval Indian temple architecture and stone craftsmanship.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Red Fort",
        "slug": "red-fort",
        "short_description": "A historic Mughal fort complex in the heart of Delhi.",
        "description": "The Red Fort is a major Mughal-era fortification in Delhi, known for its monumental architecture and important role in the history of the Indian subcontinent.",
        "category": "Fort",
        "country": "India",
        "state": "Delhi",
        "city": "Delhi",
        "latitude": 28.6562,
        "longitude": 77.2410,
        "established_year": 1648,
        "architectural_style": "Mughal",
        "historical_period": "Mughal Period",
        "significance": "An important symbol of India's historical and architectural heritage.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Machu Picchu",
        "slug": "machu-picchu",
        "short_description": "A remarkable Inca archaeological site situated high in the Andes of Peru.",
        "description": "Machu Picchu is an Inca archaeological complex set within a dramatic mountainous landscape and recognized for its exceptional integration of architecture and environment.",
        "category": "Archaeological Site",
        "country": "Peru",
        "state": "Cusco",
        "city": "Machupicchu",
        "latitude": -13.1631,
        "longitude": -72.5450,
        "established_year": 1450,
        "architectural_style": "Inca",
        "historical_period": "Inca Period",
        "significance": "A globally significant archaeological landscape representing Inca engineering, architecture, and cultural history.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Petra",
        "slug": "petra",
        "short_description": "An ancient Nabataean city famous for architecture carved directly into sandstone cliffs.",
        "description": "Petra is an ancient archaeological city in Jordan characterized by monumental rock-cut architecture, tombs, temples, and an extensive historic landscape.",
        "category": "Archaeological Site",
        "country": "Jordan",
        "state": "Ma'an",
        "city": "Petra",
        "latitude": 30.3285,
        "longitude": 35.4444,
        "established_year": -300,
        "architectural_style": "Nabataean",
        "historical_period": "Ancient Near East",
        "significance": "A major archaeological and cultural heritage site representing the Nabataean civilization.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Angkor Wat",
        "slug": "angkor-wat",
        "short_description": "A monumental Khmer temple complex and one of the great achievements of Southeast Asian architecture.",
        "description": "Angkor Wat is a vast Khmer temple complex in Cambodia, recognized for its monumental scale, architectural composition, reliefs, and historical significance.",
        "category": "Temple",
        "country": "Cambodia",
        "state": "Siem Reap",
        "city": "Siem Reap",
        "latitude": 13.4125,
        "longitude": 103.8670,
        "established_year": 1150,
        "architectural_style": "Khmer",
        "historical_period": "Khmer Empire",
        "significance": "One of the most important surviving monuments of Khmer civilization.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
    {
        "name": "Acropolis of Athens",
        "slug": "acropolis-of-athens",
        "short_description": "A monumental ancient Greek citadel overlooking the historic city of Athens.",
        "description": "The Acropolis of Athens is an ancient monumental complex containing major classical Greek structures and representing an important stage in the development of Western architecture.",
        "category": "Archaeological Site",
        "country": "Greece",
        "state": "Attica",
        "city": "Athens",
        "latitude": 37.9715,
        "longitude": 23.7257,
        "established_year": -447,
        "architectural_style": "Classical Greek",
        "historical_period": "Classical Greece",
        "significance": "A foundational monument of ancient Greek civilization and classical architecture.",
        "preservation_status": "Protected",
        "is_verified": True,
        "is_active": True,
    },
]


def seed_heritage_sites() -> None:
    engine = create_engine(settings.DATABASE_URL)

    inserted = 0
    skipped = 0

    with Session(engine) as session:
        for site_data in HERITAGE_SITES:
            existing = session.scalar(
                select(HeritageSite).where(
                    HeritageSite.slug == site_data["slug"]
                )
            )

            if existing:
                skipped += 1
                continue

            session.add(HeritageSite(**site_data))
            inserted += 1

        session.commit()

    print(f"Heritage site seed completed: {inserted} inserted, {skipped} skipped.")


if __name__ == "__main__":
    seed_heritage_sites()
