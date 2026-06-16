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
        config_inicial = {"manutencao_ativa": False, "aviso_topo": "🚜 Bem-vindo ao FS23 Mods!", "mostrar_aviso": True}
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
            {"id": 1, "titulo": "FS23 Mapa Sul do Brasil", "desc": "Mapa detalhado com estradas brasileiras.", "link": "https://www.mediafire.com/file/mys6o1lm3cin56w/FS23_MAPA_SUL_DO_BRASIL_CLZIN_MODZ.apk/file", "downloads": 0},
            {"id": 2, "titulo": "FS23 Mod Completo BR", "desc": "O pacote definitivo com diversas modificações.", "link": "https://www.mediafire.com/file/g7egyr6mmqqb3q4/FS23_MODS_%25F0%259F%2587%25A7%25F0%259F%2587%25B7_COMPLET%25C3%2583O.apk/file", "downloads": 0}
        ]
        salvar_mods(mods_iniciais)
        return mods_iniciais
    with open(BANCO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_mods(dados):
    with open(BANCO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# HTML DO SITE
HTML_SITE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8"><title>FS23 Mods Brasil</title>
    <style>
        body { background: #0d110b; color: #f4f6f3; font-family: sans-serif; margin: 0; }
        .header { background: #151c12; padding: 40px; text-align: center; border-bottom: 4px solid #659b2c; }
        .card { background: #151c12; margin: 20px; padding: 20px; border-radius: 10px; border: 1px solid #659b2c; }
        .btn { background: #659b2c; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }
    </style>
</head>
<body>
    <div class="header"><h1>🚜 FS23 Mods Brasil</h1></div>
    {% for mod in lista_mods %}
    <div class="card">
        <h3>{{ mod.titulo }}</h3>
        <p>{{ mod.desc }}</p>
        <a href="/baixar/{{ mod.id }}" class="btn">Baixar APK</a>
    </div>
    {% endfor %}
</body>
</html>
'''

# HTML DO ADMIN
HTML_ADMIN = '''
<!DOCTYPE html>
<html lang="pt-BR">
<body>
    <h2>Painel Administrativo</h2>
    <p>Manutenção: {{ config.manutencao_ativa }} | <a href="/admin/toggle?senha={{ senha }}">Alternar</a></p>
    <hr>
    <h3>Adicionar Mod</h3>
    <form action="/admin/adicionar" method="POST">
        <input type="hidden" name="senha" value="{{ senha }}">
        <input type="text" name="titulo" placeholder="Título" required>
        <input type="text" name="desc" placeholder="Descrição" required>
        <input type="url" name="link" placeholder="Link Mediafire" required>
        <button type="submit">Salvar</button>
    </form>
    <h3>Mods Atuais</h3>
    {% for mod in lista_mods %}
        <div>{{ mod.titulo }} - <a href="/admin/excluir/{{ mod.id }}?senha={{ senha }}">Excluir</a></div>
    {% endfor %}
</body>
</html>
'''

@app.route('/')
def rota_home():
    config = carregar_config()
    if config.get("manutencao_ativa"): return "<h1>Site em Manutenção</h1>"
    return render_template_string(HTML_SITE, lista_mods=carregar_mods())

@app.route('/baixar/<int:mod_id>')
def rota_baixar(mod_id):
    lista = carregar_mods()
    for mod in lista:
        if mod['id'] == mod_id:
            mod['downloads'] += 1
            salvar_mods(lista)
            return redirect(mod['link'])
    return "Erro", 404

@app.route('/admin', methods=['GET', 'POST'])
def rota_admin():
    senha = request.form.get('senha') or request.args.get('senha')
    if senha != SENHA_CORRETA:
        return '<form method="POST"><input type="password" name="senha"><button>Entrar</button></form>'
    return render_template_string(HTML_ADMIN, lista_mods=carregar_mods(), config=carregar_config(), senha=senha)

@app.route('/admin/toggle')
def admin_toggle():
    senha = request.args.get('senha')
    if senha != SENHA_CORRETA: return "403"
    config = carregar_config()
    config['manutencao_ativa'] = not config['manutencao_ativa']
    salvar_config(config)
    return redirect(f'/admin?senha={senha}')

@app.route('/admin/adicionar', methods=['POST'])
def admin_adicionar():
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA: return "403"
    lista = carregar_mods()
    novo_id = max([m['id'] for m in lista]) + 1 if lista else 1
    lista.append({"id": novo_id, "titulo": request.form.get('titulo'), "desc": request.form.get('desc'), "link": request.form.get('link'), "downloads": 0})
    salvar_mods(lista)
    return redirect(f'/admin?senha={senha}')

@app.route('/admin/excluir/<int:mod_id>')
def admin_excluir(mod_id):
    senha = request.args.get('senha')
    if senha != SENHA_CORRETA: return "403"
    lista = carregar_mods()
    lista = [m for m in lista if m['id'] != mod_id]
    salvar_mods(lista)
    return redirect(f'/admin?senha={senha}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
