from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


def find_dejavu_font() -> tuple[str, str]:
	"""Try to find DejaVu Sans fonts in common system locations."""
	possible_paths_regular = [
		"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
		"/usr/local/share/fonts/DejaVuSans.ttf",
		os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"),
	]
	possible_paths_bold = [
		"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
		"/usr/local/share/fonts/DejaVuSans-Bold.ttf",
		os.path.join(os.path.dirname(__file__), "DejaVuSans-Bold.ttf"),
	]

	regular = next((p for p in possible_paths_regular if os.path.exists(p)), None)
	bold = next((p for p in possible_paths_bold if os.path.exists(p)), None)
	return regular, bold


def register_fonts():
	regular, bold = find_dejavu_font()
	if regular:
		pdfmetrics.registerFont(TTFont("DejaVuSans", regular))
	if bold:
		pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", bold))


def build_styles():
	styles = getSampleStyleSheet()

	base_font = "DejaVuSans" if "DejaVuSans" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
	base_bold = "DejaVuSans-Bold" if "DejaVuSans-Bold" in pdfmetrics.getRegisteredFontNames() else base_font

	styles.add(
		ParagraphStyle(
			name="TitleRus",
			fontName=base_bold,
			fontSize=20,
			leading=26,
			spaceAfter=10,
			textColor=colors.HexColor("#0F172A"),
		)
	)
	styles.add(
		ParagraphStyle(
			name="SubtitleRus",
			fontName=base_font,
			fontSize=11,
			leading=16,
			textColor=colors.HexColor("#334155"),
			spaceAfter=12,
		)
	)
	styles.add(
		ParagraphStyle(
			name="H2Rus",
			fontName=base_bold,
			fontSize=14,
			leading=20,
			spaceBefore=14,
			spaceAfter=6,
			textColor=colors.HexColor("#0F172A"),
		)
	)
	styles.add(
		ParagraphStyle(
			name="BodyRus",
			fontName=base_font,
			fontSize=11,
			leading=16,
			spaceAfter=6,
			textColor=colors.HexColor("#0B1220"),
		)
	)
	styles.add(
		ParagraphStyle(
			name="NoteRus",
			fontName=base_font,
			fontSize=10,
			leading=14,
			backColor=colors.HexColor("#F1F5F9"),
			borderColor=colors.HexColor("#CBD5E1"),
			borderWidth=0.5,
			borderPadding=6,
			spaceBefore=8,
			spaceAfter=10,
			textColor=colors.HexColor("#0F172A"),
		)
	)
	styles.add(
		ParagraphStyle(
			name="SmallMuted",
			fontName=base_font,
			fontSize=9,
			leading=13,
			textColor=colors.HexColor("#64748B"),
		)
	)
	styles.add(
		ParagraphStyle(
			name="ListRus",
			fontName=base_font,
			fontSize=11,
			leading=16,
			leftIndent=10,
			spaceBefore=2,
			spaceAfter=2,
		)
	)
	return styles


def header_footer(canvas, doc):
	canvas.saveState()
	width, height = doc.pagesize
	canvas.setStrokeColor(colors.HexColor("#E2E8F0"))
	canvas.setLineWidth(0.5)
	canvas.line(20 * mm, height - 18 * mm, width - 20 * mm, height - 18 * mm)
	canvas.line(20 * mm, 15 * mm, width - 20 * mm, 15 * mm)
	canvas.setFont("DejaVuSans" if "DejaVuSans" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 9)
	canvas.setFillColor(colors.HexColor("#475569"))
	canvas.drawString(20 * mm, height - 14 * mm, "Инструкция: Как узнать свой ID в Telegram")
	canvas.drawRightString(width - 20 * mm, 11 * mm, f"Стр. {doc.page}")
	canvas.restoreState()


