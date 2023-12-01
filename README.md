# Análise léxica do Mini-Pascal

## Integrantes do grupo:

- Artur Freire dos Santos
- Gabriel Gonçales Lopes
- Gabriel Teodoro Suzano
- Gustavo Medeiros Madeira
- Lucas Silva dos Anjos
- Luís Gustavo Oliveira Machado
- Vinícius Pereira Freire Costa

## Sumário

1. Tokenizador
2. Parse
    * 2.1. Analisador sintático descendente recursivo
    * 2.2. Tabela de símbolos
    * 2.3. Modificações gramáticais
    * 2.4. Erros sintáticos
    * 2.5. Ressalvas
3. Conclusão

## 1 - Tokenizador
No processo de tokenização é onde ocorre a conversão dos lexemas (símbolos) para tokens. Para que possa ser feito a classificação correta dos tokens, os lexemas são formados a partir do agrupamento de cadeias de caracteres não espaçados e conjuntos específicos contidos na lista de símbolos especiais e palavras reservadas da gramática léxica do Mini-Pascal. Após identificados os lexemas, estes serão classificados pelos os seus respectivos tipos, sendo eles:

- **LITERAL_STRING:** Constante de caracteres;
- **Palavras reservadas:** As palavras reservadas da linguagem, e as palavras true e false são convertidas no token BOOLEAN;
- **IDENT:** Identificadores;
- **LITERAL_INT:** Constante de um número inteiro;
- **Símbolos especiais compostos:** São símbolos especiais que são compostos por dois caracteres;
- **Símbolos especiais:** São símbolos especiais que são compostos por um caracter;
- **Operadores aritméticos:** Símbolos usados para operações aritméticas;
- **Operadores lógicos:** Símbolos usados em condicionais.

> Todo e qualquer lexema que não for identificado pela a gramática léxica do Mini-Pascal será considerado um erro de símbolo desconhecido.

## 2 - Parser
Para que possa ser feito a análise da estrutura da sentença foi usado um parser top-down que usa o esquema de derivação do não-terminal mais à esquerda, de modo que a derivação inicia a partir do símbolo inicial e segue de cima para baixo.

### 2.1 - Analisador sintático descendente recursivo
Foi utilizado o **"Parser Descendente Recursivo"** (parser sem backtracking e puramente determinístico) que utiliza de funções recursivas onde cada uma implementa uma regra da grámatica. A escolha deste parser foi dada sua fácil implementação, entendimento e melhor desempenho do que uma alternativa que use backtracking.

### 2.2 - Tabela de símbolos
A tabela de símbolos conta com as seguintes colunas:
- **Linha:** A linha em que se encontra;
- **Coluna:** A coluna em que se encontra;
- **ID:** Caso seja um identificador terá um ID para que possa ser diferenciado entre outros identificadores;
- **Tipo:** O seu tipo de dado, que podem ser: 
    - Para os tipos simples: 
        - **Integer:** Número inteiro;
        - **Char:** Caracter;
        - **Boolean:** Booleano (True, False);
    - Para os tipos de array: 
        - **Array Integer:** Array de números inteiros;
        - **Array Char:** Array de caracteres;
        - **Array Boolean:** Array de booleanos;
- **Valor:** O valor que foi associado ao identificador;
- **Tamanho do array:** O tamanho do array;

