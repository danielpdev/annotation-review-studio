# Pregătire pentru interviu — Annotation Review Studio

Roluri țintă: AI Data Tools / Full-stack Python.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: Two distinct annotators label an example. An independent reviewer resolves the label with a reason. Export includes only adjudicated examples; later review decisions append to history.

## Cinci întrebări

1. Ce înseamnă două adnotări independente?
2. Cum măsori agreement?
3. De ce adjudication are motiv?
4. Cum previi data leakage?
5. Cum păstrezi versiunile datasetului?

## Exercițiu înainte de a aplica

Add authenticated roles, blinded task assignment, sampling and inter-annotator agreement statistics.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
