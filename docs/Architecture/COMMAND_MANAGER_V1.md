# Command Manager v1

```text
created → validated → queued → sent → waiting_confirmation
                                      ├─ simulated
                                      ├─ confirmed
                                      ├─ rejected
                                      ├─ timeout
                                      └─ failed
```

Endpoint:

```text
POST /api/v1/commands
GET  /api/v1/commands
GET  /api/v1/commands/{command_id}
```

Prima implementazione: dominio `lights`, modalità `simulation`.
