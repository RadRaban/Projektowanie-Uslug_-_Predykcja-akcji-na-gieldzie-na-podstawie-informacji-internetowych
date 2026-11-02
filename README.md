## Instalacja

1. Sklonuj repo
2. Pobierz zależności
```pip install -r requirements.txt```
3. Stwórz plik ```.env``` i uzupełnij według wzorca ```.envexample``` 
Przykład
```
NEWS_API_KEY=123          <- klucz z newsapi.org
XAI_API_KEY=123           <- klucz api do modelu groka
EVENT_REGISTRY_API_KEY=123          <- klucz api z newsapi.ai
```

**NIE PUSHUJ SWOJEGO ```.env```**

4. Uruchom ```py main.py```