def build_document(output_path: str):
	register_fonts()
	styles = build_styles()

	doc = BaseDocTemplate(
		output_path,
		pagesize=A4,
		leftMargin=20 * mm,
		rightMargin=20 * mm,
		topMargin=24 * mm,
		bottomMargin=20 * mm,
	)

	frame = Frame(
		doc.leftMargin,
		doc.bottomMargin,
		doc.width,
		doc.height,
		leftPadding=0,
		rightPadding=0,
		topPadding=0,
		bottomPadding=0,
	)

	doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])

	story = []

	# Title and subtitle
	story.append(Paragraph("Как узнать свой ID в Telegram", styles["TitleRus"]))
	story.append(
		Paragraph(
			"Telegram ID — это уникальный числовой идентификатор вашего аккаунта. Он может понадобиться для настройки ботов, интеграций или обращения в техническую поддержку.",
			styles["SubtitleRus"],
		)
	)

	# Section: Через бота @userinfobot
	story.append(Paragraph("Способ 1. Через бота @userinfobot", styles["H2Rus"]))
	steps_userinfo = [
		"Откройте Telegram на телефоне или компьютере.",
		"В поиске введите <b>@userinfobot</b> и перейдите в чат с ботом.",
		"Нажмите кнопку <b>Start</b> (или отправьте команду <b>/start</b>).",
		"Бот сразу отправит сообщение с вашим <b>User ID</b> — это и есть ваш Telegram ID.",
	]
	story.append(
		ListFlowable(
			[ListItem(Paragraph(item, styles["BodyRus"])) for item in steps_userinfo],
			numbered=True,
			bulletType="1",
			leftIndent=16,
			start="1",
		)
	)
	story.append(Spacer(1, 6))

	# Section: Откройте таблицу (инструкция по заполнению)
	story.append(Paragraph("Способ 2. Откройте таблицу", styles["H2Rus"]))
	story.append(Paragraph("Перейдите по предоставленной ссылке, найдите пустую строку (или строку, выделенную для вас) и внесите данные в соответствующие столбцы.", styles["BodyRus"]))
	story.append(Spacer(1, 4))
	story.append(Paragraph("Важные правила заполнения:", styles["BodyRus"]))
	rules = [
		"<b>ФИО</b> — пишите полностью: Иванов Иван Иванович (без сокращений).",
		"<b>Telegram ID</b> — только цифры (например, 582937102). Не вставляйте <b>@username</b> или ссылки.",
		"<b>Должность</b> — укажите актуальную и официальную.",
	]
	story.append(ListFlowable([ListItem(Paragraph(r, styles["ListRus"])) for r in rules], bulletType="bullet", leftIndent=12))

	# Section: Как будет работать бот
	story.append(Paragraph("Как будет работать бот: пошаговый план внедрения", styles["H2Rus"]))
	story.append(Paragraph("Для плавного и эффективного запуска подключение сотрудников к боту будет происходить в два последовательных этапа. Такой подход позволяет протестировать функционал, собрать обратную связь и затем масштабировать использование.", styles["BodyRus"]))

	# Stage 1
	story.append(Paragraph("Этап 1: Подключение НТО и ЗНТО (тестирование + сбор предложений)", styles["BodyRus"]))
	story.append(Spacer(1, 4))
	story.append(Paragraph("Цели этапа:", styles["BodyRus"]))
	stage1_goals = [
		"Тестировать основные функции бота.",
		"Фиксировать замечания, пожелания и предложения по улучшению.",
	]
	story.append(ListFlowable([ListItem(Paragraph(g, styles["ListRus"])) for g in stage1_goals], bulletType="bullet", leftIndent=12))
	story.append(Spacer(1, 2))
	story.append(Paragraph("Сроки: с 22.09.2025 по 22.10.2025", styles["SmallMuted"]))

	# Stage 2
	story.append(Paragraph("Этап 2: Подключение ЦА", styles["BodyRus"]))
	story.append(Spacer(1, 4))
	story.append(Paragraph("Условия перехода:", styles["BodyRus"]))
	stage2_rules = [
		"Сотрудники, отобранные руководителями и их заместителями.",
		"Только после успешного завершения Этапа 1.",
	]
	story.append(ListFlowable([ListItem(Paragraph(g, styles["ListRus"])) for g in stage2_rules], bulletType="bullet", leftIndent=12))

	# How connection happens
	story.append(Spacer(1, 6))
	story.append(Paragraph("Как происходит подключение:", styles["BodyRus"]))
	connect_steps = [
		"Сотрудник передаёт данные (ФИО, Telegram ID, должность) — например, через таблицу на Яндекс.Диске.",
		"Администратор системы добавляет пользователя в бота.",
	]
	story.append(ListFlowable([ListItem(Paragraph(s, styles["ListRus"])) for s in connect_steps], bulletType="bullet", leftIndent=12))

	# Important notes
	important_notes = [
		"Переход на Этап 2 возможен только после финального одобрения по итогам тестирования.",
		"Все пользователи получают персонализированный доступ — бот знает ФИО и должность каждого.",
		"Поддержка и инструкции доступны на всех этапах.",
	]
	story.append(Spacer(1, 4))
	for note in important_notes:
		story.append(Paragraph(note, styles["NoteRus"]))

	story.append(Spacer(1, 8))
	story.append(Paragraph("Такой подход обеспечит плавный, контролируемый и эффективный запуск без сбоев и перегрузок — с учётом мнений ключевых пользователей и интересов бизнеса.", styles["BodyRus"]))

	# Build
	doc.build(story)


if __name__ == "__main__":
	output = os.path.join(os.path.dirname(__file__), "telegram_id_instruction.pdf")
	build_document(output)
