#!/usr/bin/env python3
"""
🚀 CALCULADORA INFLAÇÃO & IMPOSTOS - PYTHON PURO
💰 Funciona SEM INSTALAÇÕES no VSCode Terminal
"""

import datetime
import math

# 🗄️ DADOS IPCA REAL IBGE (2006-2024)
IPCA = {
    2006: 3.14, 2007: 4.46, 2008: 5.90, 2009: 4.31, 2010: 5.91,
    2011: 6.50, 2012: 5.84, 2013: 5.91, 2014: 6.41, 2015: 10.67,
    2016: 6.29, 2017: 2.95, 2018: 3.75, 2019: 4.31, 2020: 4.52,
    2021: 10.06, 2022: 5.79, 2023: 4.62, 2024: 4.50
}

# 📊 TABELA IRPF + INSS 2024
TABELA_IRPF = [
    (0, 24999.99, 0.00, 0),
    (25000, 34999.99, 0.075, 1874),
    (35000, 43999.99, 0.15, 4123.50),
    (44000, 54999.99, 0.225, 7289.25),
    (55000, float('inf'), 0.275, 10154.75)
]

def limpar_tela():
    print("\033c", end="")

def banner():
    print("=" * 70)
    print("🚀 CALCULADORA INFLAÇÃO & IMPOSTOS 2024")
    print("📊 IPCA IBGE 2006-2024 | IRPF + INSS Completo")
    print("=" * 70)

def calcular_ipca_periodo(ano_inicio, ano_fim):
    """🧮 IPCA acumulado entre anos"""
    if ano_inicio not in IPCA or ano_fim not in IPCA:
        return 0.0
    
    fator = 1.0
    for ano in range(ano_inicio, ano_fim + 1):
        fator *= (1 + IPCA[ano] / 100)
    return (fator - 1) * 100

def corrigir_inflacao(valor, ano_inicio, ano_fim):
    """💹 Corrige valor por IPCA"""
    ipca_total = calcular_ipca_periodo(ano_inicio, ano_fim)
    fator = 1 + ipca_total / 100
    valor_corrigido = valor * fator
    return valor, valor_corrigido, ipca_total, fator

def calcular_inss(salario):
    """💳 INSS 2024"""
    if salario <= 1412:
        return salario * 0.075
    elif salario <= 2666.68:
        return salario * 0.09
    elif salario <= 4000.03:
        return salario * 0.12
    elif salario <= 7789.02:
        return salario * 0.14
    return 908.85  # Teto

def calcular_irpf(base):
    """📈 IRPF 2024"""
    for min_val, max_val, aliq, deduz in TABELA_IRPF:
        if min_val <= base < max_val:
            return max(0, (base * aliq) - deduz)
    return 0

def holerite_completo(salario):
    """💼 Holerite IRPF + INSS"""
    inss = calcular_inss(salario)
    base_ir = salario - inss
    irpf = calcular_irpf(base_ir)
    liquido = salario - inss - irpf
    return salario, inss, base_ir, irpf, liquido

def mostrar_historico_ipca():
    """📊 Tabela IPCA"""
    print("\n📊 HISTÓRICO IPCA 2006-2024")
    print("-" * 40)
    print(f"{'ANO':<6} {'IPCA':>6}")
    print("-" * 40)
    for ano in sorted(IPCA.keys()):
        print(f"{ano:<6} {IPCA[ano]:>5.2f}%")
    
    total = sum(IPCA.values())
    media = total / len(IPCA)
    print("-" * 40)
    print(f"MÉDIA:     {media:5.2f}%")
    print(f"MÁXIMA:    {max(IPCA.values()):5.2f}% (2015)")
    print(f"MÍNIMA:    {min(IPCA.values()):5.2f}% (2017)")
    print(f"TOTAL ACUM: {total:5.1f}%")
    poder_compra = 1000 * math.prod([1 + v/100 for v in IPCA.values()])
    print(f"R$1k 2006 = R${poder_compra:,.0f} hoje")

def menu_principal():
    while True:
        limpar_tela()
        banner()
        print("\n📋 OPÇÕES:")
        print("1️⃣  Inflação IPCA (corrigir valor)")
        print("2️⃣  Imposto IRPF + INSS")
        print("3️⃣  Histórico IPCA completo")
        print("4️⃣  Poder de compra R$1.000")
        print("0️⃣  Sair")
        
        op = input("\n🎯 Escolha: ").strip()
        
        if op == "1":
            valor = float(input("💰 Valor (R$): ") or 1000)
            ano_i = int(input("📅 Ano início (2006-2024): ") or 2010)
            ano_f = int(input("📅 Ano final: ") or 2024)
            
            v1, v2, ipca, fator = corrigir_inflacao(valor, ano_i, ano_f)
            print(f"\n🎯 RESULTADO:")
            print(f"💰 R${v1:,.2f} em {ano_i} = R${v2:,.2f} em {ano_f}")
            print(f"📈 IPCA: {ipca:.2f}% (fator x{fator:.4f})")
            input("\n⏸️ Enter...")
            
        elif op == "2":
            salario = float(input("💰 Salário bruto (R$): ") or 5000)
            bruto, inss, base, irpf, liquido = holerite_completo(salario)
            
            print(f"\n💼 HOLERITE R${bruto:,.2f}")
            print("─" * 40)
            print(f"💰 Bruto:      R${bruto:>10,.2f}")
            print(f"🩸 INSS:       R${inss:>10,.2f}")
            print(f"📋 Base IRPF:  R${base:>10,.2f}")
            print(f"📈 IRPF:       R${irpf:>10,.2f}")
            print("─" * 40)
            print(f"💸 **LÍQUIDO:  R${liquido:>10,.2f}**")
            total_imp = inss + irpf
            aliq = (total_imp / bruto) * 100
            print(f"⚠️  Alíquota efetiva: {aliq:.1f}%")
            input("\n⏸️ Enter...")
            
        elif op == "3":
            mostrar_historico_ipca()
            input("\n⏸️ Enter...")
            
        elif op == "4":
            ano = int(input("📅 Ano (2006-2024): ") or 2010)
            _, hoje, ipca, _ = corrigir_inflacao(1000, ano, 2024)
            print(f"\n💪 R$1.000 em {ano} = R${hoje:,.2f} **HOJE**")
            print(f"📈 Inflação acumulada: {ipca:.1f}%")
            input("\n⏸️ Enter...")
            
        elif op == "0":
            print("\n👋 Obrigado por usar!")
            break

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Tchau!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")