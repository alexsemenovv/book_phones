from loguru import logger
import datetime
from database import models
import os
import peewee

commands = ['Вывод всех контактов', 'Вывод контактов по номеру страницы', 'Поиск', 'Добавить контакт',
            'Изменить контакт', 'Удалить контакт', 'Остановить приложение']
logger.add(f'logs/debug.{datetime.datetime.now().date()}.log',
           format="{time} {level} {message}",
           level='DEBUG', rotation='10 MB', compression='zip')


@logger.catch
def greetings() -> str:
    """Функция здоровается с пользователем, и рассказывает про интерфейс"""
    print(f'\nПриветствую тебя, многоуважаемый пользователь!')
    print('Ниже приведен список команд, которые я умею выполнять:')
    logger.info(f"interface.greetings")
    global commands
    for i, i_command in enumerate(commands, start=1):
        print(f"{i} - {i_command}")
    while True:
        action = input('Выберите действие: ')
        if is_valid('greetings', action):
            return action


@logger.catch
def is_valid(flag: str, number: str) -> bool:
    """
    Функция проверяет данные вводимые пользователем
    :param number: номер который будем проверять
    :param flag: для какой функции(greetings, add_contact)
    :return:
        greetings
            True - если введено число в диапазоне длины списка команд;
            False - в противном случае
        add_contact
            True - если номер телефона состоит только из цифр, и если их кол-во равно 11
            False - в противном случае"""
    logger.info(f"interface.is_valid - flag: {flag}, number: {number}")
    global commands
    if flag == 'greetings':
        try:
            if int(number) not in range(1, len(commands) + 1):
                raise IndexError('Number out of range')
            return True
        except ValueError as error:
            logger.error(f'interface.greetings - Ошибка: {error}')
            print('Значение должно быть числом. Попробуйте снова!')
            return False
        except IndexError as error:
            logger.error(f'interface.greetings - Ошибка: {error}')
            print(f'Значение должно быть в диапазоне от 1 до {len(commands)}. Попробуйте снова!')
            return False
    else:
        if not number.isdigit() and number:
            print('Телефон должен содержать только цифры!')
            return False
        elif len(number) != 11 and number:
            print('Количество цифр в номере должно быть равным 11')
            return False
        else:
            return True


@logger.catch
def output_all_contacts() -> None:
    """
    Выводит в консоль список контактов в алфавитном порядке. Если их нет - то сообщает об этом.
    :return: None
    """
    logger.info(f"interface.output_all_contacts")
    if os.path.exists(os.path.abspath(os.path.join('database', 'people.db'))):
        try:
            with models.db:
                contacts = models.Contact.select().order_by(models.Contact.name)
                for id_contact, contact in enumerate(contacts, start=1):
                    print("{id})  Имя: {name}\n\tФамилия: {sec_name}\n\t"
                          "Отчество: {patronymic}\n\tОрганизация: "
                          "{company}\n\tРаб.тел.: {work_phone}\n\tЛичный телефон: {phone}".format(
                        id=id_contact,
                        name=contact.name,
                        sec_name=contact.sec_name,
                        patronymic=contact.patronymic,
                        company=contact.company,
                        work_phone=contact.work_phone,
                        phone=contact.personal_phone))
        except peewee.OperationalError as error:
            logger.error(f'interface.output_all_contacts - Ошибка: {error}')
            print('В таблице нет контактов')

    else:
        print('Сначала добавьте контакт')



@logger.catch
def output_contacts_by_page_number() -> None:
    logger.info('interface.output_contacts_by_page_number')


@logger.catch
def find_contact() -> None:
    name = input('Введите имя контакта: ')
    try:
        found_contact = models.Contact.select().where(peewee.fn.Lower(models.Contact.name) == name) #если здесь добавить .lower - то вообще ничего не находит. А так находит  только если так же имя указать как в бд
        if found_contact:
            for contact in found_contact:
                print(contact.name, contact.personal_phone)
        else:
            print('Контакт не найден')
    except Exception as error:
        logger.error(f'interface.find_contact - Ошибка: {error}')
        print('Произошла ошибка при поиске контакта')





@logger.catch
def add_contact() -> None:
    """
    Добавляет контакт в базу данных
    :return: None
    """
    logger.info('interface.add_contact')
    print('Поля отмеченные * - обязательные для заполнения')
    while True:
        name = input('\n*Введите имя: ')
        if name:
            break
    second_name = input('Введите фамилию: ')
    patronymic = input('Введите отчество: ')
    company = input('Название организации: ')
    while True:
        work_phone = input('Введите рабочий телефон начинающийся на "8": ')
        if is_valid('add_contact', work_phone):
            break
    while True:
        personal_phone = input('*Введите личный телефон начинающийся на "8": ')
        if is_valid('add_contact', personal_phone):
            break
    with models.db:
        models.db.create_tables([models.Contact])
        contact_db = models.Contact.create(
            name=name,
            sec_name=second_name,
            patronymic=patronymic,
            company=company,
            work_phone=work_phone,
            personal_phone=personal_phone
        )
    print('Контакт добавлен!')

@logger.catch
def editing() -> None:
    pass


@logger.catch
def delete_contact() -> None:
    pass


@logger.catch
def main() -> None:
    """Главная функция которая запускает приложение"""
    logger.info("interface.main")
    is_work = True
    while is_work:
        num_action = greetings()
        if num_action == '1':
            output_all_contacts()
        elif num_action == '2':
            pass
        elif num_action == '3':
            find_contact()
        elif num_action == '4':
            add_contact()
        elif num_action == '5':
            pass
        elif num_action == '6':
            pass
        elif num_action == '7':
            is_work = False
        input('Нажмите ввод для продолжения\n')