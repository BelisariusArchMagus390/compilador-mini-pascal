# Integrantes do grupo:

# Artur Freire dos Santos
# Gabriel Gonçales Lopes
# Gabriel Teodoro Suzano
# Gustavo Medeiros Madeira
# Lucas Silva dos Anjos
# Luís Gustavo Oliveira Machado
# Vinícius Pereira Freire Costa

import os
from parser_model import Parse

erro = False

# Menu de exibição de opções
print("1 - Arquivo (apenas arquivos de texto)")
print("2 - Exemplo pré-feito")
print("3 - Cancelar")
opcao = input("\nOpção: ")

match opcao:
    # Opção 1: Escolher um arquivo de texto onde possa estar o código para ser
    # feito sua análise léxica
    case "1":
        # Para executar em Windows
        caminho = os.path.dirname(os.path.abspath(__file__))

        # Para executar em Linux
        # caminho = os.getcwd()
        nome_arquivo = input(
            "Digite o nome do arquivo (o arquivo precisa estar na pasta raiz): "
        )

        # Para executar em Windows
        caminho_nome = os.path.join(caminho, nome_arquivo)

        # Para executar em Linux
        # caminho_nome = caminho+"/"+nome_arquivo

        if nome_arquivo.endswith(".txt"):
            try:
                with open(caminho_nome) as arquivo:
                    codigo = arquivo.readlines()
                    codigo = " ".join(codigo)
                    codigo = codigo + " "
            except FileNotFoundError:
                err_msg = "O arquivo " + nome_arquivo + " não existe."
                print(err_msg)
                erro = True
        else:
            err_msg = "O arquivo " + nome_arquivo + " não é do tipo texto."
            print(err_msg)
            erro = True

    # Opção 2: É feito a análise léxica de um exemplo pré-feito
    case "2":
        codigo = """program Exemplo;

var
  i: integer;
  c: char;
  b, d: boolean;
  arrI: array[1..5] of integer;
  arrC: array[1..5] of char;
  arrB: array[1..5] of boolean;

begin
  i := 10;
  i := 11;
  c := "A";
  b := true;
  d := false;
  
  write("Digite");
  read(arrInt[1]);
  
  write("Digite");
  read(arrChar[1]);
  
  write("Digite");
  read(arrBool[1]);

  i := i - 1;

  arrInt[2] := arrInt[1] + 5;
  arrInt[3] := arrInt[1] - 2;
  arrInt[4] := arrInt[1] * 3;
  arrInt[5] := arrInt[1] div 2;
  
  while i >= 0 do
    if (i = 5) then
      write("LOL1")
    else
      write("LOL2")
end."""
        print("\nCÓDIGO PRÉ-FEITO: \n")
        print(codigo)
    # Opção 3: Interrompe o programa
    case "3":
        erro = True
    case _:
        print("Opção indisponível!")
        erro = True

if erro == False:
    p = Parse(codigo, "parse")
    p.parse()
else:
    print("Cancelando...")
