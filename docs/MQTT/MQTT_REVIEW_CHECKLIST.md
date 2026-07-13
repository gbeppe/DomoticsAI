# MQTT Classification Review Checklist

## Da verificare manualmente

- [ ] Topic classificati come `Altro / da classificare`
- [ ] Topic costruiti dinamicamente nei Function node
- [ ] Payload reali e relativo tipo
- [ ] Unità di misura
- [ ] Semantica del segno per potenze rete/batteria
- [ ] Retain effettivo sul broker
- [ ] QoS realmente necessario
- [ ] Topic duplicati tra i due broker
- [ ] Topic dismessi ma ancora presenti nei flow
- [ ] Topic relativi al vecchio `Android APP Bridge` disabilitato
- [ ] Topic delle telecamere/PTZ
- [ ] Comandi che richiedono conferma o limiti di sicurezza
