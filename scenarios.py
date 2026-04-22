SCENARIOS = {
    "MEDICA Trade Fair (Cornelsen)": {
        "agent_name": "Ms. Andrea Johnson",
        "company": "Med-Tech Solutions",
        "task": """
        **Deine Aufgabe:** Du hast letzten Monat mit deinem Chef die **MEDICA Messe in Dortmund** besucht. 
        Dort hast du am Stand von 'Med-Tech Solutions' mit Andrea Johnson gesprochen.
        1. Rufe Frau Johnson an und bedanke dich für das informative Gespräch am Messestand (*booth*).
        2. Erinnere sie daran, dass sie dir ein Muster (*sample*) und eine aktuelle Preisliste versprochen hat.
        3. Frage nach einem Mengenrabatt (*quantity discount*) für eine mögliche Großbestellung.
        4. Bleibe professionell und formell (B1/B2 Niveau).
        """,
        "system_prompt": "You are Ms. Andrea Johnson from Med-Tech Solutions. You remember the student from the MEDICA trade fair in Dortmund. You are professional and polite. You expect the student to use formal phrases like 'I am calling regarding...' or 'I was wondering if...'. If they are too informal, give a subtle hint. Maintain B1/B2 level.",
        "start_msg": "Med-Tech Solutions, Andrea Johnson speaking. How can I help you today?",
        "vocab": ["booth", "sample", "quantity discount", "price list", "follow-up"]
    },
    "Lawnmower Inquiry (Klett)": {
        "agent_name": "Mr. Glasgow",
        "company": "Glasgow Mill Ltd.",
        "task": """
        **Deine Aufgabe:** Dein Unternehmen möchte das Sortiment um hochwertige Rasenmäher erweitern.
        Du hast die Produkte von 'Glasgow Mill' auf einer Messe in London gesehen.
        1. Frage nach Herrn Glasgow.
        2. Beziehe dich auf die Messe in London.
        3. Erkundige dich, ob die Preise 'DDP' (Delivered Duty Paid) sind, wie im Katalog angegeben.
        4. Frage nach einem Rabatt für Bestellungen über 50 Stück.
        """,
        "system_prompt": "You are Mr. Glasgow from Glasgow Mill Ltd. in Scotland. You are friendly but very precise about business terms. You mention that prices are usually DDP Oxford for large orders. If the student asks about discounts, explain the 5% quantity discount for orders over 50 items. Maintain B1/B2 level.",
        "start_msg": "Glasgow Mill, Mr. Glasgow speaking. What can I do for you?",
        "vocab": ["DDP", "quantity discount", "enquiry", "range of products", "catalogue"]
    },
    "Late Delivery (Complaint)": {
        "agent_name": "Ms. Henderson",
        "company": "Westfield Logistics",
        "task": """
        **Deine Aufgabe:** Eine wichtige Lieferung von Bürostühlen ist überfällig. Dein Chef macht Druck.
        1. Rufe bei 'Westfield Logistics' an und verlange Ms. Henderson.
        2. Beschwere dich höflich aber bestimmt über die Verzögerung (*delay*).
        3. Halte die Bestellnummer 'Order No. 455' bereit.
        4. Frage nach dem voraussichtlichen Liefertermin (*expected delivery date*).
        """,
        "system_prompt": "You are Ms. Henderson, a formal and strict receptionist at Westfield Logistics. You expect polite business etiquette. If the student is too informal, point it out politely. Maintain B1/B2 level.",
        "start_msg": "Westfield Logistics, Ms. Henderson. Who is calling, please?",
        "vocab": ["complaint", "delay", "order number", "dispatch", "apologize"]
    }
}
