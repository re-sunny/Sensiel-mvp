import os
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Import services
from services.crawler import MarketCrawler
from services.voc_analyzer import VOCAnalyzer
from services.llm_service import LLMService

app = FastAPI(
    title="Cenciel AI Brand-Ops Pipeline",
    description="FastAPI Backend for Cenciel AI Brand-Ops pipeline OS",
    version="1.0.0"
)

# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="templates")

# Pydantic Schemas for Requests
class MarketRequest(BaseModel):
    input: str

class VOCRequest(BaseModel):
    text: str

class ContentRequest(BaseModel):
    selling_point: str

# ----------------- ENDPOINTS -----------------

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """
    Renders the main dashboard index.html page
    """
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/walkthrough", response_class=HTMLResponse)
async def get_walkthrough(request: Request):
    """
    Renders the interactive HTML mockup manual walkthrough.html page
    """
    return templates.TemplateResponse(request=request, name="walkthrough.html")

@app.post("/api/analyze-market")
async def analyze_market(req: MarketRequest, x_api_key: Optional[str] = Header(None)):
    """
    Endpoint for Step 1.
    Crawls URL/Keyword and runs LLM analysis.
    """
    if not req.input.strip():
        raise HTTPException(status_code=400, detail="입력값은 비어있을 수 없습니다.")
        
    try:
        # Crawl input site/keyword
        crawler_data = await MarketCrawler.crawl_competitor(req.input)
        
        # Invoke market LLM analyzer
        llm_data = await LLMService.analyze_market(req.input, x_api_key)
        
        return {
            "status": "success",
            "crawler_data": crawler_data,
            "llm_data": llm_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시장 분석 중 오류 발생: {str(e)}")

@app.post("/api/analyze-voc")
async def analyze_voc(req: VOCRequest, x_api_key: Optional[str] = Header(None)):
    """
    Endpoint for Step 2 (Pasted Text).
    Parses pasted reviews and extracts insights via LLM.
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="분석할 리뷰 텍스트를 입력해 주세요.")
        
    try:
        # Parse pasted multiline text
        reviews = VOCAnalyzer.parse_raw_text(req.text)
        
        if not reviews:
            raise HTTPException(status_code=400, detail="텍스트 내부에 유효한 리뷰 문장이 발견되지 않았습니다.")
            
        # Run LLM analysis on reviews list
        llm_data = await LLMService.analyze_voc(reviews, x_api_key)
        
        return {
            "status": "success",
            "stats": {
                "valid_reviews_count": len(reviews),
                "detected_text_column": "직접 붙여넣기 텍스트",
                "has_ratings": False,
                "rating_distribution": {}
            },
            "llm_data": llm_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VOC 분석 중 오류 발생: {str(e)}")

@app.post("/api/upload-voc")
async def upload_voc(file: UploadFile = File(...), x_api_key: Optional[str] = Header(None)):
    """
    Endpoint for Step 2 (Excel/CSV Upload).
    Loads review files to extract statistics and key marketing ideas.
    """
    filename = file.filename
    if not filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="지원하지 않는 확장자입니다. Excel(.xlsx) 또는 CSV 파일만 업로드해 주세요.")
        
    try:
        file_bytes = await file.read()
        
        # Parse spreadsheet file
        reviews, stats = VOCAnalyzer.parse_excel_or_csv(file_bytes, filename)
        
        if "error" in stats:
            raise HTTPException(status_code=400, detail=stats["error"])
            
        if not reviews:
            raise HTTPException(status_code=400, detail="해당 리뷰 파일에서 텍스트 행을 추출하지 못했습니다.")
            
        # Run LLM analysis on reviews list (Limit to top 30 to avoid token limits in trial keys)
        llm_data = await LLMService.analyze_voc(reviews[:30], x_api_key)
        
        return {
            "status": "success",
            "stats": stats,
            "llm_data": llm_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 파싱 중 에러 발생: {str(e)}")

@app.post("/api/generate-content")
async def generate_content(req: ContentRequest, x_api_key: Optional[str] = Header(None)):
    """
    Endpoint for Step 3.
    Uses selected selling point to write platform copies.
    """
    if not req.selling_point.strip():
        raise HTTPException(status_code=400, detail="소구점을 한 줄 입력해 주세요.")
        
    try:
        llm_data = await LLMService.generate_marketing_content(req.selling_point, x_api_key)
        return {
            "status": "success",
            "llm_data": llm_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"마케팅 카피 생성 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Local boot config
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
