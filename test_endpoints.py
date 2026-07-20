import httpx
import asyncio

async def test_all():
    async with httpx.AsyncClient() as client:
        # 1. Test GET /
        print("Testing GET / ...")
        res = await client.get("http://127.0.0.1:8000/")
        print(f"Status: {res.status_code}")
        assert res.status_code == 200
        assert "<title>Cenciel AI Brand-Ops Pipeline</title>" in res.text
        print("GET / passed successfully!\n")

        # 2. Test POST /api/analyze-market
        print("Testing POST /api/analyze-market ...")
        res = await client.post("http://127.0.0.1:8000/api/analyze-market", json={"input": "PDRN 세럼"})
        print(f"Status: {res.status_code}")
        assert res.status_code == 200
        data = res.json()
        print("Keywords:", data["llm_data"]["keywords"])
        print("USP count:", len(data["llm_data"]["usp"]))
        print("Targeting count:", len(data["llm_data"]["targeting"]))
        assert len(data["llm_data"]["keywords"]) == 5
        print("POST /api/analyze-market passed successfully!\n")

        # 3. Test POST /api/analyze-voc
        print("Testing POST /api/analyze-voc ...")
        sample_reviews = "제형은 좋은데 끈적거림이 강해요\n향이 좀 특이하네요\nPDRN 효과가 좋아 여드름성 붉은기에 효과 보았습니다\n스포이트 입구 부분이 굳어서 잘 안나와요"
        res = await client.post("http://127.0.0.1:8000/api/analyze-voc", json={"text": sample_reviews})
        print(f"Status: {res.status_code}")
        assert res.status_code == 200
        data = res.json()
        print("Valid reviews:", data["stats"]["valid_reviews_count"])
        print("Pain points:", [p["category"] for p in data["llm_data"]["pain_points"]])
        print("Ideas:", [i["concept"] for i in data["llm_data"]["ideas"]])
        print("Selling points:", data["llm_data"]["selling_points"])
        assert len(data["llm_data"]["selling_points"]) > 0
        print("POST /api/analyze-voc passed successfully!\n")

        # 4. Test POST /api/generate-content
        print("Testing POST /api/generate-content ...")
        selling_point = "끈적임 없이 수분만 꽉 채워주는 신개념 깃털 밀착 PDRN 리페어 세럼"
        res = await client.post("http://127.0.0.1:8000/api/generate-content", json={"selling_point": selling_point})
        print(f"Status: {res.status_code}")
        assert res.status_code == 200
        data = res.json()
        insta = data["llm_data"]["instagram"]
        blog = data["llm_data"]["naver_blog"]
        sf = data["llm_data"]["shortform"]
        print("Instagram captions:", insta["caption"][:100] + "...")
        print("Instagram slides Count:", len(insta["slides"]))
        print("Blog SEO Title:", blog["title"])
        print("Shortform concept:", sf["concept"])
        assert len(insta["slides"]) == 5
        assert len(blog["body"]) == 3
        assert len(sf["scenes"]) >= 3
        print("POST /api/generate-content passed successfully!\n")

    print("ALL API ENDPOINTS VALIDATED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(test_all())
