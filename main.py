"""
Smart Price Tracker - Menu principal interativo.
"""

import os
import sys

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from app.database import (
    initialize_database, add_product, list_products,
    get_product_by_id, delete_product, save_price_log,
    get_price_history, get_lowest_price
)
from app.scraper import scrape_product
from app.notifier import check_price_alert, format_price_change
from app.reporter import generate_html_report, generate_csv_report

console = Console()


def show_header():
    console.print(Panel.fit(
        "[bold cyan]>>> Smart Price Tracker <<<[/bold cyan]\n"
        "[dim]Monitoramento de precos em e-commerces[/dim]",
        border_style="cyan"
    ))


def show_menu():
    console.print("\n[bold]O que deseja fazer?[/bold]")
    console.print("  [cyan]1[/cyan] - Adicionar produto para monitorar")
    console.print("  [cyan]2[/cyan] - Listar produtos cadastrados")
    console.print("  [cyan]3[/cyan] - Verificar preços agora (scraping)")
    console.print("  [cyan]4[/cyan] - Ver histórico de um produto")
    console.print("  [cyan]5[/cyan] - Gerar relatório HTML")
    console.print("  [cyan]6[/cyan] - Exportar relatório CSV")
    console.print("  [cyan]7[/cyan] - Remover produto")
    console.print("  [cyan]0[/cyan] - Sair")
    return Prompt.ask("\n[bold cyan]Escolha uma opção[/bold cyan]", default="0")


def cmd_add_product():
    console.print("\n[bold]➕ Adicionar Produto[/bold]")
    name = Prompt.ask("Nome do produto")
    url = Prompt.ask("URL do produto (link do site)")
    target_str = Prompt.ask("Preço-alvo para alerta (R$, deixe vazio para pular)", default="")

    target_price = None
    if target_str.strip():
        try:
            target_price = float(target_str.replace(",", "."))
        except ValueError:
            rprint("[red]Valor inválido, preço-alvo ignorado.[/red]")

    product = add_product(name=name, url=url, target_price=target_price)
    rprint(f"[green]✅ Produto '[bold]{product.name}[/bold]' cadastrado com ID {product.id}![/green]")


def cmd_list_products():
    products = list_products()
    if not products:
        rprint("[yellow]Nenhum produto cadastrado ainda.[/yellow]")
        return

    table = Table(title="📦 Produtos Monitorados", border_style="cyan")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("Nome", style="bold white")
    table.add_column("Preço Alvo", style="green")
    table.add_column("URL", style="dim", max_width=50)

    for p in products:
        target = f"R$ {p.target_price:.2f}" if p.target_price else "-"
        table.add_row(str(p.id), p.name, target, p.url)

    console.print(table)


def cmd_run_scraping():
    products = list_products()
    if not products:
        rprint("[yellow]Nenhum produto cadastrado. Adicione um produto primeiro.[/yellow]")
        return

    console.print(f"\n[bold]🔍 Verificando preços de {len(products)} produto(s)...[/bold]\n")

    alerts = []
    for product in products:
        console.print(f"  🌐 Coletando: [cyan]{product.name}[/cyan]...", end=" ")

        # Pega o último preço registrado para comparação
        history = get_price_history(product.id)
        last_price = history[0].price if history else None
        lowest = get_lowest_price(product.id)

        price, availability = scrape_product(product.url)
        log = save_price_log(product.id, price, availability)

        price_str = f"R$ {price:.2f}" if price else "N/A"
        change_str = format_price_change(last_price, price) if last_price else ""

        status_color = "green" if availability == "Disponível" else "red"
        console.print(
            f"[{status_color}]{price_str}[/{status_color}] | "
            f"{availability} {change_str}"
        )

        # Verifica alertas
        alert = check_price_alert(product, price, lowest)
        if alert:
            alerts.append(alert)

    if alerts:
        console.print()
        for alert in alerts:
            rprint(f"[bold yellow]{alert}[/bold yellow]")
    else:
        console.print("\n[dim]Nenhum alerta de desconto detectado.[/dim]")


