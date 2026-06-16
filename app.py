import json
import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Configurações do sistema
SENHA_CORRETA = "adms123321"
BANCO_DADOS = "mods.json"

# --- FUNÇÕES DE DADOS (Persistência) ---
def carregar_mods():
    if not os.path.exists(BANCO_DADOS):
        # Mods iniciais já com os seus links
        mods = [
            {"id": 1, "titulo": "FS23 Mapa Sul do Brasil", "categoria": "Mapas", "link": "https://www.mediafire.com/file/mys6o1lm3cin56w/FS23_MAPA_SUL_DO_BRASIL_CLZIN_MODZ.apk/file"},
            {"id": 2, "titulo": "FS23 Mod Completo BR", "categoria": "Modificações", "link": "https://www.mediafire.com/file/g7egyr6mmqqb3q4/FS23_MODS_%25F0%259F%2587%25A7%25F0%259F%2587%25B7_COMPLET%25C3%2583O.apk/file"}
        ]
        salvar_mods(mods)
        return mods
    with open(BANCO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_mods(dados):
    with open(BANCO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# --- CÓDIGO HTML (Design Premium) ---
HTML_SITE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FS23 Mods Brasil | Premium</title>
    <style>
        :root { --primary: #659b2c; --dark: #0b0e0a; --panel: #131a10; --text: #f4f6f3; }
        body { background-color: var(--dark); color: var(--text); font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; }
        .header { background: var(--panel); padding: 30px; text-align: center; border-bottom: 4px solid var(--primary); }
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .mod-card { background: var(--panel); border: 1px solid #23301c; border-radius: 10px; padding: 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        .mod-info h3 { margin: 0 0 10px 0; color: var(--primary); }
        .btn-down { background: linear-gradient(var(--primary), #4e7822); color: white; padding: 12px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚜 FS23 Mods Brasil</h1>
        <p>Qualidade e procedência para sua fazenda.</p>
    </div>
    <div class="container">
        {% for mod in lista_mods %}
        <div class="mod-card">
            <div class="mod-info">
                <h3>{{ mod.titulo }}</h3>
                <p>Categoria: {{ mod.categoria }}</p>
            </div>
            <a href="/baixar/{{ mod.id }}" class="btn-down">Baixar APK</a>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

# --- ROTAS ---
@app.route('/')
def rota_home():
    return render_template_string(HTML_SITE, lista_mods=carregar_mods())

@app.route('/baixar/<int:mod_id>')
def rota_baixar(mod_id):
    lista = carregar_mods()
    for mod in lista:
        if mod['id'] == mod_id:
            return redirect(mod['link'])
    return "Mod não encontrado", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
