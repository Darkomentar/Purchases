import requests

r = requests.get("http://localhost:888/tickers/1",
                params = {"name_or_price": False})
print(r.content)
print(r, '\n')

r = requests.get("http://localhost:888/tickers/1")
print(r.content)
print(r, '\n')

r = requests.get("http://localhost:888/ticker_search_by_name",
                 params = {"name": "ROSN"})
print(r.content)
print(r, '\n')

r = requests.get("http://localhost:888/tickers_search_by_price/",
                 params = {"low_price": 123, "high_price": 125}) 
print(r.content)
print(r, '\n')

r = requests.post("http://localhost:888/add_ticker/",
                 json = {"name": "SIBN", "price": 2500}) 
print(r.content)
print(r, '\n')

r = requests.get("http://localhost:888/return_people/",
                 params = {"name": "Timur", "age": 22, "university": "UGNTU", "gender": "man"}) 
print(r.content)
print(r, '\n')