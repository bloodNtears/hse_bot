from telebot import types
import telebot
import os
import json

directory = os.getcwd()
workout_plans_dir = directory + "/workout_plans/"

menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
menu_buttons = [
	types.KeyboardButton("Выбрать упражнение"),
	types.KeyboardButton("Выбрать план"),
	types.KeyboardButton("Составить расписание"),
	types.KeyboardButton("Удалить напоминания")]
menu_markup.add(*menu_buttons)

body_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
body_buttons = [
	types.KeyboardButton("Верх тела"),
	types.KeyboardButton("Низ тела")]
body_markup.add(*body_buttons)

upper_body_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
upper_body_buttons = [
	types.KeyboardButton("Грудь"),
	types.KeyboardButton("Бицепс"),
	types.KeyboardButton("Трицепс"),
	types.KeyboardButton("Плечи"),
	types.KeyboardButton("Спина"),
	types.KeyboardButton("Пресс")]
upper_body_markup.add(*upper_body_buttons)

lower_body_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
lower_body_buttons = [
	types.KeyboardButton("Икры"),
	types.KeyboardButton("Передняя поверхность бедра"),
	types.KeyboardButton("Задняя поверхность бедра"),
	types.KeyboardButton("Ягодицы")]
lower_body_markup.add(*lower_body_buttons)

workout_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
workout_buttons = [
	types.KeyboardButton("2 дня"),
	types.KeyboardButton("3 дня"),
	types.KeyboardButton("4 дня"),
	types.KeyboardButton("5 дней")]
workout_markup.add(*workout_buttons)

schedule_markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
schedule_buttons = [types.KeyboardButton(day) for day in days]
schedule_buttons.append(types.KeyboardButton("Готово✅"))
schedule_markup.add(*schedule_buttons)

reminder_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
reminder_buttons = [
	types.KeyboardButton("Да, за 30 минут"),
	types.KeyboardButton("Да, за 1 час"),
	types.KeyboardButton("Нет")]
reminder_markup.add(*reminder_buttons)

remove_keyboard_markup = types.ReplyKeyboardRemove()

two_days_media = []
with open(workout_plans_dir + "2days.png", 'rb') as photo:
	photo_data = photo.read()
	two_days_media.append(types.InputMediaPhoto(photo_data))

three_days_media_paths = [workout_plans_dir + "3days.png",
						  workout_plans_dir + "3days_1.png",
						  workout_plans_dir + "3days_2.png"]
three_days_media = []
for path in three_days_media_paths:
	with open(path, 'rb') as photo:
		photo_data = photo.read()
		three_days_media.append(types.InputMediaPhoto(photo_data))

four_days_media_paths = [workout_plans_dir + "4days.png",
						 workout_plans_dir + "4days_1.png",
						 workout_plans_dir + "4days_2.png"]
four_days_media = []
for path in four_days_media_paths:
	with open(path, 'rb') as photo:
		photo_data = photo.read()
		four_days_media.append(types.InputMediaPhoto(photo_data))

five_days_media = []
with open(workout_plans_dir + "5days.png", 'rb') as photo:
	photo_data = photo.read()
	five_days_media.append(types.InputMediaPhoto(photo_data))

with open(directory + '/exercises.json', 'r') as f:
	data = json.load(f)


def parse_exercises(exercises):
	exercises_string = ""
	for exercise_name, exercise_url in exercises.items():
		exercises_string += f"{exercise_name}: {exercise_url}\n"
	return exercises_string


upper_body = data['upperBody']
chest_exercises = upper_body['chest']
biceps_exercises = upper_body['biceps']
triceps_exercises = upper_body['triceps']
shoulders_exercises = upper_body['shoulders']
back_exercises = upper_body['back']
abdominals_exercises = upper_body['abdominals']

lower_body = data['lowerBody']
quads_exercises = lower_body['Quads']
hamstrings_exercises = lower_body['Hamstrings']
calves_exercises = lower_body['Calves']
glutes_exercises = lower_body['Glutes']
