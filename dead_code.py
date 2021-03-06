import random


__author__ = "Ceoletta Valentina, Zanotti Mattia, Zenari Nicolo"
__version__ = '1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"


candidate_lines = ['while', 'for', 'def', 'if ']

def start(source_path):
    # apro il file da offuscare
    source = open(source_path, "r")
    output = open('./result/output.py', 'w')

    lines = source.readlines()

    #indica se le variabili del codice morto sono state inizializzate
    dead_code_variables_is_inizialized = False

    # variabile che indica se sono in un blocco di commenti
    comment = False

    value = ('\t', ' ', '', '\n')

    for line in lines:

        # Verifico se sto entrando in un blocco di commento
        if '"""' in line or "'''" in line:
            # se il blocco non inizia e termina sulla stessa riga, allora imposto comment=True per indicare che sono entrato nel blocco,
            # la variabile comment sarà riportata a False quando verrà trovata la fine del blocco (ovvero la stringa '""""')
            if line.count('"""') or line.count("'''")!= 2:
                comment = not comment
        else:
            # Se non sono in un blocco di commento
            if comment == False:

                # verifico se ci sono commenti sulla riga, e in tal caso prendo solo la parte di stringa che lo precede
                if '#' in line:
                    line = line[:line.find('#')]

                # verifico che line non sia vuota
                if line != '':
                    # verifico che line non inizi con spazi o tabulazioni (ovvero non sia nello scope di un costrutto)
                    if (not line[0] == ' ') and (not line[0] == '\t') and is_candidate(line):

                        #se le variabili del codice morto non sono ancora state inizializzate le inizializzo
                        if dead_code_variables_is_inizialized == False:
                            inizialize_dead_code_variables(output) 
                            #indico che le variabili del dead_code sono state inizializzate
                            dead_code_variables_is_inizialized = True

                        # inserisco il codice morto
                        insert_dead_code(output)
                        output.write('\n' + line)

                    # se sono nello scope di un costrutto oppure line non è una riga candidata
                    else:

                        # verifico che line non sia fatta solo da spazi e tabulazioni
                        if any(c not in value for c in line):
                            # scrivo la line in output
                            output.write(line)

    insert_dead_code(output)

    output.close()
    source.close()

# funzione che aggiunge codice morto
def insert_dead_code(output):
    # seglie a random un file tra dead_code_.py1,...,dead_code_21.py
    ran = random.randint(1, 21)
    dead_code = open('./dead_code/dead_code_' + str(ran) + '.py', 'r')

    # inserisce il file dead_code_x.py nel file output.py
    for line in dead_code.readlines():
        output.write(line)

    dead_code.close()

def inizialize_dead_code_variables(output):

    dead_code_variables = open('./dead_code/dead_code_variables.py', 'r')
    # inizializzo le variabili del codice morto
    for line in dead_code_variables:
        output.write(line)
    output.write('\n')

# funzione che veriifica se la riga è una riga candidata
def is_candidate(source_string):
    for line in candidate_lines:
        if line in source_string:
            return True

    return False
