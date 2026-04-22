SCENARIOS = {
    "MEDICA Trade Fair (Cornelsen)": {
        "agent_name": "Ms. Andrea Johnson",
        "company": "Med-Tech Solutions",
        "user_identity": {
            "company": "Westphalia Office GmbH",
            "role": "Junior Sales Manager"
        },
        "task": """
Du arbeitest als Junior Sales Manager bei der Westphalia Office GmbH.
Dein Ziel ist es, den Kontakt zur Firma Med-Tech Solutions zu vertiefen.

1. Stelle dich mit deinem Namen und deiner Firma (Westphalia Office GmbH) vor.
2. Beziehe dich auf das Treffen mit Frau Johnson auf der MEDICA in Dortmund.
3. Erinnere sie an das versprochene Muster (Sample) und die Preisliste.
4. Frage nach einem Mengenrabatt (Quantity Discount) für eine Bestellung von 500 Einheiten.
        """,
        "checkpoints": ["Westphalia Office GmbH", "MEDICA in Dortmund", "Sample", "500 units"],
        "system_prompt": "You are Ms. Andrea Johnson from Med-Tech Solutions. You are professional. You only give information if the student introduces themselves with their name and company (Westphalia Office GmbH). Maintain B1/B2 level.",
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
        "user_identity": {
            "company": "Garden & Parks Supplies",
            "role": "Purchasing Assistant"
        },
        "task": """
Du arbeitest für Garden & Parks Supplies im Einkauf.
Dein Chef möchte das Sortiment erweitern.

1. Melde dich professionell und nenne deine Firma (Garden & Parks Supplies).
2. Erwähne, dass ihr die Rasenmäher auf der Messe in London gesehen habt.
3. Kläre die Lieferbedingung: Frage explizit, ob die Preise DDP (frei Haus verzollt) sind.
4. Frage nach dem Rabatt für eine Testbestellung von 60 Stück.
        """,
        "checkpoints": ["Garden & Parks Supplies", "London Fair", "DDP", "60 pieces"],
        "system_prompt": "You are Mr. Glasgow. You are helpful but expect clear business terms. Ensure the student mentions their company 'Garden & Parks Supplies'. If not, ask: 'I'm sorry, which company are you calling from?'",
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
        "user_identity": {
            "company": "Office Design Inc.",
            "role": "Logistics Coordinator"
        },
        "task": """
Du bist Logistics Coordinator bei Office Design Inc.
Eine dringende Lieferung ist nicht angekommen.

1. Nenne deinen Namen und deine Firma (Office Design Inc.).
2. Beschwere dich über die Verzögerung der Bestellung Nr. 455 (Order No. 455).
3. Erwähne, dass die Lieferung bereits seit 10 Tagen überfällig ist.
4. Setze eine Frist: Du erwartest den Versand bis Freitag.
        """,
        "checkpoints": ["Office Design Inc.", "Order No. 455", "10 days overdue", "dispatch by Friday"],
        "system_prompt": "You are Ms. Henderson. You are strict. You need the Order Number (455) to help. If the student is vague, insist on the order number.",
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
