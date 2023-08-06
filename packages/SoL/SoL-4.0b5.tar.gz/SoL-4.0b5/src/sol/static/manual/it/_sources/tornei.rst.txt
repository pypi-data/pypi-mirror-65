.. -*- coding: utf-8 -*-
.. :Project:   SoL
.. :Created:   mer 25 dic 2013 11:13:43 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2013, 2014, 2015, 2016, 2018, 2019, 2020 Lele Gaifax
..

.. _gestione tornei:

Gestione tornei
---------------

.. index::
   pair: Gestione; Tornei

Il *torneo* è chiaramente l'elemento primario di tutto il sistema, tutto quanto verte a
permettere di gestire in maniera facile e veloce questi eventi.

La finestra di gestione dei tornei di default **non** mostra i tornei *futuri*: per vederli,
:ref:`annulla il filtro <filtri>` applicato al campo :guilabel:`data`.

.. contents::


Voci del menu
~~~~~~~~~~~~~

Oltre alle :ref:`azioni standard <pulsanti-standard>` il menu contiene queste voci:

.. figure:: tornei.png
   :figclass: float-right

   Gestione tornei

:guilabel:`Dettagli`
  Mostra la :ref:`gestione <gestione torneo>` del torneo selezionato.

:guilabel:`Concorrenti`
  Consente di :ref:`correggere i concorrenti <correzione concorrenti>` di un torneo già svolto.

:guilabel:`Rigioca di nuovo`
  Consente di *duplicare* un torneo: particolarmente utile nei tornei di doppio o a squadre: in
  pratica replica il torneo sul giorno corrente, con tutti i suoi concorrenti; assicurati di
  aggiornarne la descrizione ed eventualmente la data dell'evento!

:guilabel:`Scarica`
  Permette di scaricare i dati del torneo.

:guilabel:`Assegna`
  Assegna la responsabilità dei tornei selezionati: è possibile selezionare uno o più
  tornei tenendo premuto il tasto :kbd:`Ctrl` ed estendere la selezione premendo il tasto
  :kbd:`Shift`


.. _inserimento e modifica torneo:

Inserimento e modifica
~~~~~~~~~~~~~~~~~~~~~~

.. index::
   pair: Inserimento e modifica; Tornei

Data e descrizione
++++++++++++++++++

Ogni torneo ha una :guilabel:`data` e una :guilabel:`descrizione` dell'evento e non ci possono
essere due distinti tornei nella stessa data associati al medesimo campionato.

Posto
+++++

Il :guilabel:`posto` è opzionale ed è puramente descrittivo.

Campionato
++++++++++

Un torneo appartiene a un particolare :guilabel:`campionato`. Il selettore ti permette di
sceglierne uno tra quelli correntemente attivi (cioè **non** :ref:`conclusi <campionato
concluso>`) **e** almeno una delle seguenti condizioni è valida:

a. ne sei il responsabile (quindi probabilmente creati da te)
b. sono legati ad un club che ti appartiene *oppure* a cui sei stato :ref:`associato <gestione
   associazione club-utenti>`.

Ospitato da
+++++++++++

Può accadere che un torneo sia ospitato da un club diverso da quello che organizza il
campionato: in questi casi è possibile selezionare il club ospitante, che apparirà su alcune
stampe.

Durata e preavviso
++++++++++++++++++

:guilabel:`Durata` e :guilabel:`preavviso` si riferiscono alla durata di un singolo turno e
sono espressi in *minuti*. Vengono usati per visualizzare il :ref:`conto alla rovescia
<countdown>`.

.. _valutazione torneo:

Valutazione
+++++++++++

Un torneo può essere associato a una particolare :guilabel:`valutazione`: in questo caso il
primo turno verrà generato tenendo conto del valore di ciascun giocatore invece che usando un
ordine casuale.

Può anche essere impostata sul :ref:`campionato <valutazione campionato>`, in modo tale che
verrà inizializzata automaticamente alla creazione di ogni nuovo torneo associato.

