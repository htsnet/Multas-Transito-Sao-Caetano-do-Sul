#importando o módulo
import PyPDF2

#criando um objeto PDF
urlArquivo = "Diario Oficial Eletronico 06052020.pdf"  ###<<<----- informar o nome do arquivo: deve estar na mesma pasta
pdfFileObj = open(urlArquivo, "rb")
#pega a data para definir como lote
partesUrl = urlArquivo.split(" ")
lote = partesUrl[3].replace(".pdf", "")

#criando um objeto leitor
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#verificando o número de páginas do arquivo PDF
print("Total de páginas do PDF: {}".format(pdfReader.numPages))

def retiraAspas(valor):
    final = valor.replace("'", "\\'")
    final = final.replace('"', '\\"')
    return final

#pegar da página inicial até a final (não pega onde tem as multas)
todoTexto = ""
for x in range(0, pdfReader.getNumPages()):
    print("Página {}".format(x))
    pageObj = pdfReader.getPage(x)
    todoTexto = todoTexto + pageObj.extractText()

#só para preservar o conteúdo completo da tabela, como segurança
todoTextoReserva = todoTexto

#remove as quebras de linhas extras
#todoTexto = todoTexto.replace("\n\n", "")
todoTexto = todoTexto.replace("\n \n", " ")
todoTexto = todoTexto.replace("\n", "")

#localiza o texto que se encontra antes da tabela
textoPesquisa = "Prazo Defesa"
inicioDestaTabela = todoTexto.find(textoPesquisa) + len(textoPesquisa)

#retira o texto do início até o início da primeira tabela
todoTexto = todoTexto[inicioDestaTabela:]
inicioDestaTabela = 0

textoSeparado = ''

while True:    
    #localiza a linha em branco no final da tabela
    textoPesquisa = "Diário Oficial"
    fimDaTabelaOpcao1 = todoTexto.find(textoPesquisa, inicioDestaTabela)
    textoPesquisa = "Auto Infração"
    fimDaTabelaOpcao2 = todoTexto.find(textoPesquisa, inicioDestaTabela)
    
    #escolhe o menor índice para delimitar o início da próxima tabela
    if fimDaTabelaOpcao1 >= 0 and fimDaTabelaOpcao2 >= 0:
        fimDaTabela = min(fimDaTabelaOpcao1, fimDaTabelaOpcao2)
    elif fimDaTabelaOpcao1 < 0 and fimDaTabelaOpcao2 < 0:
        fimDaTabela = len(todoTexto)
    else:
        #se apenas um deles for -1, pega o outro
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
    #textoPesquisa = "Prazo Recurso"
    #inicioDestaTabelaOpcao1 = todoTexto.find(textoPesquisa)
    #se não vai pegar as notificações, deixa a opção 1 como -1
    inicioDestaTabelaOpcao1 = -1
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

#extraindo o texto da página
#print(pageObj.extractText())

#fechando o objeto PDF
pdfFileObj.close()


#tratando o arquivo final, quando não tem quebra de linhas
textoSeparadoSemQuebras = textoSeparado.replace("\n", " ")


#retira os espaços que sobram e trocados por vírgula
textoSemEspacos = '\n'
tratandoQuem = 5
quantosCaracteres = 0
for letra in reversed(textoSeparadoSemQuebras):
    #se for espaço, verifica se atingiu tamanho do campo tratado
    if letra != ' ':
        textoSemEspacos += letra
        quantosCaracteres += 1
        
        if tratandoQuem == 5 and quantosCaracteres == 10:
            tratandoQuem = 4
            quantosCaracteres = 0
            textoSemEspacos += ','

        elif tratandoQuem == 4 and quantosCaracteres == 10:
            tratandoQuem = 3
            quantosCaracteres = 0
            textoSemEspacos += ','
            
        elif tratandoQuem == 3 and quantosCaracteres == 5:
            tratandoQuem = 2
            quantosCaracteres = 0
            textoSemEspacos += ','
            
        elif tratandoQuem == 2 and quantosCaracteres == 7:
            tratandoQuem = 1
            quantosCaracteres = 0
            textoSemEspacos += ','
            
        elif tratandoQuem == 1 and quantosCaracteres >= 9:
            if letra in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'):
                tratandoQuem = 5
                quantosCaracteres = 0
                textoSemEspacos += '\n'
    
#inverte novamente a string e rerira primeira quebra de linha
textoFinal = ''            
for letra in reversed(textoSemEspacos[0:len(textoSemEspacos)-1]):
    textoFinal += letra

    
with open('arquivoCsv.csv', 'w') as file:
    file.write('Auto Infracao,Placa,Codigo Infracao,Data Infracao,Prazo Defesa\n')
    file.write(textoFinal)

#grava as informações no banco de dados MySQL
from conexaoMysql import *
conta = 0

try:
    #verifica quantos registros tem antes de iniciar
    sql = "select count(*) from CEN_tInfracoes"
    #print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    qtde = cursor.fetchone()
    print("Registros antes de iniciar", qtde)


    #apaga registros com mesmo lote
    sql = "delete from CEN_tInfracoes where InfracoesLote = '{0}'".format(lote)
    #print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)

    #verifica quantos registros tem antes de iniciar
    sql = "select count(*) from CEN_tInfracoes"
    #print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    qtde = cursor.fetchone()
    print("Registros depois de remover mesmo lote", qtde)

    
    #prepara linhas para inserir no banco de dados
    linhas = textoFinal.split('\n')
    #insere os registros encontrados
    primeiro = True
    for linha in linhas:
        #print(linha)
        campos = linha.split(",")
        #print(campos)
        #não processa se não tiver campos
        if len(campos) >= 4:
            auto = retiraAspas(campos[0])
            placa = retiraAspas(campos[1])
            codigo = retiraAspas(campos[2])
            dataInfracao = retiraAspas(campos[3])
            prazoDefesa = retiraAspas(campos[4])
            sql = """insert into CEN_tInfracoes (InfracoesLote, InfracoesAuto, InfracoesPlaca, InfracoesCodigo, InfracoesDataInfracao, InfracoesPrazoDefesa) values 
                ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(lote, auto, placa, codigo, dataInfracao, prazoDefesa)
            #print(sql)
            cursor = connection.cursor()
            cursor.execute(sql)
            #print(cursor.rowcount, "Registro inserido")
            conta = conta + 1
            #print(conta)

            #imprime os dados do primeiro registro
            if primeiro == True:
                print("Primeiro registro: ", auto, placa, codigo, dataInfracao, prazoDefesa)
                primeiro = False
        

    print("Último registro: ", auto, placa, codigo, dataInfracao, prazoDefesa)
    print("Total de registros inseridos: {0}".format(conta))    
    
    #verifica quantos registros tem depois de executar
    sql = "select count(*) from CEN_tInfracoes"
    cursor = connection.cursor()
    cursor.execute(sql)
    qtde = cursor.fetchone()
    print("Registros depois: ", qtde, "\n")
        
except mysql.connector.Error as error:
    print("Falha na inclusão {}".format(error))        

connection.commit()
cursor.close()  

    