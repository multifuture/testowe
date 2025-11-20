"""
Story Generator - Aplikacja Streamlit do generowania historii AI
"""

# 1. Importy
import streamlit as st
from openai import OpenAI
import os
from datetime import datetime

# 2. Page config
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Custom CSS w st.markdown()
st.markdown("""
<style>
    /* Główny kontener */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }

    /* Styl dla tytułu */
    .title {
        text-align: center;
        color: #ffffff;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Styl dla podtytułu */
    .subtitle {
        text-align: center;
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Karty z historią */
    .story-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }

    .story-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.2);
    }

    /* Przycisk generowania */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(118, 75, 162, 0.4);
    }

    /* Statystyki */
    .stats-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }

    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    /* Historia w sidebarze */
    .history-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }

    /* Text area */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #667eea;
    }

    /* Select box */
    .stSelectbox select {
        border-radius: 10px;
        border: 2px solid #667eea;
    }

    /* Slider */
    .stSlider {
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 4. Session state initialization
if 'stories' not in st.session_state:
    st.session_state.stories = []

if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv('OPENAI_API_KEY', '')

if 'total_words' not in st.session_state:
    st.session_state.total_words = 0

if 'total_sentences' not in st.session_state:
    st.session_state.total_sentences = 0

# 5. Funkcje pomocnicze
def count_words_and_sentences(text):
    """
    Liczy liczbę słów i zdań w tekście.

    Args:
        text (str): Tekst do analizy

    Returns:
        tuple: (liczba_słów, liczba_zdań)
    """
    words = len(text.split())
    sentences = text.count('.') + text.count('!') + text.count('?')
    return words, sentences


def create_story(prompt, genre, length, temperature, api_key):
    """
    Generuje historię używając OpenAI API.

    Args:
        prompt (str): Temat/prompt historii
        genre (str): Gatunek historii
        length (str): Długość historii
        temperature (float): Temperatura modelu (kreatywność)
        api_key (str): Klucz API OpenAI

    Returns:
        str: Wygenerowana historia lub komunikat o błędzie
    """
    try:
        # Mapowanie długości na liczbę słów
        length_map = {
            "Krótka (100-200 słów)": 150,
            "Średnia (200-400 słów)": 300,
            "Długa (400-600 słów)": 500
        }

        target_words = length_map.get(length, 300)

        # Inicjalizacja klienta OpenAI
        client = OpenAI(api_key=api_key)

        # Tworzenie szczegółowego prompta
        system_prompt = f"""Jesteś kreatywnym pisarzem historii.
Twoim zadaniem jest napisanie {genre.lower()} historii o długości około {target_words} słów.
Historia powinna być wciągająca, dobrze napisana i odpowiednia do gatunku."""

        user_prompt = f"""Napisz {genre.lower()} historię na temat: {prompt}

Wymagania:
- Długość: około {target_words} słów
- Gatunek: {genre}
- Historia powinna mieć wyraźny początek, rozwinięcie i zakończenie
- Użyj żywego języka i ciekawych opisów
- Stwórz interesujących bohaterów

Napisz tylko samą historię, bez dodatkowych komentarzy."""

        # Wywołanie API OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=1500
        )

        story = response.choices[0].message.content
        return story

    except Exception as e:
        return f"❌ Błąd podczas generowania historii: {str(e)}"


# 6. UI Layout
# Nagłówek
st.markdown('<h1 class="title">📖 AI Story Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Generuj unikalne historie z pomocą sztucznej inteligencji</p>', unsafe_allow_html=True)

# Layout z kolumnami
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### ✍️ Ustawienia historii")

    # API Key input
    api_key_input = st.text_input(
        "🔑 Klucz API OpenAI",
        type="password",
        value=st.session_state.api_key,
        help="Wprowadź swój klucz API OpenAI. Możesz go uzyskać na platform.openai.com"
    )

    if api_key_input:
        st.session_state.api_key = api_key_input

    # Prompt input
    story_prompt = st.text_area(
        "📝 Temat/Prompt historii",
        placeholder="Np. 'Kosmonauta odkrywający nową planetę' lub 'Detektyw rozwiązujący tajemniczą sprawę'",
        height=100,
        help="Opisz temat lub główną ideę twojej historii"
    )

    # Ustawienia w dwóch kolumnach
    settings_col1, settings_col2 = st.columns(2)

    with settings_col1:
        genre = st.selectbox(
            "🎭 Gatunek",
            [
                "Science Fiction",
                "Fantasy",
                "Thriller",
                "Romans",
                "Horror",
                "Przygodowa",
                "Detektywistyczna",
                "Komedia"
            ],
            help="Wybierz gatunek historii"
        )

        length = st.selectbox(
            "📏 Długość",
            [
                "Krótka (100-200 słów)",
                "Średnia (200-400 słów)",
                "Długa (400-600 słów)"
            ],
            help="Wybierz przybliżoną długość historii"
        )

    with settings_col2:
        temperature = st.slider(
            "🌡️ Kreatywność (Temperature)",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Wyższe wartości = bardziej kreatywne i nieprzewidywalne historie"
        )

        st.markdown("<br>", unsafe_allow_html=True)

    # Przycisk generowania
    generate_button = st.button("🚀 Generuj Historię", use_container_width=True)

    # Generowanie historii
    if generate_button:
        if not st.session_state.api_key:
            st.error("⚠️ Proszę wprowadzić klucz API OpenAI!")
        elif not story_prompt:
            st.error("⚠️ Proszę wprowadzić temat historii!")
        else:
            with st.spinner("✨ Generuję twoją historię..."):
                story = create_story(
                    story_prompt,
                    genre,
                    length,
                    temperature,
                    st.session_state.api_key
                )

                if not story.startswith("❌"):
                    # Zliczanie słów i zdań
                    words, sentences = count_words_and_sentences(story)
                    st.session_state.total_words += words
                    st.session_state.total_sentences += sentences

                    # Zapisywanie do historii
                    story_data = {
                        'prompt': story_prompt,
                        'genre': genre,
                        'story': story,
                        'words': words,
                        'sentences': sentences,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.stories.insert(0, story_data)

                    st.success("✅ Historia wygenerowana pomyślnie!")
                else:
                    st.error(story)

    # Wyświetlanie ostatniej historii
    if st.session_state.stories:
        st.markdown("---")
        st.markdown("### 📚 Twoja Historia")

        latest_story = st.session_state.stories[0]

        st.markdown(f"""
        <div class="story-card">
            <h4>🎬 {latest_story['genre']}</h4>
            <p><strong>Prompt:</strong> {latest_story['prompt']}</p>
            <hr>
            <p style="text-align: justify; line-height: 1.8; font-size: 1.05rem;">
                {latest_story['story']}
            </p>
            <hr>
            <p style="color: #666; font-size: 0.9rem;">
                📊 {latest_story['words']} słów | {latest_story['sentences']} zdań |
                🕒 {latest_story['timestamp']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Przyciski akcji
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("📋 Kopiuj do schowka", use_container_width=True):
                st.code(latest_story['story'], language=None)
        with action_col2:
            if st.button("💾 Pobierz jako TXT", use_container_width=True):
                st.download_button(
                    label="⬇️ Pobierz",
                    data=latest_story['story'],
                    file_name=f"historia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

with col2:
    st.markdown("### 📊 Statystyki")

    # Statystyki ogólne
    st.markdown(f"""
    <div class="stats-box">
        <div class="stat-number">{len(st.session_state.stories)}</div>
        <div class="stat-label">Wygenerowanych Historii</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="stat-number">{st.session_state.total_words}</div>
        <div class="stat-label">Łączna liczba słów</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-box" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <div class="stat-number">{st.session_state.total_sentences}</div>
        <div class="stat-label">Łączna liczba zdań</div>
    </div>
    """, unsafe_allow_html=True)

    # Info box
    st.markdown("---")
    st.info("""
    **💡 Wskazówki:**
    - Bądź konkretny w swoim prompcie
    - Eksperymentuj z różnymi gatunkami
    - Wyższa temperatura = bardziej kreatywne historie
    - Niższa temperatura = bardziej przewidywalne historie
    """)

    # Reset button
    if st.button("🗑️ Wyczyść wszystkie historie", use_container_width=True):
        st.session_state.stories = []
        st.session_state.total_words = 0
        st.session_state.total_sentences = 0
        st.rerun()

# 7. Sidebar z historią
with st.sidebar:
    st.markdown("## 📜 Historia Generacji")
    st.markdown("---")

    if not st.session_state.stories:
        st.info("Brak historii. Wygeneruj swoją pierwszą historię!")
    else:
        for idx, story in enumerate(st.session_state.stories):
            with st.expander(f"📖 {story['genre']} - {story['timestamp']}", expanded=False):
                st.markdown(f"**Prompt:** {story['prompt']}")
                st.markdown(f"**Słowa:** {story['words']} | **Zdania:** {story['sentences']}")

                if st.button(f"👁️ Zobacz pełną historię", key=f"view_{idx}"):
                    st.markdown("---")
                    st.markdown(story['story'])

                if st.button(f"📥 Pobierz", key=f"download_{idx}"):
                    st.download_button(
                        label="⬇️ Pobierz TXT",
                        data=story['story'],
                        file_name=f"historia_{idx}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key=f"dl_btn_{idx}"
                    )

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>Made with ❤️ using Streamlit</p>
        <p>Powered by OpenAI GPT-3.5</p>
    </div>
    """, unsafe_allow_html=True)
