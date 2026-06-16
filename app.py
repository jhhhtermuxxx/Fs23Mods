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
            "aviso_topo": "🚜 Novas modificações adicionadas recentemente!",
            "mostrar_aviso": False
        }
        salvar_config(config_inicial)
        return config_inicial
    with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_config(dados):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_mods():
    if not os.path.exists(BANCO_DADOS):
        mods_iniciais = [
            {"id": 1, "titulo": "FS23 Jatobá e Nova Fantinati", "categoria": "mapas", "link": "https://www.mediafire.com", "downloads": 124},
            {"id": 2, "titulo": "FS23 Três Lagoas BR", "categoria": "mapas", "link": "https://www.mediafire.com", "downloads": 89},
            {"id": 3, "titulo": "John Deere 7R Series", "categoria": "tratores", "link": "https://www.mediafire.com", "downloads": 245},
            {"id": 4, "titulo": "Pack Caminhões Brasileiros V2", "categoria": "veiculos", "link": "https://www.mediafire.com", "downloads": 312}
        ]
        salvar_mods(mods_iniciais)
        return mods_iniciais
    with open(BANCO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_mods(dados):
    with open(BANCO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# --- TEMPLATES HTML (INJETADOS VIA STRING) ---

HTML_SITE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FS23 Mods Brasil</title>
    <style>
        body { background-color: #0b0e0a; color: #fff; font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .header { background-color: #131a10; padding: 20px; text-align: center; border-bottom: 3px solid #659b2c; }
        .aviso-barra { background-color: #d93838; color: white; text-align: center; padding: 10px; font-weight: bold; font-size: 0.9rem; }
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .nav-abas { display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; }
        .aba { background: #1c2618; color: #fff; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold; border: 1px solid #2d3f26; }
        .aba.ativa { background: #659b2c; border-color: #7cbd3f; }
        .mod-card { background: #131a10; border: 1px solid #23301c; border-radius: 8px; padding: 15px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }
        .mod-info { display: flex; flex-direction: column; }
        .mod-titulo { font-size: 1.2rem; font-weight: bold; color: #fff; margin-bottom: 5px; }
        .mod-cat { font-size: 0.8rem; color: #659b2c; font-weight: bold; text-transform: uppercase; }
        .btn-down { background: #659b2c; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; font-size: 0.9rem; }
    </style>
</head>
<body>
    {% if config.mostrar_aviso %}
    <div class="aviso-barra">{{ config.aviso_topo }}</div>
    {% endif %}
    
    <div class="header">
        <h1>🚜 FS23 MODS BRASIL</h1>
        <p>Os melhores modificações para o teu Farming Simulator 23</p>
    </div>
    
    <div class="container">
        <div class="nav-abas">
            <a href="/" class="aba {% if cat_atual == 'todos' %}ativa{% endif %}">Todos</a>
            <a href="/?cat=mapas" class="aba {% if cat_atual == 'mapas' %}ativa{% endif %}">Mapas</a>
            <a href="/?cat=tratores" class="aba {% if cat_atual == 'tratores' %}ativa{% endif %}">Tratores</a>
            <a href="/?cat=veiculos" class="aba {% if cat_atual == 'veiculos' %}ativa{% endif %}">Veículos</a>
        </div>
        
        {% if lista_mods %}
            {% for mod in lista_mods %}
            <div class="mod-card">
                <div class="mod-info">
                    <span class="mod-cat">[{{ mod.categoria }}]</span>
                    <span class="mod-titulo">{{ mod.titulo }}</span>
                </div>
                <a href="/baixar/{{ mod.id }}" class="btn-down" target="_blank">Fazer Download</a>
            </div>
            {% endfor %}
        {% else %}
            <p style="text-align: center; color: #72806e;">Nenhum mod encontrado nesta categoria.</p>
        {% endif %}
    </div>
</body>
</html>
'''

HTML_ADMIN = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Admin</title>
    <style>
        body { background: #0b0e0a; color: #fff; font-family: Arial, sans-serif; padding: 15px; margin: 0; }
        .painel { max-width: 500px; margin: 0 auto; background: #131a10; border: 1px solid #23301c; border-radius: 8px; padding: 20px; }
        h2, h3 { color: #fff; margin-top: 0; border-bottom: 1px solid #23301c; padding-bottom: 10px; }
        .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
        .stat-card { background: #1c2618; border: 1px solid #2d3f26; padding: 10px; border-radius: 6px; text-align: center; }
        .stat-card span { display: block; font-size: 0.8rem; color: #72806e; text-transform: uppercase; }
        .stat-card strong { font-size: 1.5rem; color: #659b2c; }
        .form-grupo { margin-bottom: 15px; }
        label { display: block; font-size: 0.85rem; color: #659b2c; font-weight: bold; margin-bottom: 5px; }
        input, select, textarea { width: 100%; padding: 10px; background: #0b0e0a; color: #fff; border: 1px solid #23301c; border-radius: 6px; box-sizing: border-box; }
        .btn { width: 100%; padding: 12px; background: #659b2c; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        .btn-aviso { background: #1f578a; margin-top: 5px; }
        .btn-manutencao { background: #d93838; margin-top: 15px; }
        .mod-lista { margin-top: 25px; }
        .mod-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; background: #0b0e0a; border: 1px solid #1f2a18; border-radius: 6px; margin-bottom: 8px; font-size: 0.9rem; }
        .btn-excluir { color: #ff6b6b; text-decoration: none; font-weight: bold; font-size: 0.85rem; }
    </style>
</head>
<body>
    <div class="painel">
        <h2>Painel FS23 Gerenciamento Pro 🚜</h2>
        
        <div class="stats">
            <div class="stat-card"><span>Mods Ativos</span><strong>{{ total }}</strong></div>
            <div class="stat-card"><span>Downloads Totais</span><strong>{{ total_downloads }}</strong></div>
        </div>

        <h3>📢 Sistema de Avisos do Site</h3>
        <form method="POST" action="/admin/config">
            <input type="hidden" name="senha" value="{{ senha_usada }}">
            <div class="form-grupo" style="display: flex; align-items: center; gap: 8px;">
                <input type="checkbox" name="mostrar_aviso" value="sim" {% if config.mostrar_aviso %}checked{% endif %} style="width: auto;">
                <label style="margin: 0;">Ativar barra de aviso vermelha</label>
            </div>
            <div class="form-grupo">
                <input type="text" name="aviso_topo" value="{{ config.aviso_topo }}">
            </div>
            <button type="submit" class="btn btn-aviso">Atualizar Avisos</button>
        </form>

        <hr style="border: 0; border-top: 1px solid #23301c; margin: 20px 0;">

        <h3>➕ Lançar Novo Mod</h3>
        <form method="POST" action="/admin/adicionar">
            <input type="hidden" name="senha" value="{{ senha_usada }}">
            <div class="form-grupo">
                <label>Título do Mod:</label>
                <input type="text" name="titulo" placeholder="Ex: Fendt 900 Vario V1" required>
            </div>
            <div class="form-grupo">
                <label>Categoria:</label>
                <select name="categoria">
                    <option value="mapas">Mapas</option>
                    <option value="tratores">Tratores</option>
                    <option value="veiculos">Veículos</option>
                </select>
            </div>
            <div class="form-grupo">
                <label>Link Direto do Mediafire:</label>
                <input type="url" name="link" placeholder="https://www.mediafire.com/file/..." required>
            </div>
            <button type="submit" class="btn">Lançar no Site</button>
        </form>

        <div class="mod-lista">
            <h3>📁 Mods no Ar</h3>
            {% for mod in lista_mods %}
            <div class="mod-item">
                <div>
                    <strong style="color: #659b2c;">[{{ mod.categoria }}]</strong><br>
                    {{ mod.titulo }}
                </div>
                <div style="text-align: right;">
                    <span style="color: #e5a93b; font-size: 0.8rem;">📥 {{ mod.downloads }}</span><br>
                    <a href="/admin/excluir/{{ mod.id }}?senha={{ senha_usada }}" class="btn-excluir" onclick="return confirm('Apagar este mod para sempre?')">❌ Excluir</a>
                </div>
            </div>
            {% endfor %}
        </div>

        <hr style="border: 0; border-top: 1px solid #23301c; margin: 20px 0;">
        <h3>⚠️ Status do Servidor</h3>
        <p>O site está no ar normalmente? <strong>{% if config.manutencao_ativa %}<span style="color: #d93838;">NÃO (Manutenção)</span>{% else %}<span style="color: #659b2c;">SIM (Online)</span>{% endif %}</strong></p>
        <form method="POST" action="/admin/manutencao">
            <input type="hidden" name="senha" value="{{ senha_usada }}">
            <button type="submit" class="btn btn-manutencao">Alternar Modo Manutenção</button>
        </form>
    </div>
</body>
</html>
'''

# --- CONTROLE DAS ROTAS ---

@app.route('/')
def rota_home():
    config = carregar_config()
    if config.get("manutencao_ativa"):
        return '<body style="background:#0b0e0a;color:#fff;text-align:center;padding-top:100px;"><h1>🚜 Site em Manutenção Básica</h1><p>Estamos organizando novos conteúdos. Volte mais tarde!</p></body>'
    
    lista = carregar_mods()
    cat = request.args.get('cat', 'todos')
    if cat != 'todos':
        lista = [m for m in lista if m.get('categoria') == cat]
    return render_template_string(HTML_SITE, lista_mods=lista, config=config, cat_atual=cat)

@app.route('/baixar/<int:mod_id>')
def rota_baixar(mod_id):
    lista = carregar_mods()
    link_redirecionar = "https://www.mediafire.com"
    for mod in lista:
        if mod['id'] == mod_id:
            if 'downloads' not in mod:
                mod['downloads'] = 0
            mod['downloads'] += 1
            link_redirecionar = mod['link']
            break
    salvar_mods(lista)
    return redirect(link_redirecionar)

@app.route('/admin', methods=['GET', 'POST'])
def rota_admin():
    senha_digitada = request.form.get('senha') or request.args.get('senha')
    
    if senha_digitada != SENHA_CORRETA:
        return '''
            <body style="background: #0b0e0a; color: #f4f6f3; font-family: 'Segoe UI', Arial, sans-serif; text-align: center; padding: 60px 20px; margin: 0;">
                <div style="max-width: 450px; margin: 0 auto; background: #131a10; border: 1px solid #23301c; border-top: 4px solid #659b2c; padding: 30px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.7);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🔒</div>
                    <h2 style="margin: 0 0 5px 0; text-transform: uppercase; letter-spacing: 1px; font-size: 1.4rem; color: #fff;">Autenticação Restrita</h2>
                    <p style="color: #72806e; font-size: 0.9rem; margin: 0 0 25px 0;">Painel de Administração — FS23 Mods Brasil</p>
                    
                    <form method="POST" action="/admin">
                        <div style="text-align: left; margin-bottom: 15px;">
                            <label style="font-size: 0.8rem; font-weight: bold; color: #659b2c; text-transform: uppercase; letter-spacing: 0.5px;">Palavra-passe do Sistema:</label>
                            <input type="password" name="senha" placeholder="Introduza a chave de acesso..." style="width: 100%; padding: 14px; margin-top: 6px; background: #0b0e0a; color: #fff; border: 1px solid #23301c; border-radius: 6px; box-sizing: border-box; font-size: 1rem; transition: border 0.2s;">
                        </div>
                        <button type="submit" style="width: 100%; padding: 14px; background: linear-gradient(#659b2c, #4e7822); color: #fff; border: none; border-radius: 6px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; cursor: pointer; font-size: 0.95rem; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">Aceder à Plataforma</button>
                    </form>
                    
                    ''' + ('''
                    <div style="margin-top: 20px; padding: 12px; background: rgba(217, 56, 56, 0.1); border: 1px solid #d93838; border-radius: 6px; color: #ff6b6b; font-size: 0.85rem; font-weight: bold; text-transform: uppercase;">
                        ⚠️ Acesso Recusado: Credenciais Inválidas!
                    </div>
                    ''' if senha_digitada else "") + '''
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #1f2a18; color: #556152; font-size: 0.75rem; line-height: 1.5; text-align: left;">
                        * Aviso: Tentativas de acesso não autorizadas serão registadas no servidor Render.<br>
                        * Para manutenção de credenciais, utilize o terminal local do Termux.
                    </div>
                </div>
            </body>
        '''
    
    lista = carregar_mods()
    config = carregar_config()
    total_downloads = sum([m.get('downloads', 0) for m in lista])
    
    return render_template_string(HTML_ADMIN, lista_mods=lista, total=len(lista), total_downloads=total_downloads, config=config, senha_usada=senha_digitada)

@app.route('/admin/adicionar', methods=['POST'])
def admin_adicionar():
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 403
    
    titulo = request.form.get('titulo')
    categoria = request.form.get('categoria')
    link = request.form.get('link')
    
    lista = carregar_mods()
    novo_id = max([m['id'] for m in lista]) + 1 if lista else 1
    
    novo_mod = {
        "id": novo_id,
        "titulo": titulo,
        "categoria": categoria,
        "link": link,
        "downloads": 0
    }
    
    lista.append(novo_mod)
    salvar_mods(lista)
    return redirect(f'/admin?senha={senha}')

@app.route('/admin/excluir/<int:mod_id>')
def admin_excluir(mod_id):
    senha = request.args.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 403
    
    lista = carregar_mods()
    lista = [m for m in lista if m['id'] != mod_id]
    salvar_mods(lista)
    return redirect(f'/admin?senha={senha}')

@app.route('/admin/config', methods=['POST'])
def admin_config():
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 403
    
    config = carregar_config()
    config['mostrar_aviso'] = request.form.get('mostrar_aviso') == 'sim'
    config['aviso_topo'] = request.form.get('aviso_topo', '')
    salvar_config(config)
    return redirect(f'/admin?senha={senha}')

@app.route('/admin/manutencao', methods=['POST'])
def admin_manutencao():
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 403
    
    config = carregar_config()
    config['manutencao_ativa'] = not config.get('manutencao_ativa', False)
    salvar_config(config)
    return redirect(f'/admin?senha={senha}')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