def cmd_view_history():
    products = list_products()
    if not products:
        rprint("[yellow]Nenhum produto cadastrado.[/yellow]")
        return

    cmd_list_products()
    product_id_str = Prompt.ask("\nDigite o ID do produto para ver o histórico")
    try:
        product_id = int(product_id_str)
    except ValueError:
        rprint("[red]ID inválido.[/red]")
        return

    product = get_product_by_id(product_id)
    if not product:
        rprint(f"[red]Produto com ID {product_id} não encontrado.[/red]")
        return

    history = get_price_history(product_id)
    if not history:
        rprint("[yellow]Nenhum histórico de preço registrado para este produto.[/yellow]")
        return

    table = Table(title=f"📊 Histórico de preços: {product.name}", border_style="cyan")
    table.add_column("Data/Hora", style="dim")
    table.add_column("Preço", style="bold cyan")
    table.add_column("Disponibilidade")

    for log in history:
        price_str = f"R$ {log.price:.2f}" if log.price else "N/A"
        avail_style = "green" if log.availability == "Disponível" else "red"
        table.add_row(
            log.scraped_at.strftime("%d/%m/%Y %H:%M:%S"),
            price_str,
            f"[{avail_style}]{log.availability}[/{avail_style}]"
        )

    console.print(table)

    prices = [log.price for log in history if log.price]
    if prices:
        rprint(f"  🟢 Menor preço: [green]R$ {min(prices):.2f}[/green]")
        rprint(f"  🔴 Maior preço: [red]R$ {max(prices):.2f}[/red]")


def cmd_generate_html():
    console.print("\n[bold]📄 Gerando relatório HTML...[/bold]")
    filepath = generate_html_report()
    rprint(f"[green]✅ Relatório gerado em: [bold]{filepath}[/bold][/green]")
    if Confirm.ask("Abrir o relatório no navegador?"):
        os.startfile(filepath)


def cmd_generate_csv():
    console.print("\n[bold]📊 Exportando CSV...[/bold]")
    filepath = generate_csv_report()
    rprint(f"[green]✅ CSV exportado em: [bold]{filepath}[/bold][/green]")


def cmd_remove_product():
    products = list_products()
    if not products:
        rprint("[yellow]Nenhum produto cadastrado.[/yellow]")
        return

    cmd_list_products()
    product_id_str = Prompt.ask("\nDigite o ID do produto para remover")
    try:
        product_id = int(product_id_str)
    except ValueError:
        rprint("[red]ID inválido.[/red]")
        return

    product = get_product_by_id(product_id)
    if not product:
        rprint(f"[red]Produto com ID {product_id} não encontrado.[/red]")
        return

    if Confirm.ask(f"[red]Confirma a remoção de '[bold]{product.name}[/bold]' e todo o seu histórico?[/red]"):
        delete_product(product_id)
        rprint(f"[green]✅ Produto removido com sucesso![/green]")
    else:
        rprint("[dim]Operação cancelada.[/dim]")


def main():
    initialize_database()
    show_header()

    while True:
        try:
            choice = show_menu()
            if choice == "1":
                cmd_add_product()
            elif choice == "2":
                cmd_list_products()
            elif choice == "3":
                cmd_run_scraping()
            elif choice == "4":
                cmd_view_history()
            elif choice == "5":
                cmd_generate_html()
            elif choice == "6":
                cmd_generate_csv()
            elif choice == "7":
                cmd_remove_product()
            elif choice == "0":
                rprint("\n[cyan]Até logo! 👋[/cyan]\n")
                sys.exit(0)
            else:
                rprint("[red]Opção inválida. Tente novamente.[/red]")
        except KeyboardInterrupt:
            rprint("\n\n[cyan]Até logo! 👋[/cyan]\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
