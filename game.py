import tkinter as tk
from tkinter import messagebox

import os, sys

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

SPLASH_IMAGE = resource_path("splash.png")
GAME_BG = resource_path("bg.png")
HERO_IMAGE = resource_path("hero.png")

START_BTN_IMAGE = resource_path("start_btn.png")
CONTINUE_BTN_IMAGE = resource_path("continue_btn.png")
BACK_BTN_IMAGE = resource_path("back_btn.png")
HOME_BTN_IMAGE = resource_path("home_btn.png")
EXIT_BTN_IMAGE = resource_path("exit_btn.png")

WIN_BG_IMAGE = resource_path("win_bg.png")
LOSE_BG_IMAGE = resource_path("lose_bg.png")
#Менять ВОПРОСЫ/СЦЕНАРИИ здесь
# Формат:
# "id": ("текст (можно {name})", [("кнопка", "next_id", очки), ...], "подсказка")
# Финал: переходи на "finish". Если score < 0 — сразу проигрыш.
NODES = {
    "start": (
        "Привет, {name}! Я - Кибергерой.\n\nГотов пройти ситуации по безопасности в интернете?",
        [("Да!", "bank", 0), ("Расскажи правила", "rules", 0)],
        "Если сомневаешься - не спеши и проверяй."
    ),
    "rules": (
        "Правила:\n"
        "1) Читай ситуацию\n"
        "2) Выбирай действие\n"
        "3) Получай очки за безопасность\n\n"
        "Поехали?",
        [("Поехали!", "bank", 0)],
        "Очки — это бонус. Главное - привычки."
    ),

    "bank": (
        "Тебе звонят: «Это банк. Срочно назовите данные карты и код из SMS!»\n\nТвой выбор?",
        [
            ("Назову данные", "bank_bad", -2),
            ("Положу трубку и перезвоню по официальному номеру", "bank_good", 2),
            ("Проигнорирую", "bank_ok", 1),
        ],
        "Банк не просит SMS-коды по телефону."
    ),
    "bank_bad": (
        "Плохо: это мог быть мошенник. Данные нельзя сообщать.",
        [("Дальше", "social", 0)],
        "Никогда не сообщай SMS-коды, PIN, CVV/CVC и пароли."
    ),
    "bank_good": (
        "Отлично! Перезвонить по официальному номеру — правильно.",
        [("Дальше", "social", 0)],
        "Номер бери с карты или официального сайта (набери вручную)."
    ),
    "bank_ok": (
        "Неплохо, но лучше ещё проверить через официальный номер/приложение банка.",
        [("Дальше", "social", 0)],
        "Игнор - лучше, чем довериться. Проверка - ещё лучше."
    ),

    "social": (
        "Незнакомец пишет в соцсети и просит номер телефона и школу/адрес.",
        [
            ("Отправлю — ничего страшного", "social_bad", -2),
            ("Откажу и заблокирую", "social_good", 2),
            ("Проигнорирую", "social_ok", 1),
        ],
        "Личные данные нельзя отправлять незнакомцам."
    ),
    "social_bad": (
        "Опасно. Эти данные могут использовать для спама и взломов.",
        [("Дальше", "password", 0)],
        "Не делись личными данными (телефон, адрес, школа, пароли)."
    ),
    "social_good": (
        "Правильно! Блокировка - отличное решение.",
        [("Дальше", "password", 0)],
        "Если сообщение странное — блок + жалоба."
    ),
    "social_ok": (
        "Нормально. Но лучше ещё и заблокировать.",
        [("Дальше", "password", 0)],
        "Игнор + блок — лучше всего."
    ),

    "password": (
        "Какой пароль выбрать для аккаунта?",
        [
            ("123456", "password_bad", -2),
            ("Имя + дата рождения", "password_bad", -1),
            ("Сложный: буквы+цифры+символы", "password_good", 2),
        ],
        "Пароль должен быть сложным и уникальным."
    ),
    "password_bad": (
        "Такой пароль легко подобрать.",
        [("Дальше", "wifi", 0)],
        "Хороший пароль - длинный и не связан с твоей жизнью."
    ),
    "password_good": (
        "Отлично! Такой пароль сложно взломать.",
        [("Дальше", "wifi", 0)],
        "Лучше: разные пароли для разных сайтов + 2FA."
    ),

    "wifi": (
        "Ты подключился к бесплатному Wi-Fi в кафе/ТЦ.",
        [
            ("Зайду в банк и введу пароль", "wifi_bad", -2),
            ("Буду только смотреть видео", "wifi_ok", 1),
            ("Не буду вводить пароли и проверю HTTPS", "wifi_good", 2),
        ],
        "Открытые сети могут быть опасны."
    ),
    "wifi_bad": (
        "Риск: данные могут перехватить.",
        [("Дальше", "phishing", 0)],
        "В открытом Wi-Fi лучше не вводить важные пароли."
    ),
    "wifi_ok": (
        "Нормально. Но осторожность всё равно важна.",
        [("Дальше", "phishing", 0)],
        "Не входи в важные аккаунты в открытом Wi-Fi."
    ),
    "wifi_good": (
        "Отлично! Так безопаснее.",
        [("Дальше", "phishing", 0)],
        "HTTPS — хорошо, но лучше избегать важных входов."
    ),

    "phishing": (
        "Письмо: «Вы выиграли приз! Срочно перейдите по ссылке и введите данные!»",
        [
            ("Перейду по ссылке", "phishing_bad", -2),
            ("Удалю письмо", "phishing_good", 2),
            ("Проверю отправителя и адрес сайта", "phishing_ok", 1),
        ],
        "Это похоже на фишинг."
    ),
    "phishing_bad": (
        "Ссылка могла украсть твои данные.",
        [("Финиш", "finish", 0)],
        "Не открывай подозрительные ссылки и вложения."
    ),
    "phishing_good": (
        "Отлично! Это безопасное решение.",
        [("Финиш", "finish", 0)],
        "Лучше удалить и не отвечать."
    ),
    "phishing_ok": (
        "Хорошо! Проверка важна.",
        [("Финиш", "finish", 0)],
        "Смотри домен, ошибки в адресе, странные просьбы."
    ),

    "finish": (
        "Финиш!",
        [],
        ""
    ),
}
# ================== КОНЕЦ БЛОКА ВОПРОСОВ ==================

