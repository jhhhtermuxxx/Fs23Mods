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
            {"id": 1, "titulo": "FS23 Jatobá e Nova Fantinati", "imagem": "MAPA JATOBÁ & FANTINATI", "desc": "Incrível modificação unindo os mapas Jatobá e Nova Fantinati com vegetação realista.", "link": "https://www.mediafire.com/...", "categoria": "mapas", "downloads": 124},
            {"id": 2, "titulo": "FS23 Três Lagoas BR", "imagem": "MAPA TRÊS LAGOAS 🇧🇷", "desc": "Sinta a experiência de cultivar no mapa de Três Lagoas com estradas de terra brasileiras.", "link": "https://www.mediafire.com/...", "categoria": "mapas", "downloads": 89},
            {"id": 3, "titulo": "John Deere 7R Series", "imagem": "JD 7R SERIES", "desc": "Trator potente com ronco original e opções de rodas duplas para a sua fazenda.", "link": "https://www.mediafire.com/...", "categoria": "tratores", "downloads": 245},
            {"id": 4, "titulo": "Pack Caminhões Brasileiros V2", "imagem": "PACK COMPLETÃO BR 🚜", "desc": "O pacote definitivo! Esse APK traz diversas modificações de caminhões ronco direto.", "link": "https://www.mediafire.com/...", "categoria": "veiculos", "downloads": 312}
        ]
        salvar_mods(mods_iniciais)
        return mods_iniciais
    with open(BANCO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_mods(dados):
    with open(BANCO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# --- SITE COM DESIGN PREMIUM INSPIRADO NO FARMING SIMULATOR ---
HTML_SITE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FS23 Mods Brasil</title>
    <style>
        :root {
            --bg-principal: #0d110b;
            --bg-card: #151c12;
            --verde-fs: #659b2c;
            --verde-hover: #7dbf37;
            --detalhe-ouro: #e5a922;
            --texto-claro: #f4f6f3;
            --texto-escuro: #939e90;
        }

        body { 
            font-family: 'Segoe UI', Roboto, sans-serif; 
            background-color: var(--bg-principal); 
            color: var(--texto-claro); 
            margin: 0; 
            padding: 0; 
        }

        .barra-aviso { 
            background: linear-gradient(90deg, #b32424, #d93838); 
            color: #fff; 
            text-align: center; 
            padding: 12px; 
            font-weight: bold; 
            font-size: 0.95rem; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.5);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        header { 
            background: linear-gradient(rgba(0,0,0,0.6), rgba(13,17,11,0.95)), url('https://images.unsplash.com/photo-1592417817098-8f3d6eb18865?q=80&w=1200') center/cover;
            text-align: center; 
            padding: 50px 20px; 
            border-bottom: 4px solid var(--verde-fs); 
        }

        header h1 { 
            margin: 0; 
            color: white; 
            font-size: 2.8rem; 
            text-transform: uppercase; 
            letter-spacing: 2px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        }
        
        header h1 span { color: var(--verde-fs); }

        header p { 
            margin: 12px 0 0 0; 
            color: var(--texto-escuro); 
            font-size: 1.1rem; 
            font-weight: 500;
        }
        
        .menu-categorias { 
            text-align: center; 
            margin: 25px 0; 
            padding: 0 10px;
        }

        .btn-cat { 
            background-color: #1a2417; 
            color: var(--texto-escuro); 
            border: 1px solid #2d3f27; 
            padding: 10px 18px; 
            margin: 5px; 
            border-radius: 6px; 
            cursor: pointer; 
            font-weight: bold; 
            text-decoration: none; 
            display: inline-block;
            transition: all 0.2s ease;
            text-transform: uppercase;
            font-size: 0.85rem;
        }

        .btn-cat:hover, .btn-cat.ativo { 
            background-color: var(--verde-fs); 
            color: white; 
            border-color: var(--verde-hover);
            box-shadow: 0 0 10px rgba(101,155,44,0.4);
        }

        .container { 
            max-width: 1200px; 
            margin: 0 auto 40px auto; 
            padding: 0 20px; 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 25px; 
        }

        .mod-card { 
            background-color: var(--bg-card); 
            border: 1px solid #232e1e; 
            border-radius: 8px; 
            overflow: hidden; 
            display: flex; 
            flex-direction: column; 
            position: relative;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        .mod-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
            border-color: #384a30;
        }

        .badge-cat { 
            position: absolute; 
            top: 12px; 
            left: 12px; 
            background: rgba(13,17,11,0.85); 
            color: var(--detalhe-ouro); 
            padding: 5px 12px; 
            border-radius: 4px; 
            font-size: 0.75rem; 
            font-weight: bold; 
            text-transform: uppercase; 
            border: 1px solid var(--detalhe-ouro); 
            z-index: 2;
        }

        .mod-image-box { 
            width: 100%; 
            height: 160px; 
            background: linear-gradient(135deg, #1b2618, #2a3d24); 
            display: flex; 
            flex-direction: column;
            align-items: center; 
            justify-content: center; 
            border-bottom: 3px solid var(--verde-fs);
            padding: 10px;
            box-sizing: border-box;
        }

        .mod-icon {
            font-size: 2.8rem;
            margin-bottom: 5px;
        }

        .mod-image-text {
            color: #fff;
            font-weight: 700;
            font-size: 1.1rem;
            text-align: center;
            text-transform: uppercase;
            text-shadow: 1px 1px 5px rgba(0,0,0,0.6);
        }

        .mod-info { 
            padding: 20px; 
            flex-grow: 1; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
        }

        .mod-title { 
            font-size: 1.3rem; 
            margin: 0 0 10px 0; 
            color: #ffffff; 
            font-weight: 600;
        }

        .mod-desc { 
            font-size: 0.9rem; 
            color: var(--texto-escuro); 
            line-height: 1.6; 
            margin-bottom: 20px; 
        }

        .mod-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: #72806e;
            margin-bottom: 15px;
            padding-top: 10px;
            border-top: 1px solid #1f2a1a;
        }

        .btn-download { 
            display: block; 
            text-align: center; 
            background: linear-gradient(var(--verde-fs), #527e24); 
            color: #fff; 
            text-decoration: none; 
            padding: 14px; 
            border-radius: 6px; 
            font-weight: bold; 
            text-transform: uppercase; 
            letter-spacing: 1px;
            transition: background 0.2s ease;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        }

        .btn-download:hover {
            background: linear-gradient(var(--verde-hover), var(--verde-fs));
        }
    </style>
</head>
<body>
    {% if config.mostrar_aviso and config.aviso_topo %}
    <div class="barra-aviso">{{ config.aviso_topo }}</div>
    {% endif %}

    <header>
        <h1>Farming Simulator 23 <span>Mods</span></h1>
        <p>A tua central brasileira de APKs, Mapas e Máquinas agrícolas modificadas</p>
    </header>

    <div class="menu-categorias">
        <a href="/" class="btn-cat {% if cat_atual == 'todos' %}ativo{% endif %}">Todos</a>
        <a href="/?cat=mapas" class="btn-cat {% if cat_atual == 'mapas' %}ativo{% endif %}">🗺️ Mapas</a>
        <a href="/?cat=tratores" class="btn-cat {% if cat_atual == 'tratores' %}ativo{% endif %}">🚜 Tratores</a>
        <a href="/?cat=veiculos" class="btn-cat {% if cat_atual == 'veiculos' %}ativo{% endif %}">🚛 Veículos</a>
        <a href="/?cat=packs" class="btn-cat {% if cat_atual == 'packs' %}ativo{% endif %}">📦 Packs</a>
    </div>

    <div class="container">
https://fs23mods.onrender.com/admin        {% for mod in lista_mods %}
        <div class="mod-card">
            <span class="badge-cat">{{ mod.categoria }}</span>
            <div class="mod-image-box">
                <span class="mod-icon">
                    {% if mod.categoria == 'mapas' %}🗺️
                    {% elif mod.categoria == 'tratores' %}🚜
                    {% elif mod.categoria == 'veiculos' %}🚛
                    {% else %}📦{% endif %}
                </span>
                <div class="mod-image-text">{{ mod.imagem }}</div>
            </div>
            <div class="mod-info">
                <div>
                    <h2 class="mod-title">{{ mod.titulo }}</h2>
                    <p class="mod-desc">{{ mod.desc }}</p>
                </div>
                <div>
                    <div class="mod-meta">
                        <span>Servidor: <b>Mediafire</b></span>
                        <span>📥 <b>{{ mod.downloads if mod.downloads else 0 }}</b> downloads</span>
                    </div>
                    <a href="/baixar/{{ mod.id }}" target="_blank" class="btn-download">Fazer Download</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

# --- PAINEL ADMIN ADAPTADO ---
HTML_ADMIN = '''
<!DOCTYPE html>
<html>
<head>
    <title>Painel Admin - FS23</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; background: #1a1a1a; color: #fff; padding: 15px; margin: 0; }
        .bloco { background: #262626; padding: 20px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #333; }
        input, select, textarea { width: 100%; padding: 10px; margin: 8px 0; background: #333; color: #fff; border: 1px solid #444; border-radius: 6px; box-sizing: border-box; }
        button { background: #659b2c; color: white; padding: 12px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; font-size: 1rem; }
        button:hover { background: #7dbf37; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; background: #222; }
        th, td { border: 1px solid #333; padding: 12px; text-align: left; font-size: 0.9rem; }
        th { background: #2d2d2d; color: #659b2c; }
        .flex-container { display: flex; gap: 15px; flex-wrap: wrap; }
        .card-stat { flex: 1; min-width: 140px; background: #333; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #659b2c; }
    </style>
</head>
<body>
    <h2>Painel FS23 Gerenciamento Pro 🚜</h2>
    
    <div class="bloco">
        <div class="flex-container">
            <div class="card-stat">
                <div style="font-size: 0.85rem; color:#aaa;">MODS ATIVOS</div>
                <div style="font-size: 1.8rem; font-weight:bold; color:#659b2c;">{{ total }}</div>
            </div>
            <div class="card-stat">
                <div style="font-size: 0.85rem; color:#aaa;">DOWNLOADS TOTAIS</div>
                <div style="font-size: 1.8rem; font-weight:bold; color:#e5a922;">{{ total_downloads }}</div>
            </div>
        </div>
    </div>

    <div class="bloco" style="border-left: 4px solid #31708f;">
        <h3>📢 Sistema de Avisos do Site</h3>
        <form method="POST" action="/admin/config">
            <input type="hidden" name="senha" value="{{ senha_usada }}">
            <label><input type="checkbox" name="mostrar_aviso" value="sim" {% if config.mostrar_aviso %}checked{% endif %} style="width:auto; margin-right:10px;">Ativar barra de aviso vermelha</label>
            <input type="text" name="aviso_topo" value="{{ config.aviso_topo }}" placeholder="Escreva a mensagem para o topo do site...">
            <button type="submit" style="background:#31708f;">Atualizar Avisos</button>
        </form>
    </div>

    <div class="bloco" style="border-left: 4px solid #d9822b;">
        <h3>⚠️ Status do Servidor</h3>
        <p>O site está no ar normalmente? <b>{% if config.manutencao_ativa %}<span style="color:#ff6b6b;">NÃO (Manutenção Ativa)</span>{% else %}<span style="color:#659b2c;">SIM (Online)</span>{% endif %}</b></p>
        <form method="POST" action="/admin/manutencao">
            <input type="hidden" name="senha" value="{{ senha_usada }}">
            <button type="submit" style="background:#d9822b;">Alternar Modo Manutenção</button>
        </form>
    </div>

    <div class="bloco">
        <h3>➕ Publicar Mod com Categoria</h3>
        <form method="POST" action="/admin/adicionar">
            <input type="hidden" name="senha" value="{{ senha_usada }}">
            <label>Nome do Mod:</label>
            <input type="text" name="titulo" placeholder="Ex: Trator Massey Ferguson 4275" required>
            
            <label>Subtítulo Curto (Fica na caixa de imagem):</label>
            <input type="text" name="imagem" placeholder="Ex: MF 4275 BRASIL" required>
            
            <label>Categoria:</label>
            <select name="categoria">
                <option value="mapas">🗺️ Mapa</option>
                <option value="tratores">🚜 Trator</option>
                <option value="veiculos">🚛 Veículo / Caminhão</option>
                <option value="packs">📦 Pack Completo (APK)</option>
            </select>
            
            <label>Descrição do Mod:</label>
            <textarea name="desc" rows="3" placeholder="Detalhes do mod, novidades da V2..." required></textarea>
            
            <label>Link Direto do Mediafire:</label>
            <input type="text" name="link" placeholder="https://www.mediafire.com/file/..." required>
            
            <button type="submit">Lançar no Site</button>
        </form>
    </div>

    <div class="bloco" style="overflow-x: auto;">
        <h3>📂 Mods no Ar</h3>
        <table>
            <tr>
                <th>Mod</th>
                <th>Downloads</th>
                <th>Ação</th>
            </tr>
            {% for mod in lista_mods %}
            <tr>
                <td><b>[{{ mod.categoria }}]</b><br>{{ mod.titulo }}</td>
                <td>📥 {{ mod.downloads if mod.downloads else 0 }}</td>
                <td>
                    <form method="POST" action="/admin/excluir/{{ mod.id }}" style="display:inline;">
                        <input type="hidden" name="senha" value="{{ senha_usada }}">
                        <button type="submit" style="background:none; color:#ff6b6b; padding:0; width:auto; font-size:0.9rem;">❌ Excluir</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
'''

# --- CONTROLE DAS ROTAS ---

@app.route('/')
def rota_home():
    config = carregar_config()
    if config["manutencao_ativa"]:
        return "<body style='background:#0d110b;color:#fff;text-align:center;font-family:Arial;padding-top:100px;'><h1>🚜 Site em Manutenção Básica</h1><p>Estamos organizando novos arquivos de Farming Simulator 23! Voltamos já.</p></body>"
    
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
            <body style="background:#1a1a1a; color:#fff; font-family:Arial; text-align:center; padding-top:100px;">
                <h2>Painel FS23 - Controle Restrito</h2>
                <form method="POST" action="/admin">
                    <input type="password" name="senha" placeholder="Senha do Administrador" style="padding:12px; width:220px; background:#333; color:#white; border:1px solid #444; border-radius:4px;"><br><br>
                    <button type="submit" style="padding:10px 20px; background:#659b2c; color:#fff; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">Entrar no Sistema</button>
                </form>
                <p style="color:#ff6b6b; margin-top:15px;">''' + ("⚠️ Senha Incorreta!" if senha_digitada else "") + '''</p>
            </body>
        '''
    
    lista = carregar_mods()
    config = carregar_config()
    total_downloads = sum([m.get('downloads', 0) for m in lista])
    
    return render_template_string(HTML_ADMIN, lista_mods=lista, total=len(lista), total_downloads=total_downloads, config=config, senha_usada=senha_digitada)

@app.route('/admin/config', methods=['POST'])
def acao_config():
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 401
        
    config = carregar_config()
    config["mostrar_aviso"] = request.form.get('mostrar_aviso') == 'sim'
    config["aviso_topo"] = request.form.get('aviso_topo')
    salvar_config(config)
    return redirect(f'/admin?senha={senha}')

@app.route('/admin/adicionar', methods=['POST'])
def acao_adicionar():
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 401
        
    lista = carregar_mods()
    
    novo_mod = {
        "id": len(lista) + 1,
        "titulo": request.form.get('titulo'),
        "imagem": request.form.get('imagem'),
        "categoria": request.form.get('categoria', 'packs'),
        "desc": request.form.get('desc'),
        "link": request.form.get('link'),
        "downloads": 0
    }
    
    lista.append(novo_mod)
    salvar_mods(lista)
    return redirect(f'/admin?senha={senha}')

@app.route('/admin/excluir/<int:mod_id>', methods=['POST'])
def acao_excluir(mod_id):
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 401
        
    lista = carregar_mods()
    lista_atualizada = [m for m in lista if m['id'] != mod_id]
    salvar_mods(lista_atualizada)
    return redirect(f'/admin?senha={senha}')

@app.route('/admin/manutencao', methods=['POST'])
def acao_manutencao():
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 401
        
    config = carregar_config()
    config["manutencao_ativa"] = not config["manutencao_ativa"]
    salvar_config(config)
    return redirect(f'/admin?senha={senha}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)








