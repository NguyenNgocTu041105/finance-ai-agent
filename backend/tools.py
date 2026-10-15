"""
Tools cho Finance AI Agent.
Các hàm này sẽ được LLM gọi thông qua Function Calling.

Bao gồm:
- get_stock_price: Lấy giá cổ phiếu mới nhất
- get_company_info: Lấy thông tin công ty
- get_financial_ratios: Lấy chỉ số tài chính với Smart Fallback
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Đảm bảo in tiếng Việt không lỗi trên Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

# Load .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

from vnstock import Market, Fundamental, Company


def get_stock_price(ticker: str) -> dict:
    """
    Lấy giá khớp lệnh và nến OHLCV phiên gần nhất của cổ phiếu.

    Args:
        ticker: Mã cổ phiếu (FPT, HPG, VCB...)

    Returns:
        Dict chứa open, high, low, close, volume, unit.
    """
    try:
        mkt = Market()
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        df = mkt.equity(ticker.upper()).ohlcv(start=start, end=end)

        if df is None or df.empty:
            return {"error": f"Không tìm thấy dữ liệu giá cho mã {ticker}"}

        latest = df.iloc[-1]
        return {
            "ticker": ticker.upper(),
            "date": str(latest["time"]),
            "open": float(latest["open"]),
            "high": float(latest["high"]),
            "low": float(latest["low"]),
            "close": float(latest["close"]),
            "volume": int(latest["volume"]),
            "unit": "nghìn VNĐ",
        }
    except Exception as e:
        return {"error": f"Lỗi lấy giá: {str(e)}"}


def get_company_info(ticker: str) -> dict:
    """Lấy thông tin cơ bản của doanh nghiệp."""
    try:
        comp = Company(symbol=ticker.upper())
        df = comp.overview()

        if df is None or df.empty:
            return {"error": f"Không tìm thấy thông tin cho mã {ticker}"}

        row = df.iloc[0]
        return {
            "ticker": ticker.upper(),
            "exchange": str(row.get("exchange", "N/A")),
            "ceo_name": str(row.get("ceo_name", "N/A")),
            "founded_date": str(row.get("founded_date", "N/A")),
            "listing_date": str(row.get("listing_date", "N/A")),
            "number_of_employees": int(row.get("number_of_employees", 0)) if row.get("number_of_employees") else None,
            "website": str(row.get("website", "N/A")),
            "business_model": str(row.get("business_model", "N/A"))[:500],  # Giới hạn 500 ký tự
        }
    except Exception as e:
        return {"error": f"Lỗi lấy thông tin công ty: {str(e)}"}


def get_financial_ratios(ticker: str) -> dict:
    """
    Lấy chỉ số tài chính với Smart Fallback.
    Với mỗi chỉ số (P/E, P/B, ROE, ROA, EPS), tự tìm quý gần nhất có dữ liệu.

    Args:
        ticker: Mã cổ phiếu

    Returns:
        Dict chứa các chỉ số với format:
        {
            "pe": {"value": 18.5, "quarter": "2025-Q4", "is_latest": False},
            ...
        }
        Nếu chỉ số không có dữ liệu ở bất kỳ quý nào → None.
    """
    try:
        fnd = Fundamental()
        df = fnd.equity(ticker.upper()).ratio(period="quarter")

        if df is None or df.empty:
            return {"error": f"Không tìm thấy chỉ số tài chính cho {ticker}"}

        # Lấy tất cả các cột quý (loại bỏ cột trùng kiểm toán _1)
        quarter_cols = [
            c for c in df.columns
            if "-Q" in str(c) and not str(c).endswith("_1")
        ]
        quarter_cols.sort(reverse=True)  # Mới nhất lên đầu

        if not quarter_cols:
            return {"error": "Không tìm thấy dữ liệu quý phù hợp"}

        # Hàm helper: tìm quý gần nhất có chỉ số này
        def find_latest_value(item_id: str):
            for quarter in quarter_cols:
                ratios_dict = dict(zip(df["item_id"], df[quarter]))
                value = ratios_dict.get(item_id)
                if value is not None:
                    return float(value), quarter
            return None, None

        # Quý mới nhất (để tham chiếu)
        latest_quarter = quarter_cols[0]

        # Tìm cho từng chỉ số
        pe, pe_quarter = find_latest_value("pe_ratio")
        pb, pb_quarter = find_latest_value("pb_ratio")
        roe, roe_quarter = find_latest_value("roe")
        roa, roa_quarter = find_latest_value("roa")
        eps, eps_quarter = find_latest_value("trailing_eps")

        return {
            "ticker": ticker.upper(),
            "latest_quarter": latest_quarter,
            "pe": {
                "value": pe,
                "quarter": pe_quarter,
                "is_latest": pe_quarter == latest_quarter,
            } if pe else None,
            "pb": {
                "value": pb,
                "quarter": pb_quarter,
                "is_latest": pb_quarter == latest_quarter,
            } if pb else None,
            "roe": {
                "value": roe,
                "quarter": roe_quarter,
                "is_latest": roe_quarter == latest_quarter,
            } if roe else None,
            "roa": {
                "value": roa,
                "quarter": roa_quarter,
                "is_latest": roa_quarter == latest_quarter,
            } if roa else None,
            "eps": {
                "value": eps,
                "quarter": eps_quarter,
                "is_latest": eps_quarter == latest_quarter,
            } if eps else None,
        }
    except Exception as e:
        return {"error": f"Lỗi lấy chỉ số tài chính: {str(e)}"}


# ==============================================================================
# MENU KHAI BÁO CÔNG CỤ (TOOLS SCHEMA) CHO LLM
# ==============================================================================
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": (
                "Lấy giá khớp lệnh, giá mở/cao/thấp và khối lượng giao dịch "
                "mới nhất của một mã cổ phiếu."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Mã cổ phiếu, ví dụ: FPT, HPG, VCB",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_info",
            "description": (
                "Lấy thông tin cơ bản của doanh nghiệp: "
                "tên công ty, ngành nghề hoạt động, sàn niêm yết."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Mã cổ phiếu, ví dụ: FPT, VNM",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_financial_ratios",
            "description": (
                "Lấy chỉ số tài chính (P/E, P/B, ROE, ROA, EPS) với Smart Fallback. "
                "Mỗi chỉ số trả về: value (giá trị), quarter (quý lấy dữ liệu), "
                "is_latest (có phải quý mới nhất không). "
                "Nếu is_latest = false, chỉ số đó lấy từ quý cũ hơn "
                "vì quý mới nhất chưa cập nhật."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Mã cổ phiếu, ví dụ: FPT, VNM",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
]

# tên hàm → hàm Python thật
AVAILABLE_TOOLS = {
    "get_stock_price": get_stock_price,
    "get_company_info": get_company_info,
    "get_financial_ratios": get_financial_ratios,
}


if __name__ == "__main__":
    print("=== TEST CÁC TOOL TÀI CHÍNH ===\n")

    print("1. Test get_stock_price('FPT'):")
    print(get_stock_price("FPT"))

    print("\n2. Test get_company_info('FPT'):")
    print(get_company_info("FPT"))

    print("\n3. Test get_financial_ratios('FPT'):")
    print(get_financial_ratios("FPT"))