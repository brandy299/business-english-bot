SCENARIOS = {
    "Inquiry (Trade Fair)": {
        "agent_name": "Mr. Miller",
        "company": "Eco-Tech Germany",
        "task": """
        **Deine Aufgabe:** Du arbeitest bei der 'Westphalia Office GmbH'. Letzte Woche warst du auf einer Messe in Köln.
        1. Rufe bei 'Eco-Tech Germany' an und verlange Herrn Miller.
        2. Beziehe dich auf das Gespräch an ihrem Messestand (*booth*).
        3. Bitte um einen Katalog und ein Angebot (*quotation*).
        4. Frage nach den Lieferzeiten (*delivery period*).
        """,
        "system_prompt": "You are Mr. Miller from Eco-Tech. A student calls about a trade fair. Be professional, slightly busy but helpful. Maintain B1/B2 level. Do not use complex idioms without explanation.",
        "start_msg": "Eco-Tech Germany, Mr. Miller speaking. How can I help you?",
        "vocab": ["trade fair", "booth", "catalogue", "quotation", "delivery period"]
    },
    "Late Delivery (Complaint)": {
        "agent_name": "Ms. Henderson",
        "company": "Westfield Logistics",
        "task": """
        **Deine Aufgabe:** Eine wichtige Lieferung von Bürostühlen ist überfällig. Dein Chef macht Druck.
        1. Rufe bei 'Westfield Logistics' an und verlange Ms. Henderson.
        2. Beschwere dich höflich aber bestimmt über die Verzögerung (*delay*).
        3. Halte eine fiktive Bestellnummer bereit (z.B. Order No. 455).
        4. Verlange eine schnelle Lösung.
        """,
        "system_prompt": "You are Ms. Henderson, a formal and strict receptionist at Westfield Logistics. You expect polite business etiquette. If the student is too informal, point it out politely. Maintain B1/B2 level.",
        "start_msg": "Westfield Logistics, Ms. Henderson. Who is calling, please?",
        "vocab": ["complaint", "delay", "order number", "dispatch", "apologize"]
    }
}
