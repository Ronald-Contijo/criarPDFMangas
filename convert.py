import os
import img2pdf
from PyPDF2 import PdfMerger

# Diretório base onde estão os mangas (Diretório padrão do HakuNeko Desktop)
DIRETORIO_BASE = "/home/ronald/Documentos/Mangas"

'''
Estrutura de pastas 
/home/ronald/Documentos/Mangas
---/home/ronald/Documentos/Mangas/Manga1/
------/home/ronald/Documentos/Mangas/Manga1/Capitulo1
------/home/ronald/Documentos/Mangas/Manga1/Capitulo2

'''


# Lista de extensões de imagem suportadas
EXTENSOES = (".jpg", ".jpeg", ".png")


def converter_pasta_para_pdf(caminho_pasta, nome_pdf):
    imagens = []
    
    # Percorre os arquivos na pasta e filtra imagens
    for arquivo in sorted(os.listdir(caminho_pasta)):
        if arquivo.lower().endswith(EXTENSOES):
            imagens.append(os.path.join(caminho_pasta, arquivo))

    if imagens:
        caminho_pdf = os.path.join(caminho_pasta, f"{nome_pdf}.pdf")
        with open(caminho_pdf, "wb") as pdf:
            pdf.write(img2pdf.convert(imagens))
        return caminho_pdf
    return None

# Função para processar uma pasta principal e juntar os PDFs
def processar_pasta_principal(pasta_principal):
    caminho_principal = os.path.join(DIRETORIO_BASE, pasta_principal)
    
    if not os.path.isdir(caminho_principal):
        return
    
    pdfs_gerados = []
    

    for subpasta in sorted(os.listdir(caminho_principal)):
        caminho_subpasta = os.path.join(caminho_principal, subpasta)
        
        if os.path.isdir(caminho_subpasta):
            nome_pdf = f"{pasta_principal}_{subpasta}"
            pdf_gerado = converter_pasta_para_pdf(caminho_subpasta, nome_pdf)
            if pdf_gerado:
                pdfs_gerados.append(pdf_gerado)
    
    # Juntar PDFs de 20 em 20 pra ficar fácil de ler no KIndle
    for i in range(0, len(pdfs_gerados), 20):
        merger = PdfMerger()
        subset_pdfs = pdfs_gerados[i:i+20]
        nome_arquivo_saida = os.path.join(DIRETORIO_BASE, f"{pasta_principal}_parte_{i//20 + 1}.pdf")
        
        for pdf in subset_pdfs:
            merger.append(pdf)
        
        merger.write(nome_arquivo_saida)
        merger.close()
        print(f"PDF mesclado criado: {nome_arquivo_saida}")

# Percorre todas as pastas no diretório base e processa cada uma
for pasta_principal in sorted(os.listdir(DIRETORIO_BASE)):
    processar_pasta_principal(pasta_principal)

print("Conversão e mesclagem concluídas!")
