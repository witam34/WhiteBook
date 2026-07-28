from PIL import Image
import os
import re

pasta_imagens = "inteiras"
pasta_saida = "."
os.makedirs(pasta_saida, exist_ok=True)

# Função para extrair apenas o número da página/sequência e ordenar
def get_sort_key(nome_arquivo):
    # Procura por qualquer número no formato 'pagina_enem_X' ou 'pagina_X'
    match = re.search(r'pagina_enem_(\d+)', nome_arquivo)
    if match:
        return int(match.group(1))
    
    # Caso os arquivos não tenham 'pagina_enem_', busca o primeiro grupo de dígitos no nome
    match_generico = re.search(r'(\d+)', nome_arquivo)
    return int(match_generico.group(1)) if match_generico else 0

# Pegar e ordenar as imagens corretamente
arquivos = [f for f in os.listdir(pasta_imagens) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
arquivos.sort(key=get_sort_key)

# Abrir todas as imagens na ordem correta
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando: {arquivo}")  # Para verificar a ordem

# Encontrar a largura máxima
largura_max = max(img.width for img in imagens)

# Concatenar verticalmente
altura_total = sum(img.height for img in imagens)
imagem_final = Image.new('RGB', (largura_max, altura_total))

y = 0
for img in imagens:
    imagem_final.paste(img, (0, y))
    y += img.height

# Salvar
imagem_final.save(os.path.join(pasta_saida, 'inteiras_concatenadas_verticalmente.png'))
print("Imagens concatenadas na ordem correta!")
print(f"Ordem dos arquivos: {arquivos}")