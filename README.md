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

 * 1 - Tokenizador
 * 2 - Parse
    * 2.1 - Analisador sintático descendente recursivo
    * 2.2 - Parâmetros do token
    * 2.3 - Tabela de símbolos
    * 2.4 - Modificações gramáticais
    * 2.5 - Erros sintáticos
    * 2.6 - Ressalvas
* 3 - Conclusão

## 1 - Tokenizador
No processo de tokenização é onde ocorre a conversão dos lexemas (símbolos) para tokens. Para que possa ser feito a classificação correta dos tokens, os lexemas são formados apartir da filtragem de cadeias de caracteres não espaçados, e conjuntos específicos que sejam similares aos símbolos especiais e palavras reservadas especificadas pela gramática léxica do Mini-Pascal, que após isso todos os símbolos que são reconhecidos pela mesma, incluindo identificadores e constantes, serão classificados pelos os seus tipos respectivos, sendo eles:

- **LITERAL_STRING:** Constante de caracteres;
- **Palavras reservadas:** As palavras reservadas da linguagem, e as palavras true e false são convertidas no token BOOLEAN;
- **IDENT:** Identificadores;
- **LITERAL_INT:** Constante de um número inteiro;
- **Símbolos especiais compostos:** São símbolos especiais que são compostos por dois caracteres;
- **Símbolos especiais:** São símbolos especiais que são compostos por um caracter;
- **Operadores aritméticos:** Símbolos usados para operações aritméticas;
- **Operadores lógicos:** Símbolos usados em condicionais.

> Para todo e qualquer lexema que não seja identificado pela a gramática léxica do Mini-Pascal será considerado um erro de símbolo desconhecido.

## 2 - Parser
Para que possa ser feito a análise da estrutura da sentança foi usado um parser top-down, que se usa de um esquema de derivação de um não terminal mais á esquerda, sempre iniciando a partir do símbolo inicial, e seguindo de cima para baixo.

### 2.1 - Analisador sintático descendente recursivo
Foi utilizado o Parser Descendente Recursivo, que é um parser sem backtracking, ou seja é puramente determinístico, utilizando-se de funções recursivas, onde cada uma implementa uma regra da grámatica. Ela foi escolhida pela sua fácil implementação, além de possuir um desempenho melhor do que uma alternativa que use backtracking.

### 2.2 - Parâmetros do token
Cada um dos tokens possui parâmetros que servem como as suas informações, que serão mostradas na tabela de símbolos. Os parâmetros de tokens são:
- **Linha:** A linha em que se encontra.;
- **Coluna:** A coluna em que se encontra;
- **ID:** Caso seja um identificador terá um ID para que possa ser diferenciado entre outros identificadores.
- **Tipo:** O seu tipo de dado, que podem ser: 
    - Para os tipos simples: 
        - **Integer:** Número inteiro;
        - **Char:** Caracter;
        - **Boolean:** Booleano (True, False).
    - Para os tipos de array: 
        - **Array Integer:** Array de números inteiros;
        - **Array Char:** Array de caracteres;
        - **Array Boolean:** Array de booleanos.
- **Valor:** O valor que foi associado ao identificador;
- **Tamanho do array:** O tamanho do array. 

### 2.3 Tabela de símbolos
A tabela de símbolos é formado pelas as informações básicas do token, além de seus parâmetros. As informações básicas de um token são:
- **Lexema:** O lexema do símbolo;
- **Token:** O token do lexema.
> Os parâmetros do token são explicados na seção anterior.

