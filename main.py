import re
import ipaddress

def extract_path(input_string):
    """
    Извлекает путь из входной строки.

    Паттерн для поиска пути: '--path.settings <путь>'

    :param input_string: Входная строка для анализа
    :return: Извлеченный путь или None, если не найдено
    """
    pattern = r'--path\.settings\s*((?:"[^"]*"|[^"\s]+)(?:\s+[^\s]+)*|"[^"]*")'
    match = re.search(pattern, input_string)
    
    if match:
        # Удаляем пробелы в конце
        path = match.group(1).rstrip() 
        # Удаляем кавычки (одинарные и двойные)
        path = re.sub(r'[\'"\']', '', path)
        # Удаляем всё после пути
        path = re.sub(r'\s*--.*$', '', path)
        # Заменяем экранированные обратные слэши на обычные
        path = path.replace('\\\\', '\\')
        
        return path
    
    return None

def extract_bind_addresses(config):
    """
    Извлекает адреса для привязки из конфигурационного файла.

    :param config: Конфигурационный файл для анализа
    :return: Список извлеченных адресов
    """
    pattern = r'bind\s+((?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{1,5})?|ipv4@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{1,5})?|ipv6@[a-fA-F0-9:]+|2a00:[a-fA-F0-9:]+)(?:,\s*(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{1,5})?|ipv4@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{1,5})?|ipv6@[a-fA-F0-9:]+|2a00:[a-fA-F0-9:]+))*)\b'

    bind_addresses = re.findall(pattern, config)
    # Разбиваем адреса кавычками
    separated_addresses = [address.split(',') for address in bind_addresses]
    return [item for sublist in separated_addresses for item in sublist]


def create_collection(bind_addresses):
    """
    Создает коллекцию из извлеченных адресов привязки.

    :param bind_addresses: Список адресов привязки
    :return: Список словарей с информацией о каждом адресе
    """
    result = []
    
    for address in bind_addresses:
        ip, separator, port = address.rpartition(':')
        assert separator  # разделитель (:) должен присутствовать
        port = int(port)  # преобразуем в целое число
        
        # Удаляем префиксы ipv4@ или ipv6@
        if ip.startswith('ipv4@') or ip.startswith('ipv6@'):
            ip = ip[5:]
        
        # Проверяем, пуст ли IP
        if not ip:
            ip = '::' if 'ipv6' in address else '0.0.0.0'
        # Преобразуем в IPv4Address или IPv6Address
        ip = ipaddress.ip_address(ip.strip("[]"))  
        # Подгоняем версию по требованию
        ip_version = 'ipv6' if ip.version == 6 else 'ipv4'
        # Создаем коллекцию
        collection = {
            'IP': str(ip),
            'Type': ip_version,
            'Port': port
        }
        
        result.append(collection)
    
    return result