player_name = ""
score = 0
current_id = "start"

root = tk.Tk()
root.title("Кибергерой")
root.geometry("920x540")
root.minsize(920, 540)
root.maxsize(920, 540)

container = tk.Frame(root)
container.pack(fill="both", expand=True)

splash_img = None
bg_img = None
hero_img = None
start_btn_img = None
continue_btn_img = None
back_btn_img = None
home_btn_img = None
exit_btn_img = None
win_bg_img = None
lose_bg_img = None

game_canvas = None
score_label = None
tip_label = None

bubble_rect_id = None
bubble_text_id = None
bubble_hero_id = None

option_btn_widgets = []
option_btn_windows = []


def clear():
    for w in container.winfo_children():
        w.destroy()


def draw_rounded_rect(canvas, x1, y1, x2, y2, r=22, **kwargs):
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def show_result_screen(result: str):
    clear()
    global win_bg_img, lose_bg_img, start_btn_img, exit_btn_img

    canvas = tk.Canvas(container, width=920, height=540, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    if result == "win":
        win_bg_img = tk.PhotoImage(file=WIN_BG_IMAGE)
        canvas.create_image(0, 0, image=win_bg_img, anchor="nw")
    else:
        lose_bg_img = tk.PhotoImage(file=LOSE_BG_IMAGE)
        canvas.create_image(0, 0, image=lose_bg_img, anchor="nw")

    canvas.create_text(
        460, 60,
        text=f"Очки: {score}",
        fill="white",
        font=("Arial", 20, "bold")
    )

    start_btn_img = tk.PhotoImage(file=START_BTN_IMAGE)
    start_lbl = tk.Label(container, image=start_btn_img, bd=0)
    start_lbl.place(relx=0.5, rely=0.82, anchor="center")

    def restart():
        global score, current_id
        score = 0
        current_id = "start"
        show_game_screen()
        render_node()

    start_lbl.bind("<Button-1>", lambda e: restart())

    exit_btn_img = tk.PhotoImage(file=EXIT_BTN_IMAGE)
    exit_lbl = tk.Label(container, image=exit_btn_img, bd=0)
    exit_lbl.place(relx=0.92, rely=0.93, anchor="center")
    exit_lbl.bind("<Button-1>", lambda e: root.destroy())


def show_splash_screen():
    clear()
    global splash_img, start_btn_img

    canvas = tk.Canvas(container, width=920, height=540, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    splash_img = tk.PhotoImage(file=SPLASH_IMAGE)
    canvas.create_image(0, 0, image=splash_img, anchor="nw")

    start_btn_img = tk.PhotoImage(file=START_BTN_IMAGE)
    start_btn = tk.Label(container, image=start_btn_img, bd=0)
    start_btn.place(relx=0.5, rely=0.9, anchor="center")
    start_btn.bind("<Button-1>", lambda e: show_name_screen())


def show_name_screen():
    clear()
    global continue_btn_img, back_btn_img

    frame = tk.Frame(container, bg="#0b1f3a")
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="Введите имя:",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#0b1f3a"
    ).pack(pady=(120, 20))

    name_entry = tk.Entry(
        frame,
        font=("Arial", 18),
        justify="center",
        width=24,
        bg="#132b52",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    name_entry.pack(pady=10)
    name_entry.focus_set()

    def go():
        global player_name, score, current_id
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Имя", "Введите имя")
            return
        player_name = name
        score = 0
        current_id = "start"
        show_game_screen()
        render_node()

    continue_btn_img = tk.PhotoImage(file=CONTINUE_BTN_IMAGE)
    continue_lbl = tk.Label(frame, image=continue_btn_img, bd=0)
    continue_lbl.pack(pady=(20, 14))
    continue_lbl.bind("<Button-1>", lambda e: go())

    back_btn_img = tk.PhotoImage(file=BACK_BTN_IMAGE)
    back_lbl = tk.Label(frame, image=back_btn_img, bd=0)
    back_lbl.pack()
    back_lbl.bind("<Button-1>", lambda e: show_splash_screen())

    root.bind("<Return>", lambda e: go())


def show_game_screen():
    clear()
    root.unbind("<Return>")

    global game_canvas, bg_img, hero_img, score_label, tip_label, home_btn_img, exit_btn_img

    game_canvas = tk.Canvas(container, width=920, height=540, highlightthickness=0)
    game_canvas.pack(fill="both", expand=True)

    bg_img = tk.PhotoImage(file=GAME_BG)
    game_canvas.create_image(0, 0, image=bg_img, anchor="nw")

    hero_img = tk.PhotoImage(file=HERO_IMAGE).subsample(4, 4)

    name_label = tk.Label(container, text=f"Игрок: {player_name}", font=("Arial", 12, "bold"),
                          fg="white", bg="#111827")
    score_label = tk.Label(container, text=f"Очки: {score}", font=("Arial", 12, "bold"),
                           fg="white", bg="#111827")
    game_canvas.create_window(12, 10, anchor="nw", window=name_label)
    game_canvas.create_window(920 - 12, 10, anchor="ne", window=score_label)

    tip_label = tk.Label(container, text="", wraplength=260, justify="left",
                         font=("Arial", 11), fg="white", bg="#111827")
    game_canvas.create_window(12, 500, anchor="sw", window=tip_label)

    home_btn_img = tk.PhotoImage(file=HOME_BTN_IMAGE)
    home_lbl = tk.Label(container, image=home_btn_img, bd=0)
    game_canvas.create_window(12, 535, anchor="sw", window=home_lbl)
    home_lbl.bind("<Button-1>", lambda e: show_splash_screen())

    exit_btn_img = tk.PhotoImage(file=EXIT_BTN_IMAGE)
    exit_lbl = tk.Label(container, image=exit_btn_img, bd=0)
    game_canvas.create_window(920 - 12, 535, anchor="se", window=exit_lbl)
    exit_lbl.bind("<Button-1>", lambda e: root.destroy())


def clear_option_buttons():
    global option_btn_widgets, option_btn_windows
    for b in option_btn_widgets:
        try:
            b.destroy()
        except Exception:
            pass
    option_btn_widgets = []
    option_btn_windows = []


def draw_bubble(text: str):
    global bubble_rect_id, bubble_text_id, bubble_hero_id

    x1, y1 = 220, 80
    x2, y2 = 900, 300

    if bubble_rect_id is not None:
        game_canvas.delete(bubble_rect_id)
    if bubble_text_id is not None:
        game_canvas.delete(bubble_text_id)
    if bubble_hero_id is not None:
        game_canvas.delete(bubble_hero_id)

    bubble_rect_id = draw_rounded_rect(
        game_canvas, x1, y1, x2, y2,
        r=22,
        fill="#f7fbff",
        outline="#c7d4e4",
        width=2
    )

    bubble_hero_id = game_canvas.create_image(
        x1 + 20, y1 - 20,
        image=hero_img,
        anchor="nw"
    )

    hero_space = 210
    bubble_text_id = game_canvas.create_text(
        x1 + hero_space, y1 + 18,
        anchor="nw",
        width=(x2 - x1 - hero_space - 18),
        text=text.replace("{name}", player_name),
        font=("Arial", 14),
        fill="#1d2a39"
    )


def choose(next_id: str, pts: int):
    global current_id, score
    score += pts

    if score < 0:
        show_result_screen("lose")
        return

    if next_id == "finish":
        show_result_screen("win" if score > 0 else "lose")
        return

    current_id = next_id
    render_node()


def render_node():
    text, options, tip = NODES[current_id]

    score_label.config(text=f"Очки: {score}")
    tip_label.config(text=tip or "")

    draw_bubble(text)

    clear_option_buttons()

    btn_x, btn_y = 220, 320
    btn_w, btn_h, gap = 680, 36, 10

    for i, (btn_text, next_id, pts) in enumerate(options):
        b = tk.Button(
            container,
            text=btn_text,
            font=("Arial", 12),
            wraplength=650,
            justify="left",
            anchor="w",
            command=lambda n=next_id, p=pts: choose(n, p)
        )
        option_btn_widgets.append(b)
        option_btn_windows.append(
            game_canvas.create_window(
                btn_x, btn_y + i * (btn_h + gap),
                anchor="nw",
                window=b,
                width=btn_w,
                height=btn_h
            )
        )


show_splash_screen()
root.mainloop()
