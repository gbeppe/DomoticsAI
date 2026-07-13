# AI Climate — Regression Test Plan Draft

## Obiettivo

Prima di qualsiasi refactoring, registrare input e output per poter confrontare il comportamento attuale con una futura implementazione modulare.

## Scenari minimi

### Inverno giorno

- temperatura sotto 19 °C;
- surplus FV sufficiente;
- lockout OFF scaduto;
- atteso: `HEAT_DIURNO`.

### Inverno notte

- temperatura sotto 17 °C;
- SOC sopra soglia dinamica;
- atteso: `HEAT_SICUREZZA_NOTTE`.

### Estate giorno

- Humidex sopra target;
- SOC e surplus sufficienti;
- atteso: `COOLING_ON`.

### Estate grace mode away

- fascia grace attiva;
- Humidex sotto emergenza;
- atteso: climatizzatore spento.

### Estate grace mode solar-only

- surplus sotto soglia;
- atteso: nessuna accensione.

### Estate notte

- Humidex sopra target + isteresi;
- SOC sufficiente;
- pausa notturna scaduta;
- atteso: `NIGHT_DRY`.

### Deficit transitorio

- deficit più breve della tolleranza;
- atteso: nessuno spegnimento.

### Deficit persistente

- deficit oltre la tolleranza;
- atteso: richiesta spegnimento dopo tempo minimo ON.

### Falso OFF

- stato logico OFF;
- assorbimento AC reale sopra soglia;
- atteso: reinvio comando OFF.

### Falso ON

- stato logico ON;
- assorbimento reale insufficiente;
- atteso: tentativo di riavvio, massimo tre tentativi.

### AI disabilitata

- atteso: OFF, VMC livello base, stato persistente aggiornato.

## Dati da registrare

- timestamp;
- tutti gli input;
- configurazione;
- stato precedente;
- stato successivo;
- comando IR;
- velocità VMC;
- motivazione;
- output completo;
- warning/errori.