### 2.3 - Modificações gramáticais
Tomamos a liberdade de adicionar pequenas mudanças nas regras gramáticais do mini-pascal para um melhor aproveitamento. São elas:
- A regra `< write statement >` na grámatica original aceita apenas identificadores o que impossibilita a inserção direta de uma constante de caracteres ou uma constante inteira (como uma mensagem ou um código numérico). Para melhorar a flexibilidade desta regra, estas constantes poderão ser utilizadas no lugar do identificador.
- As regras `< block >` e `< statement part >` foram removidas e passaram a ser produções da regra `< program >` pois se comportavam como "produções unitárias" e foram simplificadas.
- A regra `< sign >` foi removida pois pode ser substituída por `< adding operator >`.
- As regras `< array variable >` e `< entire variable >` foram removidas e passaram a ser produções da regra `< variable identifier >` pois se comportavam como "produções unitárias" e foram simplificadas.
- A regra `< type identifier >` foi removida por ser um símbolo inacessível, afinal, nenhuma outra regra a deriva.
- Foram adicionados regras sintáticas para a declaração das estruturas de function e procedure, além da chamada das mesmas.
- Foi alterada a regra < factor > para que pudesse aceitar chamadas de functions e procedures como expressions em assign statements.
- A declaração de uma constante de char é feita somente entre aspas simples, não diferenciando entre um char e uma string.

### 2.4 - Erros sintáticos
Abaixo está listado todos os erros sintáticos implementados:
|Número do erro |Descrição do erro                                          |
|---------------|-----------------------------------------------------------|
|0              |Caso não encontre o símbolo, apenas ignore                 |
|1              |Falta a palvra reservada program                           |
|2              |Falta um identificador                                     |
|3              |Falta um ;                                                 |
|4              |Falta a palvra reservada var                               |
|5              |Falta por : e um identificador                             |
|6              |Não é do tipo simple_type ou array_type                    |
|7              |Falta a palvra reservada array                             |
|8              |Não abriu [                                                |
|9              |Não é do tipo LITERAL_INT                                  |
|10             |Faltou usar ..                                             |
|11             |Faltou fechar ]                                            |
|12             |Falta a palvra reservada of                                |
|13             |Não é do tipo simple_type                                  |
|14             |Falta a palvra reservada begin                             |
|15             |Falta a palvra reservada read                              |
|16             |Não abriu (                                                |
|17             |Faltou fazer uma declaração de variável                    |
|18             |Não fechou )                                               |
|19             |Falta a palvra reservada write                             |
|20             |Faltou o símbolo de atribuição :=                          |
|21             |Não é do tipo literal_int, literal_string ou usou ( ou not |
|22             |Falta a palavra reservada end                              |
|23             |Falta a palavra reservada if                               |
|24             |Falta a palavra reservada then                             |
|25             |Falta a palavra reservada while                            |
|26             |Falta a palavra reservada do                               |
|27             |Faltou o .                                                 |
|28             |Símbolo desconhecido                                       |
|29             |Falta ser feito uma expressão                              |
|30             |Falta a palavra reservada procedure                        |
|31             |Falta a palavra reservada function                         |
|32             |Falta de armazenamento de memória                          |

### 2.5 - Ressalvas
Por ser um analisador léxico, certos elementos não serão garantidos, como atribuições, tipos e etc, como é melhor detalhado abaixo: 
- É possível fazer atribuições à variáveis no meio do código sem ter que declará-la antes, tornando-a uma variável não tipada.
- Caso o valor de uma variável seja uma expressão, a informação que aparecerá na tabela é a própria expressão e não o seu resultado. No exemplo `y := x + 2` o valor do identificador `y` será igual a expressão `x + 2` e não ao resultado da operação mesmo que já tenha sido declarado um valor inteiro para `x`.
- Caso uma mesma variável seja declarada múltiplas vezes com diferentes tipos apenas o último tipo que foi declarado será válido para ser exibido na tabela de símbolos. O mesmo vale para o tamanho de `array`. Neste caso não é possível garantir o tipo de valor que será atríbuido à variável.
- As expressões tanto aritméticas como lógicas só podem ser feitas por dois elementos.

## 3 - Conclusão
Pode-se concluir que a tokenização é fundamental no desenvolvimento de um Parser. A escolha do Parser Descendente Recursivo se mostrou satisfatória para resolver o problema de se compilar um código escrito em mini-pascal dado que esta linguaguem não é ambígua.
