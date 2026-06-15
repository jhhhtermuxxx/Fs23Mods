import json
import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Configurações do sistema
SENHA_CORRETA = "adms123321"
BANCO_DADOS = "mods.json"

# Variável global do Modo Manutenção
manutencao_ativa = False

# Função para ler os mods do arquivo JSON
def carregar_mods():
    if not os.path.exists(BANCO_DADOS):
        # Se o arquivo não existir, cria um com os seus 4 mods iniciais
        mods_iniciais = [
            {"id": 1, "titulo": "FS23 Jatobá e Nova Fantinati", "imagem": "MAPA JATOBÁ & FANTINATI", "desc": "Incrível modificação unindo os mapas Jatobá e Nova Fantinati.", "link": "https://www.mediafire.com/..."},
            {"id": 2, "titulo": "FS23 Três Lagoas BR", "imagem": "MAPA TRÊS LAGOAS 🇧🇷", "desc": "Sinta a experiência de cultivar no mapa de Três Lagoas.", "link": "https://www.mediafire.com/..."},
            {"id": 3, "titulo": "FS23 Mods Completão", "imagem": "PACK COMPLETÃO BR 🚜", "desc": "O pacote definitivo! Esse APK traz diversas modificações.", "link": "https://www.mediafire.com/..."},
            {"id": 4, "titulo": "Bacuri + PR Oeste V2", "imagem": "BACURI + PR OESTE V2", "desc": "Versão atualizada V2 combinando as regiões de Bacuri.", "link": "https://www.mediafire.com/..."}
        ]
        salvar_mods(mods_iniciais)
        return mods_iniciais
        
    with open(BANCO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

# Função para salvar os mods no arquivo JSON
def salvar_mods(dados):
    with open(BANCO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# --- HTML DO SEU SITE (Modificado para Python ler os dados) ---
HTML_SITE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FS23 Mods Brasileiros</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #121611; color: #e0e0e0; margin: 0; padding: 0; }
        header { background-color: #1b2418; text-align: center; padding: 40px 20px; border-bottom: 4px solid #5c8a27; }
        header h1 { margin: 0; color: #7ca942; font-size: 2.5rem; text-transform: uppercase; }
        header p { margin: 10px 0 0 0; color: #a0a0a0; font-size: 1.1rem; }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
        .mod-card { background-color: #1a2018; border: 1px solid #2d3629; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }
        .mod-image { width: 100%; height: 180px; object-fit: cover; background: linear-gradient(135deg, #2e3d26, #141a11); display: flex; align-items: center; justify-content: center; color: #7ca942; font-weight: bold; font-size: 1.2rem; text-align: center;}
        .mod-info { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .mod-title { font-size: 1.3rem; margin: 0 0 10px 0; color: #ffffff; }
        .mod-desc { font-size: 0.9rem; color: #b0b0b0; line-height: 1.5; margin-bottom: 20px; }
        .btn-download { display: block; text-align: center; background-color: #0070f3; color: #fff; text-decoration: none; padding: 12px; border-radius: 6px; font-weight: bold; text-transform: uppercase; }
    </style>
</head>
<body>
    <header>
        <h1>FS23 MODS BRASIL</h1>
        <p>Baixe os melhores mapas e modificações modificadas (APK)</p>
    </header>

    <div class="container">
        {% for mod in lista_mods %}
        <div class="mod-card">
            <div class="mod-image">{{ mod.imagem }}</div>
            <div class="mod-info">
                <h2 class="mod-title">{{ mod.titulo }}</h2>
                <p class="mod-desc">{{ mod.desc }}</p>
                <a href="{{ mod.link }}" target="_blank" class="btn-download">Baixar via Mediafire</a>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

# --- HTML DO PAINEL ADMIN ---
HTML_ADMIN = '''
<!DOCTYPE html>
<html>
<head>
    <title>Painel Admin - FS23</title>
    <style>
        body { font-family: Arial, sans-serif; background: #222; color: #fff; padding: 20px; }
        .bloco { background: #333; padding: 15px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #444; }
        input, select, textarea { width: 95%; padding: 8px; margin: 5px 0; background: #444; color: #fff; border: 1px solid #555; }
        button { background: #5c8a27; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #555; padding: 8px; text-align: left; }
        th { background: #444; }
        .btn-excluir { color: #ff6b6b; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Painel de Administração 🚜</h1>
    
    <div class="bloco">
        <h3>📊 Estatísticas Rápidas</h3>
        <p>Total de Mods Ativos: <b>{{ total }}</b></p>
    </div>

    <div class="bloco" style="background-color: #4d3d1a;">
        <h3>⚠️ Controle do Site</h3>
        <p>Modo Manutenção: <b>{% if status %} ATIVADO {% else %} DESATIVADO {% endif %}</b></p>
        <form method="POST" action="/admin/manutencao">
            <input type="hidden" name="senha" value="{{ senha_usada }}">
            <button type="submit" style="background:#d9822b;">Alternar Modo Manutenção</button>
        </form>
    </div>

    <div class="bloco">
        <h3>➕ Cadastrar Novo Mod</h3>
        <form method="POST" action="/admin/adicionar">
            <input type="hidden" name="senha" value="{{ senha_usada }}">
            <input type="text" name="titulo" placeholder="Nome do Mod (Ex: Trator BR)" required>
            <input type="text" name="imagem" placeholder="Texto da Imagem (Ex: TRATOR 123)" required>
            <textarea name="desc" placeholder="Descrição do mod..." required></textarea>
            <input type="text" name="link" placeholder="Link de Download do Mediafire" required>
            <button type="submit">Publicar Mod</button>
        </form>
    </div>

    <div class="bloco">
        <h3>📂 Todos os Mods Cadastrados</h3>
        <table>
            <tr>
                <th>Nome do Mod</th>
                <th>Ações</th>
            </tr>
            {% for mod in lista_mods %}
            <tr>
                <td>{{ mod.titulo }}</td>
                <td>
                    <form method="POST" action="/admin/excluir/{{ mod.id }}" style="display:inline;">
                        <input type="hidden" name="senha" value="{{ senha_usada }}">
                        <button type="submit" style="background:none; border:none; color:#ff6b6b; cursor:pointer; font-weight:bold;">❌ Excluir</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
'''

# --- ROTAS FLASK ---

@app.route('/')
def rota_home():
    if manutencao_ativa:
        return "<body style='background:#121611;color:#fff;text-align:center;padding-top:100px;'><h1>O site está em manutenção!</h1><p>Voltamos em breve com novos mods para o FS23.</p></body>"
    
    lista = carregar_mods()
    return render_template_string(HTML_SITE, lista_mods=lista)


# Rota da Tela de Login / Painel
@app.route('/admin', methods=['GET', 'POST'])
def rota_admin():
    senha_digitada = request.form.get('senha') or request.args.get('senha')
    
    # Se não digitou a senha ou ela está errada, mostra a caixinha de login
    if senha_digitada != SENHA_CORRETA:
        return '''
            <body style="background:#222; color:#fff; font-family:Arial; text-align:center; padding-top:100px;">
                <h2>Acesso Restrito - FS23 Admin</h2>
                <form method="POST" action="/admin">
                    <input type="password" name="senha" placeholder="Digite a senha" style="padding:10px; width:200px;"><br><br>
                    <button type="submit" style="padding:10px 20px; background:#5c8a27; color:#fff; border:none; border-radius:4px;">Entrar</button>
                </form>
                <p style="color:red;">''' + ("Senha incorreta!" if senha_digitada else "") + '''</p>
            </body>
        '''
    
    lista = carregar_mods()
    # CORRIGIDO: Agora calcula o total real de itens cadastrados
    total_mods = len(lista) 
    
    return render_template_string(HTML_ADMIN, lista_mods=lista, total=total_mods, status=manutencao_ativa, senha_usada=senha_digitada)


# Ação: Adicionar Mod
@app.route('/admin/adicionar', methods=['POST'])
def acao_adicionar():
    senha = request.form.get('senha')
    # CORRIGIDO: Adicionado o ":" que faltava no final da linha do if
    if senha != SENHA_CORRETA:
        return "Não autorizado", 401
        
    lista = carregar_mods()
    
    novo_mod = {
        "id": len(lista) + 1,
        "titulo": request.form.get('titulo'),
        "imagem": request.form.get('imagem'),
        "desc": request.form.get('desc'),
        "link": request.form.get('link')
    }
    
    lista.append(novo_mod)
    salvar_mods(lista)
    
    return redirect(f'/admin?senha={senha}')


# Ação: Excluir Mod
@app.route('/admin/excluir/<int:mod_id>', methods=['POST'])
def acao_excluir(mod_id):
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 401
        
    lista = carregar_mods()
    lista_atualizada = [m for m in lista if m['id'] != mod_id]
    salvar_mods(lista_atualizada)
    
    return redirect(f'/admin?senha={senha}')


# Ação: Ligar/Desligar Manutenção
@app.route('/admin/manutencao', methods=['POST'])
def acao_manutencao():
    senha = request.form.get('senha')
    if senha != SENHA_CORRETA:
        return "Não autorizado", 401
        
    global manutencao_ativa
    manutencao_ativa = not manutencao_ativa
    return redirect(f'/admin?senha={senha}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
	

