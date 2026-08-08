import random, ssl
import flet as ft

# Отключение SSL для стабильной работы сетевого движка
ssl._create_default_https_context = ssl._create_unverified_context


def main(page: ft.Page):
    page.title = "SmartHealth PRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 10

    st = {"c": 2000, "p": "гречка, куриное филе, яйца"}

    db = {
        "куриное филе": 110,
        "гречка": 310,
        "яйца": 155,
        "творог": 120,
        "яблоки": 47,
    }

    # --- Экран 1: Профиль ---
    gen = ft.Dropdown(
        label="Пол",
        options=[ft.dropdown.Option("Муж"), ft.dropdown.Option("Жен")],
        value="Муж",
        width=320,
    )
    w_in, h_in, a_in = (
        ft.TextField(label="Вес (кг)", value="70", width=320),
        ft.TextField(label="Рост (см)", value="175", width=320),
        ft.TextField(label="Возраст", value="25", width=320),
    )
    act = ft.Dropdown(
        label="Активность",
        options=[
            ft.dropdown.Option("Минимум"),
            ft.dropdown.Option("Средняя"),
            ft.dropdown.Option("Высокая"),
        ],
        value="Минимум",
        width=320,
    )
    goal = ft.Dropdown(
        label="Цель",
        options=[
            ft.dropdown.Option("Похудение"),
            ft.dropdown.Option("Баланс"),
            ft.dropdown.Option("Набор массы"),
        ],
        value="Баланс",
        width=320,
    )
    res_c = ft.Text("Суточная норма: -- ккал", size=18, color="green", weight="bold")
    res_b = ft.Text("БЖУ: --г |--г |--г", size=14, color="white", weight="bold")

    def calc_profile(e):
        try:
            w, h, a = float(w_in.value), float(h_in.value), float(a_in.value)
            bmr = (
                10 * w + 6.25 * h - 5 * a + (5 if gen.value == "Муж" else -161)
            )
            m = bmr * {"Минимум": 1.2, "Средняя": 1.55, "Высокая": 1.725}.get(
                act.value, 1.2
            )
            st["c"] = int(
                m
                * {"Похудение": 0.85, "Набор массы": 1.15, "Баланс": 1.0}.get(
                    goal.value, 1.0
                )
            )
            res_c.value = f"Суточная норма: {st['c']} ккал"
            res_b.value = f"Б: {int(st['c']*0.3/4)}г • Ж: {int(st['c']*0.3/9)}г • У: {int(st['c']*0.4/4)}г"
        except:
            res_c.value = "Заполните поля числами!"
        page.update()

    t_prof = ft.Column(
        [
            gen, h_in, w_in, a_in, act, goal,
            ft.ElevatedButton(
                content=ft.Text("РАССЧИТАТЬ КБЖУ", weight="bold"),
                on_click=calc_profile,
                width=320,
                bgcolor="green700"
            ),
            res_c, res_b,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    # --- Экран 2: Рацион ---
    pr_in = ft.TextField(
        label="Продукты через запятую",
        value="гречка, куриное филе, яйца",
        width=320,
    )
    m_cont = ft.Column(spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def gen_menu(e):
        st["p"] = pr_in.value
        m_cont.controls.clear()
        v = [
            p.strip().lower()
            for p in pr_in.value.split(",")
            if p.strip().lower() in db
        ] or ["яйца", "куриное филе", "гречка"]
        for meal, pct in [("Завтрак", 0.35), ("Обед", 0.40), ("Ужин", 0.25)]:
            item = random.choice(v)
            g = int((st["c"] * pct / db[item]) * 100)
            m_cont.controls.append(
                ft.Card(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"{meal}: {item.capitalize()} ({g}г)", weight="bold", color="blue"),
                                ft.Text(f"Всего калорий: {int(db[item]*g/100)}", size=11),
                            ]
                        ),
                        padding=8, width=310
                    )
                )
            )
        page.update()

    t_rat = ft.Column(
        [
            pr_in,
            ft.ElevatedButton(
                content=ft.Text("СОЗДАТЬ МЕНЮ РАЦИОНА", weight="bold"),
                on_click=gen_menu,
                width=320,
                bgcolor="blue700"
            ),
            m_cont,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    # --- Экран 3: Цены Красноярск ---
    p_cont = ft.Column(spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def get_prices(e):
        p_cont.controls.clear()
        items = [p.strip() for p in st["p"].split(",") if p.strip()] or ["курица", "гречка"]
        stores = ["Командор", "Красный Яр", "Пятерочка", "Магнит", "Лента"]
        prices = {s: sum(random.randint(90, 300) for _ in items) for s in stores}
        best = min(prices, key=prices.get)
        for s, total in prices.items():
            win = s == best
            
            # ИСПРАВЛЕНИЕ: Параметр color убран из Card. Вместо этого bgcolor задан в ft.Container
            p_cont.controls.append(
                ft.Card(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"{s} ➔ {total} руб." + (" (ВЫГОДНО!)" if win else ""), weight="bold", color="white" if win else "blue"),
                                ft.Text(f"Корзина Красноярск: {', '.join(items)}", size=10),
                            ]
                        ),
                        padding=8, width=310,
                        bgcolor="green700" if win else "transparent"
                    )
                )
            )
        page.update()

    t_pr = ft.Column(
        [
            ft.Text("Мониторинг цен (Красноярск)", size=14, color="grey"),
            ft.ElevatedButton(
                content=ft.Text("ОБНОВИТЬ ЦЕНЫ СУПЕРМАРКЕТОВ", weight="bold"),
                on_click=get_prices,
                width=320,
                bgcolor="orange700"
            ),
            p_cont,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    # --- НАВИГАЦИЯ И УПРАВЛЕНИЕ ОКНАМИ ---
    screen_container = ft.Container(content=t_prof, padding=10)

    def show_profile(e):
        screen_container.content = t_prof
        page.update()

    def show_ration(e):
        screen_container.content = t_rat
        page.update()

    def show_prices(e):
        screen_container.content = t_pr
        page.update()

    btn_prof = ft.ElevatedButton(content=ft.Text("ПРОФИЛЬ", size=12, weight="bold"), on_click=show_profile, bgcolor="bluegrey")
    btn_ration = ft.ElevatedButton(content=ft.Text("РАЦИОН", size=12, weight="bold"), on_click=show_ration, bgcolor="bluegrey")
    btn_prices = ft.ElevatedButton(content=ft.Text("ЦЕНЫ КРСК", size=12, weight="bold"), on_click=show_prices, bgcolor="bluegrey")

    navigation_row = ft.Row(
        [btn_prof, btn_ration, btn_prices],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    background_img = ft.Image(
        src="https://unsplash.com",
        width=380,
        height=250,
        fit="cover"
    )

    app_content = ft.Column(
        [
            ft.Text("SmartHealth PRO", size=26, weight="bold", color="green"),
            navigation_row,
            ft.Divider(height=10, color="grey"),
            screen_container
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    page.add(
        ft.Column(
            [
                background_img,
                app_content
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=9990, host="0.0.0.0")
