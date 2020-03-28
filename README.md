# Nachbarschftshilfe - WebApp - Django Bootstrap

Dies ist eine WebApp zur dezentralen Koordinierung von Einkaufs- und Nachbarschaftshilfen über ein online Schwarzes Brett.
Gesuche können aufgegeben werden und angemeldeten Nutzern ist es möglich Aufträge anzunehmen. Nach der Annahme eines Auftrags 
sind die Kontaktdaten der AuftraggeberIn einsehbar.

Dieses Projekt ist während der Corona-Krise 2020 enststanden und wurde in 2 Städten eingesetzt.
Beobachtungen: Vor allem um die Zielgruppe (Senioren) zu erreichen, ist es notwendig auch eine Telefon-Hotline anzubieten.

## Funktionen - Anwendung des Nutzers

- Navigations-Leiste:
    - Anmeldung (oben links)
    - Menu (oben rechts) zur Navigation zwischen verschiedenen Funktionen/Seiten

- Startseite: 
    - Registrierung als HelferIn und HilfsempfängerIn möglich.
    - Begrüßungstext
    - Informationen über Hilfsangebot
    
- Scharzes Brett:
    - Auswahl: Ort und Status der Hilfsgesuche
    - Hilfsgesuche: Karten mit Nachricht der AuftraggeberIn, Einkaufsliste, Budget und Ort

- Schwarzes Brett (nach Anmeldung):
    - Anklicken eines Auftrags und Annahme des Auftrags möglich
    
- Mein Bereicht (nach Anmeldung):
    - Begrüßung des Nutzers
    - Angemeldet als HelferIin:
        - Wechseln zu Schwarzem Brett möglich
        - Übersicht über angenommene Aufträge einsehen (mit Kontaktdaten!)
    - Angemeldet als HilfsempfängerIn:
        - Auftrag aufgeben möglich
        
- Auftrag aufgeben (nach Anmeldung als HilfsempfängerIn):
    - Formular (Desktop: links, Mobil: oben) ausfüllen und abschicken (Listen auf Schwarzem Brett)
    - Aufgegebene Aufträge (Desktop: rechts, Mobil: unten):
        - Abschließen (falls angenommen)
        - Widerrufen (falls noch nicht angenommen)