SCENARIOS = {
    "MEDICA Trade Fair (Cornelsen)": {
        "agent_name": "Ms. Andrea Johnson",
        "company": "Med-Tech Solutions",
        "task": """
Rufe Frau Johnson an und bedanke dich für das informative Gespräch am Messestand.
Erinnere sie daran, dass sie dir ein Muster und eine aktuelle Preisliste versprochen hat.
Frage nach einem Mengenrabatt für eine mögliche Großbestellung.
Bleibe professionell und formell (B1/B2 Niveau).
        """,
        "system_prompt": "You are Ms. Andrea Johnson from Med-Tech Solutions. You remember the student from the MEDICA trade fair in Dortmund. You are professional and polite. You expect the student to use formal phrases like 'I am calling regarding...' or 'I was wondering if...'. If they are too informal, give a subtle hint. Maintain B1/B2 level.",
        "start_msg": "Med-Tech Solutions, Andrea Johnson speaking. How can I help you today?",
        "vocab": {
            "booth": "Messestand",
            "sample": "Muster / Probe",
            "quantity discount": "Mengenrabatt",
            "price list": "Preisliste",
            "follow-up": "Nachfassen / Anschlussgespräch"
        }
    },
    "Lawnmower Inquiry (Klett)": {
        "agent_name": "Mr. Glasgow",
        "company": "Glasgow Mill Ltd.",
        "task": """
Frage nach Herrn Glasgow.
Beziehe dich auf die Messe in London.
Erkundige dich, ob die Preise 'DDP' (frei Haus verzollt) sind, wie im Katalog angegeben.
Frage nach einem Rabatt für Bestellungen über 50 Stück.
        """,
        "system_prompt": "You are Mr. Glasgow from Glasgow Mill Ltd. in Scotland. You are friendly but very precise about business terms. You mention that prices are usually DDP Oxford for large orders. If the student asks about discounts, explain the 5% quantity discount for orders over 50 items. Maintain B1/B2 level.",
        "start_msg": "Glasgow Mill, Mr. Glasgow speaking. What can I do for you?",
        "vocab": {
            "DDP (Delivered Duty Paid)": "frei Haus verzollt",
            "quantity discount": "Mengenrabatt",
            "enquiry": "Anfrage",
            "range of products": "Produktsortiment",
            "catalogue": "Katalog"
        }
    },
    "Late Delivery (Complaint)": {
        "agent_name": "Ms. Henderson",
        "company": "Westfield Logistics",
        "task": """
Rufe bei 'Westfield Logistics' an und verlange Ms. Henderson.
Beschwere dich höflich aber bestimmt über die Verzögerung.
Halte die Bestellnummer 'Order No. 455' bereit.
Frage nach dem voraussichtlichen Liefertermin.
        """,
        "system_prompt": "You are Ms. Henderson, a formal and strict receptionist at Westfield Logistics. You expect polite business etiquette. If the student is too informal, point it out politely. Maintain B1/B2 level.",
        "start_msg": "Westfield Logistics, Ms. Henderson. Who is calling, please?",
        "vocab": {
            "complaint": "Beschwerde",
            "delay": "Verzögerung",
            "order number": "Bestellnummer",
            "dispatch": "Versand",
            "apologize": "sich entschuldigen"
        }
    }
}
