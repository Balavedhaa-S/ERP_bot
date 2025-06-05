import os
import redis
import json
from dotenv import load_dotenv
from rag.qa_chain import create_qa_chain

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Connect to Redis using REDIS_URL
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# ✅ Create LangChain QA chain once
qa_chain = create_qa_chain()

# ✅ Main handler function
async def handle_query(q: str):
    print("🟢 Received query:", q)

    try:
        # 🔍 Check Redis cache first
        cached = r.get(q)
        print("🔍 Redis raw cache result:", cached)

        if cached:
            print("✅ Answer served from Redis cache")
            return {"answer": json.loads(cached)}

        # ❌ Not in cache → run LangChain
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, qa_chain.invoke, q)

        answer_obj = {
            "query": q,
            "result": response if isinstance(response, str) else str(response)
        }

        # 💾 Store in Redis with TTL (1 hour)
        r.setex(q, 3600, json.dumps(answer_obj))
        print("💾 Answer cached in Redis.")
        return {"answer": answer_obj}

    except Exception as e:
        print("❌ Error in handle_query:", str(e))
        return {"error": "Something went wrong while processing the query."}