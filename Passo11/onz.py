from PIL import Image
import os
import shutil

def encontrar_faixa_inferior(imagem, cor_alvo, tolerancia=15):
    """
    Encontra a faixa descrita de baixo para cima.
    Retorna a posição Y onde deve ser feito o corte (acima da faixa) ou None se não encontrar.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Percorre a imagem de baixo para cima
    for y in range(altura - 1, 15, -1):
        faixa_encontrada = True
        
        # 1. Verifica os 4 pixels azuis inferiores (y-11 até y-8)
        for dy in range(4):
            pixel_y = y - 11 + dy
            if pixel_y < 0:
                faixa_encontrada = False
                break
                
            pixel = pixels[largura // 2, pixel_y]
            r, g, b = pixel[:3]
            
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if not faixa_encontrada:
            continue
            
        # 2. Verifica os 4 pixels brancos do meio (y-7 até y-4)
        for dy in range(4):
            pixel_y = y - 7 + dy
            pixel = pixels[largura // 2, pixel_y]
            r, g, b = pixel[:3]
            
            if (abs(r - 255) > tolerancia or 
                abs(g - 255) > tolerancia or 
                abs(b - 255) > tolerancia):
                faixa_encontrada = False
                break
        
        if not faixa_encontrada:
            continue
            
        # 3. Verifica os 4 pixels azuis superiores (y-3 até y)
        for dy in range(4):
            pixel_y = y - 3 + dy
            pixel = pixels[largura // 2, pixel_y]
            r, g, b = pixel[:3]
            
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            print(f"Faixa encontrada! Cortando na posição y={y-11}")
            return y - 11

    return None

def processar_imagens(pasta_origem, pasta_destino, cor_alvo):
    os.makedirs(pasta_destino, exist_ok=True)
    
    arquivos = [f for f in os.listdir(pasta_origem) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    print(f"Encontrados {len(arquivos)} arquivos para processar")
    
    for arquivo in arquivos:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        
        try:
            with Image.open(caminho_origem) as imagem:
                print(f"\nProcessando: {arquivo} ({imagem.width}x{imagem.height})")
                
                # Chamada corrigida da função
                posicao_corte = encontrar_faixa_inferior(imagem, cor_alvo)
                
                if posicao_corte is not None and posicao_corte > 0:
                    area_corte = (0, 0, imagem.width, posicao_corte)
                    imagem_recortada = imagem.crop(area_corte)
                    imagem_recortada.save(caminho_destino)
                    print(f"✓ Imagem recortada: {imagem_recortada.width}x{imagem_recortada.height}")
                else:
                    shutil.copy2(caminho_origem, caminho_destino)
                    print(f"✓ Imagem mantida original (sem faixa detectada)")
                    
        except Exception as e:
            print(f"✗ Erro ao processar {arquivo}: {e}")
            try:
                shutil.copy2(caminho_origem, caminho_destino)
                print(f"✓ Arquivo copiado mesmo com erro")
            except Exception as err:
                print(f"✗ Não foi possível copiar o arquivo: {err}")

if __name__ == "__main__":
    pasta_origem = "./questoes"
    pasta_destino = "finalizadas"
    cor_alvo = (64, 193, 243)  # Ajuste conforme os valores RGB da sua prova
    
    print("Iniciando processamento de imagens...")
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta '{pasta_origem}' não existe!")
        exit(1)
    
    processar_imagens(pasta_origem, pasta_destino, cor_alvo)
    print("\n" + "="*50)
    print("Processamento concluído!")