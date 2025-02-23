# Esercizi di riconoscimento rocce

L'esercizio consiste nel riconoscere una roccia data la sua foto e senza altre informazioni. 

Nella cartella [photos](./photos/) si trovano le foto dei "campioni macroscopici" tratti dall'[Atlante di petrografia del Dipartimento di Scienze della Terra dell'Università di Torino](https://www.atlantepetro.unito.it/page-1d41d.html?).

Nell'Atlante i nomi dei file suggeriscono il tipo di roccia (ignea, sedimentaria, metamorfica); per non avere questo suggerimento i nomi dei file sono stati cambiati in nomi di fantasia come per esempio "Vaderite blu giurassica".

Per svolgere l'esercizio:

1) scegliere una immagine a caso dalla cartella, per esempio la "Vaderite blu giurassica" ![photos](./photos/Vaderite_Blu_Giurassica.gif).

2) applicare i metodi di riconoscimento e giungere ad un nome. Nell'esempio si ha una roccia olocristallina con indice di colore M pari circa al 50% (nello stimare M ho escluso il cristallo più grande indicato dalla punta della matita); i minerali chiari hanno aspetto bianco lattiginoso quindi mi suggeriscono una predominanza di plagioclasi rispetto ai K-feldspati, stimo quindi P/(A+P) > 65%; dalla foto non riesco a vedere con sicurezza quarzo quindi stimo Q < 20%. Dal diagramma QAP per la classificazione speditiva sul campo si tratta quindi di Dioritoide o Gabbroide.

3) trovare la corrispondenza tra il nome di fantasia ed il nome originale usando la [tabella allegata](corrispondenza_immagini.csv).

4)