.. _abbinamenti:

Abbinamenti
+++++++++++

Il :guilabel:`metodo abbinamenti` determina come verranno create le coppie di avversari ad
ogni nuovo turno:

``Tutti contro tutti``
  l'algoritmo ``all`` genera tutte le possibili combinazioni, senza un particolare ordine;

``Classifica``
  l'algoritmo ``serial`` cercherà di abbinare un concorrente con uno di quelli che lo seguono
  nella classifica corrente, ad esempio il primo col secondo, il terzo con il quarto e così
  via;

``Classifica incrociata``
  per ritardare per quanto possibile gli incontri tra le teste di serie, questo metodo
  (``dazed``) usa un sistema più elaborato: prende i concorrenti a pari punti di quello che sta
  esaminando e cerca di abbinare il primo con quello che sta a metà di questa serie, il
  secondo con quello a metà+1, e così via;

.. attention:: Con meno di otto concorrenti gli algoritmi ``serial`` e ``dazed`` non possono
               garantire la generazione di tutti i possibili incontri. Dovesse accadere, SoL
               suggerirà di passare al metodo ``all`` per generare le partite rimanenti.

               In generale, con un numero di concorrenti così basso, consiglio di usare il
               metodo ``all`` fin dall'inizio del torneo.

``Classifica sfalsata``
  il metodo ``staggered`` è equivalente al precedente quando il numero di concorrenti a pari
  merito non supera i 50, superato il quale anziché abbinare il primo con quello a metà della
  serie viene usato un scostamento massimo di 25 a prescindere dal numero: si otterrà quindi il
  primo con il ventiseiesimo, il secondo con il ventisettesimo e così via.

Ritarda abbinamenti teste di serie
++++++++++++++++++++++++++++++++++

Il campo :guilabel:`ritarda abbinamenti teste di serie`, significativo solo quando il torneo è
associato a una valutazione, determina per quanti turni viene data priorità alla quotazione
Glicko di ciascun concorrente rispetto alla *differenza pedine* nell'ordinamento utilizzato per
effettuare gli abbinamenti.

.. note::

   SoL utilizza cinque parametri per stabilire l'ordinamento della classifica:

   1. punteggio
   2. bucholz
   3. differenza score
   4. score totale
   5. quotazione Glicko

   Prima di giocare il primo turno i primi 4 valori sono tutti nulli, quindi solo il
   quinto è determinante. All'inizio del secondo turno tutti i vincitori hanno lo stesso
   punteggio e lo stesso bucholz, per cui è la differenza pedine ad essere determinante.

   Dal punto di vista della generazione dei turni, per la bellezza del gioco è
   generalmente desiderabile ritardare quanto più possibile gli scontri tra le *teste di
   serie*: a tal fine è sufficiente dare una priorità maggiore alla quotazione Glicko,
   spostandola al terzo posto, dopo il bucholz e prima della differenza score.

   Il valore assegnato a questo campo controlla appunto per quanti turni debba venire
   utilizzato questo diverso criterio di ordinamento: il valore di default è ``1``,
   indica che si desidera usarlo al termine del primo turno per la generazione del
   secondo; un valore ``0`` invece inibisce questo ritardo e quindi solo il primo turno è
   determinato dalla quotazione Glicko, dal secondo in poi diventa di fatto
   ininfluente. Valori maggiori di ``1`` hanno un impatto via via meno significativo, dal
   momento che dal terzo turno in avanti il punteggio e i bucholz diventano comunque
   predominanti.

Ritarda abbinamenti connazionali
++++++++++++++++++++++++++++++++

Il campo :guilabel:`ritarda abbinamenti connazionali` indica se l'algoritmo di generazione
degli abbinamenti dovrà tentare di ritardare per quanto possibile gli incontri tra giocatori
*con il medesimo punteggio* appartenenti alla stessa nazione.

