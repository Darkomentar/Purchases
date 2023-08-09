import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import uvicorn

if __name__ == "__main__":
    uvicorn.run("fast_api_programm:app", host="localhost", port=888, reload=True)
