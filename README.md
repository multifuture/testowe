# AI Story Generator 📖

Aplikacja Streamlit do generowania historii przy użyciu OpenAI API.

## 🚀 Funkcjonalności

- Generowanie historii w różnych gatunkach (Science Fiction, Fantasy, Thriller, Horror, etc.)
- Wybór długości historii (krótka, średnia, długa)
- Kontrola kreatywności (temperature)
- Historia wszystkich wygenerowanych historii
- Statystyki (liczba historii, słów, zdań)
- Pobieranie historii jako pliki TXT
- Responsywny design z gradientami i animacjami

## 📋 Wymagania

- Python 3.x
- Klucz API OpenAI (zarejestruj się na platform.openai.com)

## 🛠️ Instalacja

1. Sklonuj repozytorium:
```bash
git clone <url-repozytorium>
cd testowe
```

2. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

3. (Opcjonalnie) Ustaw zmienną środowiskową z kluczem API:
```bash
export OPENAI_API_KEY='twoj-klucz-api'
```

## 🎮 Uruchomienie

Uruchom aplikację Streamlit:
```bash
streamlit run story_generator.py
```

Aplikacja otworzy się w przeglądarce pod adresem `http://localhost:8501`

## 📖 Użytkowanie

1. Wprowadź swój klucz API OpenAI (jeśli nie ustawiony w zmiennej środowiskowej)
2. Wpisz temat/prompt historii
3. Wybierz gatunek, długość i poziom kreatywności
4. Kliknij "Generuj Historię"
5. Przeglądaj wygenerowane historie w głównym oknie i sidebarze
6. Pobieraj historie jako pliki TXT

## 🏗️ Struktura kodu

- **Importy** - biblioteki Python
- **Page config** - konfiguracja strony Streamlit
- **Custom CSS** - stylowanie w st.markdown()
- **Session state** - zarządzanie stanem aplikacji
- **Funkcje pomocnicze** - create_story(), count_words_and_sentences()
- **UI layout** - interfejs użytkownika z kolumnami
- **Sidebar** - historia generacji

## 🎨 Technologie

- Python 3.x
- Streamlit
- OpenAI Python SDK
- CSS (poprzez st.markdown)

## 📝 Licencja

MIT