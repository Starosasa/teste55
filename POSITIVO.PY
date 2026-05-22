# -*- coding: utf-8 -*-
"""
Sistema com formulário e galeria de cards (blocos)
- Campos: nome, modelo, OSS, marca, data
- Após cadastrar, vai direto para a galeria
- Cards com borda arredondada e sombra
"""

import json
import os
from pywebio import start_server
from pywebio.input import input, input_group, DATE
from pywebio.output import put_markdown, put_button, clear, put_text, put_row, put_scope, use_scope

ARQUIVO = "cadastros.json"

def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def galeria():
    """Exibe os cadastros como cards em grade"""
    clear()
    put_markdown("## 🖼️ Galeria de Cadastros")
    cadastros = carregar_dados()
    if not cadastros:
        put_text("📭 Nenhum cadastro ainda.")
        put_button("➕ Novo Cadastro", onclick=cadastrar)
        return
    
    # Exibir cards em linhas de 2
    linha_cards = []
    for i, c in enumerate(cadastros):
        # Cria um container para cada card (usamos put_scope para organizar)
        nome_scope = f"card_{i}"
        put_scope(nome_scope)
        with use_scope(nome_scope):
            # HTML/CSS inline para o card
            put_markdown(f"""
            <div style="border:1px solid #ddd; border-radius:12px; padding:12px; margin:8px;
                        background:white; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                <div style="font-size:1.2em; font-weight:bold;">👤 {c['nome']}</div>
                <div>📦 Modelo: {c['modelo']}</div>
                <div>🏷️ Marca: {c['marca']}</div>
                <div>🆔 OSS: {c['oss']}</div>
                <div>📅 Data: {c['data']}</div>
            </div>
            """, raw=True)
        linha_cards.append(nome_scope)
        if len(linha_cards) == 2:
            put_row(linha_cards)
            linha_cards = []
    if linha_cards:
        put_row(linha_cards)
    
    put_button("➕ Novo Cadastro", onclick=cadastrar)

def cadastrar():
    """Formulário de cadastro - após salvar, vai para galeria"""
    clear()
    put_markdown("## 📝 Novo Cadastro")
    dados_form = input_group("Preencha os campos", [
        input("Nome completo", name="nome", required=True),
        input("Modelo", name="modelo", required=True),
        input("OSS (Ordem de Serviço)", name="oss", required=True),
        input("Marca", name="marca", required=True),
        input("Data", name="data", type=DATE, required=True)
    ])
    cadastros = carregar_dados()
    cadastros.append(dados_form)
    salvar_dados(cadastros)
    # Vai direto para a galeria após salvar
    galeria()

def menu():
    clear()
    put_markdown("# 🚀 Sistema de Cadastros")
    put_markdown("### Escolha uma opção:")
    put_button("📝 Cadastrar", onclick=cadastrar)
    put_button("🖼️ Ver Galeria", onclick=galeria)

if __name__ == "__main__":
    start_server(menu, port=8080, debug=True)