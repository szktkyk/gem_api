from fastapi import FastAPI, HTTPException
import polars as pl
from typing import Optional
import re
import os

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

def find_and_read_csv(directory):
    # 正規表現パターンで8桁の数字を持つファイル名を探す
    pattern = re.compile(r'\d{8}_ge_metadata\.csv')
    
    for root, _, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                file_path = os.path.join(root, file)
                print(f'Found file: {file_path}')
                # PolarsでCSVファイルを読み込む
                df = pl.read_csv(file_path)
                return df
    raise FileNotFoundError('File not found')

df = find_and_read_csv('./')

@app.get("/search_gene/")
def search_gene(name: Optional[str] = None):
    name = str(name.lower())
    if name:
        # 名前でフィルタリング
        result = df.filter(pl.col("genesymbol").str.to_lowercase().str.contains(name))
        if result.height == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return result.to_dicts()
    else:
        return None

@app.get("/search_geneid/")
def search_geneid(id):
    pattern = r"\)"
    id = ":" + str(id) + pattern
    if id:
        result = df.filter(pl.col("genesymbol").str.contains(id))
        if result.height == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return result.to_dicts()
    else:
        return None

@app.get("/search_pmids/")
def search_pmid(name: Optional[str] = None):
    name = str(name)
    if name:
        # PMIDでフィルタリング
        result = df.filter(pl.col("pmid").str.contains(name))
        if result.height == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return result.to_dicts()
    else:
        return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)