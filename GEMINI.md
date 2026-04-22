# Projekt-Gedächtnis: Business Communication Lab

## 🎯 Projekt-Ziel
Entwicklung eines KI-gestützten Telefontrainers für Business English, speziell für kaufmännische Berufskollegs in NRW (Industriekaufleute/Büromanagement).

## 🛠 Technischer Stack
- **Framework:** Python mit Streamlit.
- **KI-Modell:** `google/gemma-4-26b-a4b-it` via OpenRouter.
- **Hosting:** GitHub + Streamlit Cloud.

## 🎨 Design-System ("Warm Academic Workbench")
- **Ästhetik:** Hochwertiger, professioneller Look (kein "AI-Slop").
- **Farbgebung:** Hintergrund in warmem Sandstein (`#ede7de`), Chatbox in absolutem Reinweiß (`#ffffff`) für garantierten Kontrast.
- **Typografie:** `Crimson Pro` (Serif) für akademische Titel, `Plus Jakarta Sans` für UI, `Georgia` für Aufgaben.
- **Elemente:** Custom HTML Chat-Renderer mit Avataren (💼 Partner, 🎓 Student) und farbigen Sprechblasen.

## 🎓 Didaktische Features
- **Identity-System:** Schüler erhalten eine feste Firmen-Identität und Rolle pro Szenario.
- **Vocabulary Bank:** Zweisprachige Vokabellisten (Englisch/Deutsch) pro Modul.
- **Smart Evaluation:** Die KI prüft am Ende des Gesprächs explizit:
    - Wurde die eigene Firma korrekt genannt?
    - Wurden alle inhaltlichen Checkpoints (Daten, Fakten) erwähnt?
    - Höflichkeit und kaufmännische Etikette.

## 📚 Datenbasis (Bibliothek)
- Cornelsen Buch Kompendium (Fokus Vokabeln/Trade Fair).
- Klett Business to Business (Fokus kaufmännische Szenarien).
- NRW Bildungsplan (Niveau B1/B2).

## 🚀 Nächste Schritte
- [ ] Export-Funktion für das Feedback (PDF oder Text).
- [ ] Integration weiterer Szenarien aus der `bibliothek/`.
- [ ] Verfeinerung der "Strenge" der KI-Geschäftspartner.
