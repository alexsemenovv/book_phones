from loguru import logger
import datetime
from database.models import Contact, db
import os
import peewee

commands = ['Вывод контактов по номеру страницы', 'Добавить контакт', 'Изменить контакт', 'Поиск контакта']
logger.add(f'logs/debug.{datetime.datetime.now().date()}.log',
           format="{time} {level} {message}",
           level='DEBUG', rotation='10 MB', compression='zip')


def clear() -> None:
    """
    Функция очистки консоли
    :return: None
    """
    logger.info(f'interface.clear - os.system: {os.system}')
    os.system('cls' if os.name == 'nt' else 'clear')


@logger.catch
def greetings() -> str:
    """Функция здоровается с пользователем, и рассказывает про интерфейс"""
    print(f'\nПриветствую тебя, многоуважаемый пользователь!')
    print('Ниже приведен список команд, которые я умею выполнять:')
    logger.info(f"interface.greetings")
    global commands
    for i, i_command in enumerate(commands, start=1):
        print(f"{i} - {i_command}")
    action = input('Выберите действие: ')
    return action


@logger.catch
def is_valid(number: str) -> bool:
    """
    Функция проверяет номер телефона вводимые пользователем
    :param number: номер который будем проверять
    :return: True или False
    """
    logger.info(f"interface.is_valid - number: {number}")
    if number.startswith('+7'):
        number = number[1:]
    try:
        number = int(number)
        return True
    except ValueError as error:
        logger.error(f'interface.greetings - Ошибка: {error}')
        return False


@logger.catch
def output_all_contacts(num_page: int) -> None:
    """
    Выводит в консоль список контактов в алфавитном порядке. Если их нет - то сообщает об этом.
    :param: num_page: int - номер страницы
    :return: None
    """
    logger.info(f"interface.output_all_contacts")
    if os.path.exists(os.path.abspath(os.path.join('database', 'people.db'))):
        try:
            with db:
                contacts = Contact.select().order_by(Contact.name).paginate(num_page, 10)
                if contacts:
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
                else:
                    print('На этой странице нет контактов.')
        except peewee.OperationalError as error:
            logger.error(f'interface.output_all_contacts - Ошибка: {error}')
            print('В таблице нет контактов')

    else:
        print('Сначала добавьте контакт')


@logger.catch
def search_contact(query: str) -> None:
    """
    Ищет в БД контакты по переданным характеристикам
    :param: query: str - запрос/информацию о искомом контакте
    :return: None
    """
    contacts = Contact.select().where(
        (Contact.name.contains(query)) |
        Contact.personal_phone.contains(query))
    if contacts:
        for i, contact in enumerate(contacts, start=1):
            print("{i})  Имя: {name}\n\tФамилия: {sec_name}\n\t"
                  "Отчество: {patronymic}\n\tОрганизация: "
                  "{company}\n\tРаб.тел.: {work_phone}\n\tЛичный телефон: {phone}".format(
                i=i,
                name=contact.name,
                sec_name=contact.sec_name,
                patronymic=contact.patronymic,
                company=contact.company,
                work_phone=contact.work_phone,
                phone=contact.personal_phone))
    else:
        print('По заданным характеристикам, контактов не найдено')


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
    work_phone = input('Рабочий телефон: ')
    while work_phone:
        if is_valid(work_phone):
            break
        print('Номер телефона может содержать только цифры и знак "+" в начале')
        work_phone = input('Рабочий телефон: ')
    while True:
        personal_phone = input('*Введите личный телефон: ')
        if is_valid(personal_phone):
            break
        print('Номер телефона может содержать только цифры и знак "+" в начале')
    with db:
        db.create_tables([Contact])
        contact_db = Contact.create(
            name=name,
            sec_name=second_name,
            patronymic=patronymic,
            company=company,
            work_phone=work_phone,
            personal_phone=personal_phone
        )
    print(f'Контакт {name} добавлен!')


@logger.catch
def edit_contact(name: str) -> None:
    """
    Ищет контакт в БД. Если находит - то запрашивает у пользователя новые данные.
    :param name: str - имя контакта, который должен быть в БД
    :return: None
    """
    contact = Contact.get_or_none(Contact.name == name)
    if contact:
        print('Если не хотите перезаписывать данные - то жмите Enter')
        contact.name = input(f'Имя [{contact.name}]: ') or contact.name
        contact.sec_name = input(f'Фамилия [{contact.sec_name}]: ') or contact.sec_name
        contact.patronymic = input(f'Отчество [{contact.patronymic}]: ') or contact.patronymic
        contact.company = input(f'Организация [{contact.company}]: ') or contact.company
        while True:
            contact.work_phone = input(f'Раб.тел. [{contact.work_phone}]: ') or contact.work_phone
            if is_valid(contact.work_phone):
                break
            print('Номер телефона может содержать только цифры и знак "+" в начале')
        while True:
            contact.personal_phone = input(f'Личный телефон [{contact.personal_phone}]: ') or contact.personal_phone
            if is_valid(contact.personal_phone):
                break
            print('Номер телефона может содержать только цифры и знак "+" в начале')
        contact.save()
        print(f'Контакт {contact.name} изменён!')
    else:
        print('Контакт не найден!')


@logger.catch
def main() -> None:
    """Главная функция которая запускает приложение"""
    logger.info("interface.main")
    while True:
        num_action = greetings()
        if num_action == '1':
            number_page = int(input('Введите номер страницы: '))
            output_all_contacts(number_page)
        elif num_action == '2':
            add_contact()
        elif num_action == '3':
            name = input('Введите имя контакта, который хотите изменить: ')
            edit_contact(name)
        elif num_action == '4':
            characteristics = input('Введите характеристику(и) для контакта: ')
            search_contact(characteristics)
        else:
            print('Нет такого действия.')
        input('Нажмите ввод для продолжения\n')
        clear()
