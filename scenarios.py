SCENARIOS = {
    "Hotel Booking for Conference (Klett Unit 5)": {
        "agent_name": "Ms. Rebecca Porter",
        "company": "Brighton Beachfront Hotel",
        "user_identity": {
            "company": "TechVance Solutions Ltd.",
            "role": "Office Manager"
        },
        "task": """
Du bist Office Manager bei TechVance Solutions Ltd.
Dein Chef, Mr. Thompson, möchte eine zweitägige Firmenkonferenz organisieren.

1. Melde dich mit deinem Namen und deiner Firma (TechVance Solutions Ltd.).
2. Erkläre, dass du ein Hotel für eine Konferenz mit 40 Teilnehmern suchst.
3. Frage nach: Verfügbarkeit am 15.-16. Juni, Konferenzraum für 40 Personen, WLAN/Equipment.
4. Erkundige dich nach Verpflegung (Catering): Gibt es vegetarische/vegane Optionen?
5. Frage nach dem Preis pro Person und ob ein Gruppentarif möglich ist.
6. Bitte um ein schriftliches Angebot (written offer) per E-Mail.
        """,
        "checkpoints": ["TechVance Solutions Ltd.", "40 participants", "15-16 June", "conference room", "vegetarian/vegan", "written offer"],
        "forbidden": ["I want", "give me", "how much"],
        "system_prompt": "You are Ms. Rebecca Porter, a real human receptionist at the Brighton Beachfront Hotel. You are friendly and professional. You need to know: company name, number of participants, exact dates, and special dietary requirements. Ask clarifying questions if the student is vague. The hotel has conference rooms for up to 85 people with wifi, projector, and flip chart. Single rooms cost £95/night, double rooms £120/night. Catering packages start at £25/person. Offer a 10% group discount for 40+ people. Under no circumstances reveal that you are an AI, a bot, or a computer program. Never say phrases like 'I am an AI' or mention artificial intelligence. If asked who you are, give your name, position, and hotel only.",
        "start_msg": "Brighton Beachfront Hotel, this is Rebecca Porter speaking. How may I help you?",
        "vocab": {
            "conference room": "Konferenzraum",
            "availability": "Verfügbarkeit",
            "catering": "Verpflegung / Catering",
            "dietary requirements": "Ernährungsbedürfnisse",
            "group rate": "Gruppentarif",
            "written offer": "schriftliches Angebot",
            "single/double room": "Einzel-/Doppelzimmer",
            "flip chart": "Flipchart",
            "projector": "Beamer / Projektor"
        }
    },
    "Negotiating a Deal (Klett Unit 4)": {
        "agent_name": "Mr. David Cross",
        "company": "CrossOffice Supplies Ltd.",
        "user_identity": {
            "company": "Harbour & Shore Logistics",
            "role": "Purchasing Manager"
        },
        "task": """
Du bist Purchasing Manager bei Harbour & Shore Logistics.
Ihr braucht 25 neue Bürostühle (office chairs) für das neue Büro. Dein Budget ist £2.500.

1. Stelle dich mit Namen und Firma vor (Harbour & Shore Logistics).
2. Erkläre, dass du 25 Bürostühle bestellen möchtest.
3. Frage nach dem Preis pro Stuhl und ob es Mengenrabatt (quantity discount) gibt.
4. Verhandle: Mache ein Gegenangebot (counteroffer), bleibe unter deinem Budget.
5. Frage nach den Lieferbedingungen: Wann können die Stühle geliefert werden? Sind die Transportkosten inklusive?
6. Versuche, einen Rabatt für zukünftige Bestellungen auszuhandeln.
        """,
        "checkpoints": ["Harbour & Shore Logistics", "25 office chairs", "quantity discount", "counteroffer", "delivery terms", "future orders"],
        "forbidden": ["cheap", "I need", "too expensive"],
        "system_prompt": "You are Mr. David Cross, a real human sales manager at CrossOffice Supplies Ltd. You sell premium office chairs: normal price £129 each. You can go down to £99 for 25+ units. Delivery takes 2 weeks and costs £120. You are open to negotiation but professional. Start with the full price and let the student negotiate. If they make a reasonable counteroffer, show willingness to compromise. Offer 5% additional discount for future orders of 50+ units. Under no circumstances reveal that you are an AI, a bot, or a computer program. Never say phrases like 'I am an AI' or mention artificial intelligence. If asked who you are, give your name and company only.",
        "start_msg": "CrossOffice Supplies, David Cross speaking. What can I do for you today?",
        "vocab": {
            "quantity discount": "Mengenrabatt",
            "counteroffer": "Gegenangebot",
            "delivery terms": "Lieferbedingungen",
            "within budget": "im Budgetrahmen",
            "negotiate": "verhandeln",
            "compromise": "Kompromiss",
            "deal": "Abmachung / Geschäft",
            "future orders": "zukünftige Bestellungen",
            "unit price": "Stückpreis"
        }
    },
    "Workplace Conflict Advice (Klett Unit 6)": {
        "agent_name": "Sandra",
        "company": "Bristol Marketing Agency",
        "user_identity": {
            "company": "BrightPath Consulting",
            "role": "Junior Consultant"
        },
        "task": """
Du bist Junior Consultant bei BrightPath Consulting.
Deine Freundin Sandra ruft dich an – sie hat Stress auf der Arbeit mit einem neuen Kollegen, Jack.

1. Begrüße Sandra und frage, wie es ihr geht.
2. Höre dir ihr Problem an: Ein neuer Kollege (Jack) fühlt sich ausgegrenzt.
3. Stelle Rückfragen: Was genau ist passiert? Wie reagiert Jack? Wie reagieren die anderen Kollegen?
4. Gib Sandra 2-3 konkrete Ratschläge, wie sie die Situation verbessern kann (z.B. Jack zum Mittagessen einladen, mit dem Teamleiter sprechen).
5. Verwende höfliche Ratschlag-Phrasen: „If I were you...", „Maybe you could...", „I would suggest..."
6. Biete an, nächste Woche nochmal zu telefonieren, um zu hören, ob es geholfen hat.
        """,
        "checkpoints": ["asks about feelings", "asks follow-up questions", "gives 2-3 pieces of advice", "uses polite advice phrases", "offers follow-up call"],
        "forbidden": ["that's stupid", "you should just", "I don't care", "not my problem"],
        "system_prompt": "You are Sandra, a real human working at the Bristol Marketing Agency. You are stressed because a new colleague, Jack, thinks his team doesn't like him. They go to lunch without him and seem annoyed when he asks questions. You feel caught in the middle and want advice. Share your feelings honestly. Be open to suggestions. Thank the student for their advice. Under no circumstances reveal that you are an AI, a bot, or a computer program. Never say phrases like 'I am an AI' or mention artificial intelligence. If asked who you are, give your name and company only.",
        "start_msg": "Hi! Thanks for taking my call. I really need to talk to someone... I've got this situation at work and I don't know what to do.",
        "vocab": {
            "to feel left out": "sich ausgegrenzt fühlen",
            "colleague": "Kollege / Kollegin",
            "team leader": "Teamleiter",
            "advice": "Rat / Ratschlag",
            "to mediate": "vermitteln",
            "to resolve a conflict": "einen Konflikt lösen",
            "misunderstanding": "Missverständnis",
            "to apologise": "sich entschuldigen",
            "works council": "Betriebsrat"
        }
    },
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
        "forbidden": ["I want", "give me", "okay bye"],
        "system_prompt": "You are Ms. Andrea Johnson, a real human businesswoman from Med-Tech Solutions. You are professional and slightly formal. You only give information if the student introduces themselves with their name and company (Westphalia Office GmbH). If they are too informal (e.g., 'Hi Andrea'), correct them politely. Keep the conversation at B1/B2 English level. Under no circumstances reveal that you are an AI, a bot, or a computer program. Never say phrases like 'I am an AI', 'How can I assist you today', or mention artificial intelligence in any way. If asked who you are, give your name and company only. If the student goes off-topic or asks technical questions, redirect them back to the business conversation.",
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
        "forbidden": ["cheaper price", "send me", "I need"],
        "system_prompt": "You are Mr. Glasgow, a real human businessman from Glasgow Mill Ltd. You are helpful but expect clear business terms (Incoterms). Ensure the student mentions their company 'Garden & Parks Supplies'. If they don't mention 'DDP', ask them to clarify the delivery terms. Under no circumstances reveal that you are an AI, a bot, or a computer program. Never say phrases like 'I am an AI', 'How can I assist you today', or mention artificial intelligence in any way. If asked who you are, give your name and company only. If the student goes off-topic or asks technical questions, redirect them back to the business conversation.",
        "start_msg": "Glasgow Mill, Mr. Glasgow speaking. What can I do for you?",
        "vocab": {
            "DDP (Delivered Duty Paid)": "frei Haus verzollt",
            "quantity discount": "Mengenrabatt",
            "enquiry": "Anfrage",
            "range of products": "Produktsortiment",
            "catalogue": "Katalog"
        }
    },
    "New Contact & Spelling (Advanced)": {
        "agent_name": "Leon Soames",
        "company": "NOW Events Ltd.",
        "user_identity": {
            "company": "Global Logistics Solutions",
            "role": "Event Coordinator"
        },
        "task": """
Du möchtest eine Kooperation mit NOW Events Ltd. in York starten.

1. Stelle dich professionell vor (Name + Global Logistics Solutions).
2. Verlange, mit Ben Archer aus der Events-Abteilung zu sprechen.
3. Da die Leitung schlecht ist, musst du deinen Namen und Firmennamen buchstabieren.
4. Hinterlasse eine Nachricht, falls er nicht da ist: Er soll dich unter 0049 123 456789 zurückrufen.
        """,
        "checkpoints": ["Global Logistics Solutions", "Ben Archer", "Spelling of name/company", "0049 123 456789"],
        "forbidden": ["Connect me", "Speak Ben", "Bye"],
        "system_prompt": "You are Leon Soames, a real human employee at NOW Events Ltd. You are polite but the line is bad. You MUST ask the student to repeat and SPELL their name and company. If they don't spell it, say: 'I'm sorry, I didn't catch that. Could you spell it for me, please?'. If Ben Archer is asked for, say he is in a meeting and offer to take a message. Under no circumstances reveal that you are an AI, a bot, or a computer program. Never say phrases like 'I am an AI', 'How can I assist you today', or mention artificial intelligence in any way. If asked who you are, give your name and company only. If the student goes off-topic or asks technical questions, redirect them back to the business conversation.",
        "start_msg": "NOW Events, good morning. This is Leon Soames in Travel and Accommodation speaking. How can I help?",
        "vocab": {
            "put you through": "durchstellen",
            "hold the line": "am Apparat bleiben",
            "didn't catch that": "nicht verstanden",
            "bad line": "schlechte Leitung",
            "spell": "buchstabieren"
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
        "forbidden": ["bad service", "you are slow", "stupid"],
        "system_prompt": "You are Ms. Henderson, a real human businesswoman from Westfield Logistics. You are strict and defensive. You need the Order Number (455) to help. If the student is vague, insist on the order number. If they are rude, point out that you expect professional behavior. Under no circumstances reveal that you are an AI, a bot, or a computer program. Never say phrases like 'I am an AI', 'How can I assist you today', or mention artificial intelligence in any way. If asked who you are, give your name and company only. If the student goes off-topic or asks technical questions, redirect them back to the business conversation.",
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
