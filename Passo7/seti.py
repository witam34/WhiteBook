import os
from PIL import Image

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    """
    Converte valores de cor do GIMP (0-100%) para escala RGB (0-255).
    """
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def encontrar_bolas_questoes(imagem, cor_alvo, tolerancia=25, x_inicio=0, x_fim=100, altura_minima_bola=6):
    """
    Varre a imagem buscando pela presença da bola colorida na margem informada.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    y = 0

    while y < altura - altura_minima_bola:
        bola_encontrada = False

        # Percorre a largura (eixo X) especificada onde as bolinhas se localizam
        for x in range(x_inicio, min(x_fim, largura)):
            pixels_coincidentes = 0

            # Verifica verticalmente (eixo Y) se temos altura suficiente da cor da bola
            for dy in range(altura_minima_bola):
                pixel = pixels[x, y + dy]
                r, g, b = pixel[:3]

                # Distância da cor alvo
                if (abs(r - cor_alvo[0]) <= tolerancia and 
                    abs(g - cor_alvo[1]) <= tolerancia and 
                    abs(b - cor_alvo[2]) <= tolerancia):
                    pixels_coincidentes += 1
                else:
                    break

            # Se encontrou a sequência de pixels verticalmente, confirmamos a bola
            if pixels_coincidentes >= altura_minima_bola:
                bola_encontrada = True
                break

        if bola_encontrada:
            # Posição do corte ajustada (offset de pixels acima da bola para pegar a questão inteira)
            offset_topo = 15  # Ajuste conforme necessário no GIMP
            posicao_corte = max(0, y - offset_topo)
            
            posicoes_corte.append(posicao_corte)
            print(f"🎯 Bola identificada em Y={y}. Corte aplicado em Y={posicao_corte}")

            # Salta a altura estimada da bolinha/questão para evitar detecção dupla do mesmo marcador
            y += 40  
        else:
            y += 1

    return posicoes_corte

def dividir_imagem_por_bolas(caminho_imagem, pasta_saida, cor_alvo, x_inicio=0, x_fim=100):
    """
    Realiza os cortes na imagem com base nas posições encontradas.
    """
    if not os.path.exists(caminho_imagem):
        print(f"❌ Erro: Arquivo '{caminho_imagem}' não encontrado!")
        return

    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    print(f"🖼️ Imagem carregada: {largura}x{altura}px")

    posicoes_corte = encontrar_bolas_questoes(imagem, cor_alvo, x_inicio=x_inicio, x_fim=x_fim)

    if not posicoes_corte:
        print("⚠️ Nenhuma bola com a cor especificada foi encontrada!")
        return

    os.makedirs(pasta_saida, exist_ok=True)

    # Adiciona o final da imagem como último limite
    limites = posicoes_corte + [altura]
    
    for i in range(len(limites) - 1):
        y_inicio = limites[i]
        y_fim = limites[i + 1]

        if y_fim - y_inicio < 30:  # Ignora cortes excessivamente pequenos
            continue

        area_corte = (0, y_inicio, largura, y_fim)
        secao = imagem.crop(area_corte)

        nome_arquivo = f"questao_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"💾 Salvo: {nome_arquivo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    # --- CONFIGURAÇÕES DA PROVA ---
    CAMINHO_IMAGEM = "colunas_concatenadas_verticalmente.png"
    PASTA_SAIDA = "questoes_cortadas"

    # 1. Defina a cor da bola (Valores em % do GIMP: R, G, B)
    # Exemplo: Se no GIMP for (25.1%, 75.7%, 95.3%)
    COR_BOLA_GIMP = (87.8, 87.5, 87.5) 
    
    # 2. Faixa horizontal no GIMP (Eixo X) onde as bolas ficam posicionadas na coluna
    X_INICIAL = 5   # Pixel X onde a bola começa
    X_FINAL = 50    # Pixel X onde a bola termina

    # Execução
    cor_rgb = converter_cor_gimp_para_rgb(*COR_BOLA_GIMP)
    print(f"🔍 Buscando cor RGB: {cor_rgb}")
    
    dividir_imagem_por_bolas(
        CAMINHO_IMAGEM, 
        PASTA_SAIDA, 
        cor_rgb, 
        x_inicio=X_INICIAL, 
        x_fim=X_FINAL
    )
    print("✨ Processo concluído com sucesso!")