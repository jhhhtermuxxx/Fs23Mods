import json
import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Configurações do sistema
SENHA_CORRETA = "adms123321"
BANCO_DADOS = "mods.json"
ARQUIVO_CONFIG = "config_painel.json"

def carregar_config():
    if not os.path.exists(ARQUIVO_CONFIG):
        config_inicial = {
            "manutencao_ativa": False,
            "aviso_topo": "🚜 Novas modificações adicionadas hoje! Aproveita os downloads diretos.",
            "mostrar_aviso": True
        }
        salvar_config(config_inicial)
        return config_inicial
    with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_config(dados):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_mods():
    if not os.path.exists(BANCO_DADOS):
        mods_iniciais = [
            {"id": 1, "titulo": "FS23 Mapa Sul do Brasil", "imagem": "MAPA SUL DO BRASIL", "desc": "Mapa detalhado com estradas brasileiras.", "link": "https://www.mediafire.com/file/mys6o1lm3cin56w/FS23_MAPA_SUL_DO_BRASIL_CLZIN_MODZ.apk/file", "categoria": "mapas", "downloads": 0},
            {"id": 2, "titulo": "FS23 Mod Completo BR", "imagem": "MOD COMPLETÃO BR", "desc": "O pacote definitivo com diversas modificações.", "link": "https://www.mediafire.com/file/g7egyr6mmqqb3q4/FS23_MODS_%25F0%259F%2587%25A7%25F0%259F%2587%25B7_COMPLET%25C3%2583O.apk/file", "categoria": "veiculos", "downloads": 0}
        ]
        salvar_mods(mods_iniciais)
        return mods_iniciais
    with open(BANCO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_mods(dados):
    with open(BANCO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# --- CSS E HTML PREMIUM ---
HTML_SITE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>FS23 Mods Brasil</title>
    <style>
        :root { --bg-principal: #0d110b; --bg-card: #151c12; --verde-fs: #659b2c; --texto-claro: #f4f6f3; }
        body { font-family: sans-serif; background-color: var(--bg-principal); color: var(--texto-claro); margin: 0; }
        .barra-aviso { background: #d93838; text-align: center; padding: 10px; font-weight: bold; }
        header { background: #151c12; text-align: center; padding: 40px; border-bottom: 4px solid var(--verde-fs); }
        .mod-card { background: var(--bg-card); margin: 20px; padding: 20px; border-radius: 10px; border: 1px solid var(--verde-fs); }
        .btn { background: var(--verde-fs); color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }
    </style>
</head>
<body>
    {% if config.mostrar_aviso %}<div class="barra-aviso">{{ config.aviso_topo }}</div>{% endif %}
    <header><h1>🚜 FS23 Mods Brasil</h1></header>
    {% for mod in lista_mods %}
    <div class="mod-card">
        <h3>{{ mod.titulo }}</h3>
        <p>{{ mod.desc }}</p>
        <a href="/baixar/{{ mod.id }}" class="btn">Baixar APK</a>
    </div>
    {% endfor %}
</body>
</html>
'''

# --- ROTAS ---
@app.route('/')
def rota_home():
    config = carregar_config()
    if config.get("manutencao_ativa"): return '<body style="background:#000;color:#fff;text-align:center;padding-top:100px;"><h1>Em manutenção</h1></body>'
    return render_template_string(HTML_SITE, lista_mods=carregar_mods(), config=config)

@app.route('/baixar/<int:mod_id>')
def rota_baixar(mod_id):
    lista = carregar_mods()
    for mod in lista:
        if mod['id'] == mod_id:
            mod['downloads'] += 1
            salvar_mods(lista)
            return redirect(mod['link'])
    return "Mod não encontrado", 404

@app.route('/admin', methods=['GET', 'POST'])
def rota_admin():
    senha = request.form.get('senha') or request.args.get('senha')
    if senha != SENHA_CORRETA:
        return '<form method="POST"><input type="password" name="senha"><button>Entrar</button></form>'
    config = carregar_config()
    return f'<h2>Admin</h2><a href="/admin/toggle?senha={senha}">Alternar Manutenção (Atual: {config["manutencao_ativa"]})</a>'

@app.route('/admin/toggle')
def admin_toggle():
    senha = request.args.get('senha')
    if senha != SENHA_CORRETA: return "403"
    config = carregar_config()
    config['manutencao_ativa'] = not config['manutencao_ativa']
    salvar_config(config)
    return redirect(f'/admin?senha={senha}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''

