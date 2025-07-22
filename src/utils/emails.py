import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader
from src.config import settings
import os


template_dir = settings.mail.templates_path


def render_html(filename: str, **template_args) -> str:
    """
    Рендерит HTML-шаблон с заданными аргументами.
    
    Args:
        filename (str): Имя файла шаблона.
        **template_args: Аргументы для передачи в шаблон.
    
    Returns:
        str: Сгенерированный HTML-контент.
    """
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(filename)
    html_content = template.render(**template_args)

    return html_content


def get_logo(css_class_to_add: str | None) -> str:
    """
    Возвращает содержимое файла logo.svg с добавленным CSS классом, если он указан.
    
    Args:
        css_class_to_add (str | None): CSS класс для добавления к SVG логотипу.
    
    Returns:
        str: Содержимое файла logo.svg с добавленным CSS классом.
    """
    svg_path = os.path.join(template_dir, "logo.svg")
    with open(svg_path, "r", encoding="utf-8") as f:
        logo_svg = f.read()

    if css_class_to_add:
        logo_svg = logo_svg.replace('<svg', f'<svg class=\"{css_class_to_add}\"', 1)
    return logo_svg


async def send_verification_code(
    to_email: str, 
    code: str
) -> bool:
    # Настройка Jinja2
    html_content = render_html(
        filename="verification.html",
        code=code,
        app_name=settings.app.name,
        logo_svg=get_logo(css_class_to_add="logo-svg")
    )

    # Формируем письмо с HTML, plain text и embedded image
    message = MIMEMultipart("related")
    message["From"] = settings.mail.sender
    message["To"] = to_email
    message["Subject"] = f"Ваш код подтверждения {settings.app.name}"

    # Альтернативные части: plain и html
    alt = MIMEMultipart("alternative")
    text_content = f"Введите этот код в iOS приложении: {code}"
    alt.attach(MIMEText(text_content, "plain", "utf-8"))
    alt.attach(MIMEText(html_content, "html", "utf-8"))
    message.attach(alt)

    try:
        async with aiosmtplib.SMTP(
            hostname=settings.mail.hostname,
            port=settings.mail.port,
            username=settings.mail.sender,
            password=settings.mail.password,
            use_tls=True
        ) as client:
            await client.send_message(message)
            print("email успешно отправлен")
            return True
    except Exception as e:
        print(f"SMTP error: {e}")
        return False
