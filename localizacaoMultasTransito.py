#importando o módulo
import PyPDF2

#criando um objeto PDF
pdfFileObj = open("Diario Oficial Eletronico 17032020.pdf", "rb")

#criando um objeto leitor
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#verificando o número de páginas do arquivo PDF
print(pdfReader.numPages)

#criando um objeto da página 1
pageObj = pdfReader.getPage(0)

#pegar da página 4 até a 38 (onde tem as multas)
todoTexto = ""
for x in range(3, 39):
    print("*********************************Página {}".format(x))
    pageObj = pdfReader.getPage(x)
    todoTexto = todoTexto + pageObj.extractText()

#só para preservar o conteúdo completo da tabela, como segurança
todoTextoReserva = todoTexto

#localiza o texto que se encontra antes da tabela
textoPesquisa = "Prazo Defesa"
inicioDestaTabela = todoTexto.find(textoPesquisa) + len(textoPesquisa)

#retira o texto do início até o início da primeira tabela
todoTexto = todoTexto[inicioDestaTabela:]

while True:    
    #localiza a linha em branco no final da tabela
    textoPesquisa = "  \n"
    fimDaTabelaOpcao1 = todoTexto.find(textoPesquisa, inicioDestaTabela)
    textoPesquisa = "Auto Infração"
    fimDaTabelaOpcao2 = todoTexto.find(textoPesquisa, inicioDestaTabela)
    
    #escolhe o menor índice para delimitar o início da próxima tabela
    if fimDaTabelaOpcao1 >= 0 and fimDaTabelaOpcao2 >= 0:
        fimDaTabela = min(fimDaTabelaOpcao1, fimDaTabelaOpcao2)    
    else:
        #se um deles for -1, pega o outro
        fimDaTabela = max(fimDaTabelaOpcao1, fimDaTabelaOpcao2)    

    #mostra o pedaço onde localizou
    print("Fim: {}".format(todoTexto[fimDaTabela-10:fimDaTabela+10]))
    #se não tem mais informação, interrompe
    if fimDaTabela < 0:
        #pega o último bloco antes de interromper
        textoSeparado = textoSeparado + todoTexto[inicioDestaTabela:fimDaTabela]
        print("***Pegou o último bloco e encerrou***")
        break
    
    #prepara o conteúdo para juntar com os anteriores
    blocoTexto = todoTexto[inicioDestaTabela:fimDaTabela]
    #remove espaços antes do final da linha
    blocoTexto = blocoTexto.replace(" \n", "\n")
    #remove espaços no início da linha
    blocoTexto = blocoTexto.replace("\n ", "\n")
    #remove 2 trocas de linha
    blocoTexto = blocoTexto.replace("\n\n", "\n")
    
    #separa o texto útil (corresponde à tabela
    textoSeparado = textoSeparado + blocoTexto
    
    #remove todo o bloco do texto base
    todoTexto = todoTexto[fimDaTabela:]
    
    #verifica se bloco ficou sem informação
    if len(todoTexto) < 10:
        break

    #localiza o texto que inicia nova da tabela
    textoPesquisa = "Prazo Recurso"
    inicioDestaTabelaOpcao1 = todoTexto.find(textoPesquisa)
    textoPesquisa = "Prazo Defesa"
    inicioDestaTabelaOpcao2 = todoTexto.find(textoPesquisa)
    
    #escolhe o menor índice para delimitar o início da próxima tabela
    if inicioDestaTabelaOpcao1 >= 0 and inicioDestaTabelaOpcao2 >= 0:
        inicioDestaTabela = min(inicioDestaTabelaOpcao1, inicioDestaTabelaOpcao2)    
    else:        
        #se um deles for -1, pega o outro
        inicioDestaTabela = max(inicioDestaTabelaOpcao1, inicioDestaTabelaOpcao2)    
        
    #se não tem mais informação, interrompe
    print("Início {}: {}".format(inicioDestaTabela, todoTexto[inicioDestaTabela-10:inicioDestaTabela+10]))
    if inicioDestaTabela < 0:
        print("********* Não achou mais tabela *********")
        break
    
    #se não terminou, acrescenta o tamanho da string pesquisada
    inicioDestaTabela = inicioDestaTabela + len(textoPesquisa)

#fechando o objeto PDF
pdfFileObj.close()

#O resultado está na variável "textoSeparado". Basta copiar o conteúdo e colar em uma planilha para uso.