### 2.4 - Modificações gramáticais
Pela a grámatica do Mini-Pascal dada ter certas limitações, portanto tivemos a liberdade de mudar certas regras gramáticais, além reduções da mesma por termos considerado ser produções unitárias, e da remoção de uma regra por ser um símbolo inacessível. Essas mudanças estão melhor detalhadas abaixo:
- Na regra `< write statement >` na grámatica original apenas aceita identificadores, impossibilitando a inserção direta de uma constante de caracteres ou inteira, como uma mensagem ou um número, portanto para que possa ter mais flexibilidade decidimos mudar para que possam ser aceitos além de somente os identificadores.
- As regras `< block >` e `< statement part >`, foram removidas pois eram apenas produções unitárias produzindo um único não terminal cada. Suas respectivas produções passaram a ser da regra `< program >`.
- A regra `< sign >`, foi removida pois possui as mesmas produções que `< adding operator >` com excessão da produção vazia, portanto essa produção foi a atribuida ao `< adding operator >`.
- As regras `< array variable >` e `< entire variable >`, foram removidas pois eram apenas produções unitárias produzindo um único não terminal cada. Suas respectivas produções passaram a ser da regra `< variable identifier >`.
- A regra `< type identifier >` foi removida por ser um símbolo inacessível, pois nenhuma outra regra a deriva.

### 2.5 - Erros sintáticos
Abaixo está listado todos os erros sintáticos implementados:
|Número do erro|Descrição do erro|
|---|--------|
|1|Falta a palvra reservada program|
|2|Falta um identificador|
|3|Falta um ;|
|4|Falta a palvra reservada var|
|5|Falta por : e um identificador|
|6|Não é do tipo simple_type ou array_type|
|7|Falta a palvra reservada array|
|8|Não abriu [|
|9|Não é do tipo LITERAL_INT|
|10|Faltou usar ..|
|11|Faltou fechar ]|
|12|Falta a palvra reservada of|
|13|Não é do tipo simple_type|
|14|Falta a palvra reservada begin|
|15|Falta a palvra reservada read|
|16|Não abriu (|
|17|Faltou fazer uma declaração de variável|
|18|Não fechou )|
|19|Falta a palvra reservada write|
|20|Faltou o símbolo de atribuição :=|
|21|Não é do tipo literal_int, literal_string ou usou ( ou not|
|22|Falta a palvra reservada end|
|23|Falta a palvra reservada if|
|24|Falta a palvra reservada then|
|25|Falta a palvra reservada while|
|26|Falta a palvra reservada do|
|27|Faltou o .|
|28|Símbolo desconhecido|
|29|Falta ser feito uma expressão|

### 2.6 - Ressalvas
Por ser um analisador léxico, certos elementos não serão garantidos, como atribuições, tipos e etc, como é melhor detalhado abaixo: 
- É possível fazer atribuições a variáveis no meio do código sem ter que declará-la antes, o que fará com que não apereçará o seu tipo específico, nem tamanho de `array` caso seja um na tabela de símbolos;
- Os valores atreladas as variáveis só aparecerá na tabela de símbolos daquelas que estão á esquerda de uma atribuição, portanto caso seja uma expressão, o valor será apenas a expressão em si, e não seu significado, por exemplo `x := x + 2`, o valor do identificador `x` será igual a expressão `x + 2`, mesmo que já tenha sido declarado um valor inteiro para `x` a operação aritemética não ocorrerá, além disso, o segundo `x` na expressão a direita do símbolo de atribuição na tabela de símbolos não possuirá um valor, pois vai ser considerado que não lhe foi atribuído um, mesmo que já o tenha sido antes, para que ao longo das atribuições no código possa ser mostrado o seu valor sendo alterado, caso ocorra;
- Caso uma mesma variável seja declarada múltiplas vezes com diferentes tipos, apenas será contabilizado o último tipo que foi declarado, para que possa ser mostrado na tabela de simbolos, mas nas declarações não é garatindo o tipo de valor que lhe será atríbuido, o mesmo vale para o tamanho de `array`.
- Só foram retiradas procuções que produzam apenas um elemento, que seja um não terminal para que as regras ficassem mais enxutas.

## 3 - Conclusão
Pode-se concluir que, para que possa ser feito de forma adequada a análise do parser, a tokenização é fundamental. Além de é claro a escolha da melhor técnica de parser, que seja necessária para a implementação da grámatica em questão, e que tenha o melhor desempenho possível na compilação, e que seja mais compatível com a mesma, como por exemplo parsers sem backtracking lidam melhor com gramáticas não ambíguas e determinísticas, mas aquelas que possuem ambiguidades, e portanto não determinísticas, precisam de um parser com maior flexibilidade como os com backtracking.
