import io
import re
import pandas as pd
from typing import List, Dict, Any, Tuple

class VOCAnalyzer:
    @staticmethod
    def parse_excel_or_csv(file_bytes: bytes, file_name: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        Parses an uploaded Excel or CSV file.
        Attempts to auto-detect review text column and rating columns.
        Returns a list of extracted reviews and metadata for charting (e.g., rating counts).
        """
        try:
            # Load into DataFrame based on file extension
            if file_name.endswith('.csv'):
                # Try UTF-8 first, fallback to CP949 (Korean encoding)
                try:
                    df = pd.read_csv(io.BytesIO(file_bytes), encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(io.BytesIO(file_bytes), encoding='cp949')
            elif file_name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(io.BytesIO(file_bytes))
            else:
                return [], {"error": "Unsupported file format. Please upload CSV or Excel."}
            
            if df.empty:
                return [], {"error": "The uploaded file is empty."}
            
            # 1. Detect Text Column
            # Candidates for review content in Korean/English
            target_cols = ['리뷰', '내용', '리뷰내용', '평가', '리뷰 텍스트', 'content', 'review', 'comment', 'text', 'body']
            text_col = None
            
            # Look for exact / partial match in headers
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if any(cand in col_lower for cand in target_cols):
                    text_col = col
                    break
                    
            # If no matches, search for the column with the highest average string length
            if not text_col:
                str_cols = []
                for col in df.columns:
                    # check if column is object/string type mostly
                    sample_nonnull = df[col].dropna()
                    if not sample_nonnull.empty and all(isinstance(val, str) for val in sample_nonnull.head(5)):
                        avg_len = sample_nonnull.astype(str).str.len().mean()
                        str_cols.append((col, avg_len))
                if str_cols:
                    # Get column with longest text on average
                    str_cols.sort(key=lambda x: x[1], reverse=True)
                    text_col = str_cols[0][0]
                else:
                    # Fallback to the first column
                    text_col = df.columns[0]
            
            # Extract reviews
            reviews = df[text_col].dropna().astype(str).tolist()
            reviews = [r.strip() for r in reviews if len(r.strip()) > 3]
            
            # 2. Detect Rating Column (optional index or score)
            rating_cols = ['평점', '점수', '별점', 'rating', 'score', 'star']
            rating_col = None
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if any(cand in col_lower for cand in rating_cols):
                    rating_col = col
                    break
            
            rating_distribution = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
            has_ratings = False
            
            if rating_col:
                ratings = df[rating_col].dropna()
                # Normalize values to 1-5 scale if they are numbers
                try:
                    ratings_num = pd.to_numeric(ratings, errors='coerce').dropna()
                    for r in ratings_num:
                        # Round to nearest integer and map to 1-5
                        val = int(round(r))
                        if 1 <= val <= 5:
                            rating_distribution[str(val)] += 1
                            has_ratings = True
                except Exception:
                    pass
            
            stats = {
                "total_rows": len(df),
                "valid_reviews_count": len(reviews),
                "detected_text_column": str(text_col),
                "detected_rating_column": str(rating_col) if rating_col else None,
                "has_ratings": has_ratings,
                "rating_distribution": rating_distribution
            }
            
            return reviews, stats
            
        except Exception as e:
            return [], {"error": f"Failed to parse file: {str(e)}"}
            
    @staticmethod
    def parse_raw_text(text: str) -> List[str]:
        """
        Parses raw text pasted directly into the textbox.
        Can split by newline or bullet points.
        """
        if not text:
            return []
            
        # Split by newlines, clean up bullet points or numbering
        raw_lines = text.split('\n')
        reviews = []
        for line in raw_lines:
            line_clean = re.sub(r'^[\s\-\*\d\.\,\(\)\]\[]+', '', line).strip()
            if len(line_clean) > 3:
                reviews.append(line_clean)
        return reviews