Ad esempio se il campo è marcato **e** il metodo di abbinamento è diverso da *"tutti contro
tutti"*, quando in base alla classifica attuale ci fossero 10 giocatori a pari punti, i primi
tre italiani e i rimanenti di una nazionalità diversa, il sistema anziché tentare un
abbinamento tra il primo e il secondo oppure tra il primo e il terzo, cercherà prima di far
giocare il primo con il quarto e poi col quinto, prendendo in considerazione il secondo e il
terzo solo se necessario.

Score fantasma
++++++++++++++

Lo :guilabel:`score fantasma` è il punteggio assegnato al giocatore negli incontri con il
*fantasma*, quando il numero di concorrenti è dispari. Per convenzione questi incontri
assegnano uno score pari a 25 al giocatore ma ci possono essere casi in cui sia preferibile un
punteggio diverso, ad esempio quando il numero di concorrenti è molto basso e il vincere 25—0
darebbe un vantaggio inappropriato ai giocatori più deboli.

Responsabile
++++++++++++

Il :guilabel:`responsabile` generalmente indica l'utente che ha inserito quel particolare
torneo: i dati del torneo potranno essere modificati solo da lui (oltre che
dall'*amministratore* del sistema.).

.. _campo finali:

Finali
++++++

Il campo :guilabel:`finali` stabilisce quante finali verranno giocate. Può essere lasciato in
bianco oppure può essere un numero tra ``0`` e ``2`` compresi: nel primo caso le finali
verranno gestite *manualmente*, nel senso che SoL non genererà gli incontri finali ma il loro
esito potrà essere applicato correggendo i premi finali. Il valore ``0`` indica che non ci sarà
alcuna finale, ``1`` indica che SoL genererà un singolo match finale per il primo e secondo
posto, mentre con il valore ``2`` verranno generati due incontri, uno per il primo e secondo
posto e l'altro per il terzo e quarto posto.

Tipo di finale
++++++++++++++

Il :guilabel:`Tipo di finale` determina la modalità di svolgimento delle finali:

``Match singolo``
  il tipo ``single`` creerà un singolo round, con un match tra il primo e secondo concorrente
  e, se :guilabel:`finali` è impostato a ``2``, un altro tra il terzo e il quarto concorrente;

``Al meglio di tre match``
  il tipo ``bestof3`` creerà al massimo tre turni e la finale sarà vinta dal concorrente che ne
  vince almeno due.

Non appena i risultati di tutti i turni sono stati inseriti, l'assegnazione dei *premi finali*
avviene automaticamente.

.. _ritiri:

Ritiri
++++++

Il campo :guilabel:`ritiri` consente di scegliere un meccanismo diverso per calcolare il valore
``bucholz`` quando ci sono concorrenti `ritirati`. Normalmente quel valore viene calcolato come
somma dei ``punti`` degli avversari incontrati da un determinato contendente, misurando in
pratica la loro forza. Quando uno (o più) di questi avversari smette di giocare, il loro
punteggio rimane costante e quindi non contribuisce alla classifica dei concorrenti che ha
incontrato. Nei tornei altamente competitivi questo può essere visto come una penalità, quindi
abbiamo cercato di immaginare un meccanismo per mitigare l'effetto. Le opzioni sono:

``none``
  il metodo classico, nessun aggiustamento: il valore ``bucholz`` è la semplice somma dei punti
  degli avversari incontrati

``trend``
  calcola il *punteggio medio* del giocatore ritirato (escludendo eventuali incontri con il
  *fantasma*) e assegna un *bonus extra* ai suoi avversari, in modo che il loro ``bucholz``
  viene *aumentato artificialmente* di un valore uguale a quella media moltiplicata per il
  numero di turni; in altre parole, è *come se* il giocatore ritirato avesse continuato a
  giocare allo stesso livello

``trend70``
  simile alla precedente, ma viene considerato il 70% del punteggio medio

.. warning:: Si tratta di approccio **sperimentale**, comprendi bene le implicazioni prima di
             usarlo!

.. toctree::
   :maxdepth: 2

   torneo
   concorrenti
