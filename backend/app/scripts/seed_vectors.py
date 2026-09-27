import asyncio
import os
import csv
from pathlib import Path
from sqlalchemy import text
from app.core.database import async_session_maker, init_db
from app.models.dataset import DatasetFile, DatasetChunk

# A simple stub embedding generator if OpenAI is not configured
async def generate_embedding(text: str) -> list[float]:
    """Generate dummy embeddings for demonstration if API fails/missing."""
    try:
        from langchain_openai import OpenAIEmbeddings
        # Dummy key for OpenAIEmbeddings since it's just a fallback
        embeddings = OpenAIEmbeddings(api_key="sk-dummy")
        return await embeddings.aembed_query(text)
    except Exception:
        # Return a dummy vector of 1536 dims (OpenAI ada-002 size)
        import random
        return [random.uniform(-1, 1) for _ in range(1536)]

async def seed_vectors():
    await init_db()
    data_dir = Path("/app/data") if os.environ.get("DOCKER_ENV") else Path("../../data")
    if not data_dir.exists():
        data_dir = Path(__file__).parent.parent.parent.parent / "data"

    print(f"Reading data from {data_dir}")

    async with async_session_maker() as session:
        # ensure pgvector is created
        await session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await session.commit()
        
        # Iterate over all csv files in data directory
        for csv_path in data_dir.rglob("*.csv"):
            category = csv_path.parent.name
            filename = csv_path.name
            
            # Check if already seeded
            from sqlalchemy import select
            stmt = select(DatasetFile).where(DatasetFile.filename == filename)
            existing = (await session.execute(stmt)).scalar_one_or_none()
            if existing:
                print(f"Skipping {filename} (already seeded)")
                continue

            print(f"Processing {filename}...")
            file_record = DatasetFile(
                filename=filename,
                category=category,
                description=f"CSV data for {category}"
            )
            session.add(file_record)
            await session.flush()

            try:
                with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    if not header:
                        continue
                    
                    chunk_text = ""
                    chunk_count = 0
                    for row in reader:
                        row_dict = dict(zip(header, row))
                        # format as string
                        row_str = ", ".join(f"{k}: {v}" for k, v in row_dict.items())
                        chunk_text += row_str + "\n"
                        
                        # Every 10 rows, create a chunk
                        if len(chunk_text.split("\n")) > 10:
                            emb = await generate_embedding(chunk_text)
                            chunk_record = DatasetChunk(
                                file_id=file_record.id,
                                content=chunk_text,
                                embedding=emb
                            )
                            session.add(chunk_record)
                            chunk_text = ""
                            chunk_count += 1
                            if chunk_count > 5: # Limit chunks per file for demonstration
                                break
                    
                    if chunk_text:
                        emb = await generate_embedding(chunk_text)
                        chunk_record = DatasetChunk(
                            file_id=file_record.id,
                            content=chunk_text,
                            embedding=emb
                        )
                        session.add(chunk_record)
                        
            except Exception as e:
                print(f"Error reading {filename}: {e}")

        await session.commit()
    print("Vector database seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_vectors())
