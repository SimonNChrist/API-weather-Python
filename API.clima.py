import requests
import json
import os

#configuracao
CHAVE_API = " "
ARQUIVO_ULTIMA_CIDADE = "ultima_cidade.txt"

def obter_local_ip():
    #cidade aproximada pelo IP
    try:
        resposta = requests.get("https://ipinfo.io/json")
        dados = resposta.json()
        cidade = dados.get("city")
        if cidade:
            return cidade
    except:
        pass
    return None


def obter_clima(cidade):
    #informacao climatica da cidade pesquisada
    cidade = cidade.strip().title()  #padroniza capitalizacao
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={CHAVE_API}&units=metric&lang=pt_br"

    try:
        resposta = requests.get(url)
    except requests.exceptions.RequestException:
        return "⚠️ Erro de conexão. Verifique sua internet."

    #se der certo (codigo 200)
    if resposta.status_code == 200:
        dados = resposta.json()
        temp = dados["main"]["temp"]
        desc = dados["weather"][0]["description"]
        emoji = escolher_emoji(desc)
        return f"{emoji}  {cidade}: {temp}°C, {desc.capitalize()}"
    elif resposta.status_code == 404:
        return f"⚠️ Não foi possível encontrar o clima de '{cidade}'."
    else:
        return f"⚠️ Erro ao obter dados da API (código {resposta.status_code})."


def escolher_emoji(descricao):
    #emojis com base na descricao do clima
    desc = descricao.lower()
    if "chuva" in desc or "rain" in desc:
        return "🌧️"
    elif "nuvem" in desc or "cloud" in desc:
        return "☁️"
    elif "céu limpo" in desc or "clear" in desc:
        return "☀️"
    elif "neve" in desc or "snow" in desc:
        return "❄️"
    elif "tempestade" in desc or "storm" in desc:
        return "⛈️"
    else:
        return "🌡️"


def salvar_ultima_cidade(cidade):
    #salva a ultima cidade pesquisada em um arquivo
    with open(ARQUIVO_ULTIMA_CIDADE, "w", encoding="utf-8") as f:
        f.write(cidade)


def carregar_ultima_cidade():
    #carrega a ultima cidade pesquisada, caso exista
    if os.path.exists(ARQUIVO_ULTIMA_CIDADE):
        with open(ARQUIVO_ULTIMA_CIDADE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None



#menu principal
def main():
    print("-  INFO CLIMA  -")

    ultima_cidade = carregar_ultima_cidade()
    cidade_automatica = obter_local_ip()

    if ultima_cidade:
        print(f"📍 Última cidade pesquisada: {ultima_cidade}")
    if cidade_automatica:
        print(f"🌍 Cidade detectada automaticamente: {cidade_automatica}")

    escolha = input("\nUsar (U)ltima, (A)utomática ou digitar nova cidade: ").strip()

    #define a cidade conforme a escolha do usuário
    if escolha.lower() == "u" and ultima_cidade:
        cidade = ultima_cidade
    elif escolha.lower() == "a" and cidade_automatica:
        cidade = cidade_automatica
    else:
        cidade = escolha if escolha else cidade_automatica or "Porto Alegre"

    print("\nBuscando informações do clima...\n")
    resultado = obter_clima(cidade)
    print(resultado)

    salvar_ultima_cidade(cidade)
    print("\n✅ Última cidade pesquisada salva com sucesso.")


#executa o programa
if __name__ == "__main__":
    main()

