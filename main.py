from fastapi import FastAPI, Response
from pydantic import BaseModel
import uvicorn
import redis
import psycopg2

app = FastAPI()

class HealthCheck(BaseModel):
    status: str
    database: str
    redis: str

@app.get("/health-check")
async def health_check():
    try:
        # Redis status
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        redis_status = redis_client.ping()
        redis_status = "OK" if redis_status else "Redis is not responding"

        # Database status
        conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="myuser",
            password="mypassword"
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        row = cur.fetchone()
        cur.close()
        conn.close()
        database_status = "OK" if row else "Database is not responding"

        return HealthCheck(status="OK", database=database_status, redis=redis_status)
    except Exception as e:
        return HealthCheck(status="ERROR", database=str(e), redis=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Kodda quyidagilar qo'llangan:

- FastAPI frameworki
- Pydantic uchun BaseModel
- Uvicorn uchun FastAPI serveri
- Redis uchun Redis client
- PostgreSQL uchun psycopg2

Kodda quyidagilar amalga oshiriladi:

- `/health-check` endpointi yaratiladi
- Endpointda Redis va PostgreSQL statusi tekshiriladi
- Agar har ikki status "OK" bo'lsa, endpoint "OK" statusi bilan javob qaytaradi
- Agar har ikki status "ERROR" bo'lsa, endpoint "ERROR" statusi bilan javob qaytaradi
- Agar biror status "ERROR" bo'lsa, endpoint "ERROR" statusi bilan javob qaytaradi va statusni tekshirilgan xatoni keltiradi
