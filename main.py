import xml.dom.minidom as mn


def get_info(tag, books):
    # список элементов(могли бы быть еще узлы, в нашем случае их нет)
    # дочерних узлов корневого узла 'Book'
    tag_elements = []

    # список значений элементов узлов 'Title'
    nodes_values = []

    # заполнение списка элементов, берем значения из дочернего узла с заданным названием из всех корневых узлов
    for book in books:
        # получение элемента по тегу
        element = book.getElementsByTagName(tag)[0]
        tag_elements.append(element)

    # извлечение значений элементов из дочерних узлов tag
    for element in tag_elements:
        # значеник элемента
        nodes = element.childNodes
        for node in nodes:
            # список значений в этих узлах
            nodes_values.append(node.data.replace('\n', ''))

    return nodes_values


def get_id(books):
    # список атрибутов, то есть ID каждой книги
    attribute_values = []

    # заполнение списка
    for book in books:
        # получение атрибута каждого корневого узла
        attribute = book.getAttribute('id')
        attribute_values.append(attribute)

    return attribute_values


def main(file):
    #считывание файла, список корневых узлов 'Book', в которых хранятся другие узлы
    books = mn.parse(file).getElementsByTagName('Book')

    title_val = get_info('Title', books)
    publish_val = get_info('Publisher', books)
    eans_val = get_info('EAN', books)
    isbn_val = get_info('ISBN', books)
    ath_val = get_info('Author', books)
    print_val = get_info('Printing', books)
    yr_of_publish_val = get_info('Year_of_publishing', books)
    format_val = get_info('Format', books)
    price_val = get_info('Price', books)
    id_val = get_id(books)

    ath_val.insert(title_val.index('Послушные вещи'), 'Неизвестно')
    ath_val.insert(title_val.index('Послушные вещи') + 1, 'Неизвестно')

    print('Какую задачу нужно сделать?')
    print('Введите:', '\n', '1, если нужно узнать информацию по ID книги',
          '\n', '2, если нужно узнать информацию по ISBN книги',
          '\n', '3, если нужно посчитать количество книг по году издания',
          '\n', '4, если нужно посчитать среднюю стоимость книг по каждому издательству',
          '\n', '5, если нужно вывести информацию о самой дорогой книге по издательству и году издания',)

    answer = str(input())
    answers = ['1', '2', '3', '4', '5']

    while answer not in answers:
        print('Введите верную цифру')
        answer = str(input())

    answer = int(answer)

    if answer == 1:
        dictionary_id = {}
        lst_turn = ['Title', 'Publisher', 'EAN', 'ISBN', 'Author',
                    'Printing copies', 'Year of publishing', 'Format', 'Price']

        for i in range(len(id_val)):
            dictionary_id[id_val[i]] = [title_val[i], publish_val[i],
                                        eans_val[i], isbn_val[i],
                                        ath_val[i], print_val[i],
                                        yr_of_publish_val[i],
                                        format_val[i], price_val[i]]

        print('Введите ID книги')
        id = str(input())
        while id not in id_val:
            print('Введите верный ID книги')
            id = str(input())

        for i in range(len(dictionary_id[id])):
            print(dictionary_id[id][i], '-', lst_turn[i])

    elif answer == 2:
        dictionary_isbn = {}
        lst_turn = ['ID', 'Title', 'Publisher', 'EAN', 'Author',
                    'Printing copies', 'Year of publishing', 'Format', 'Price']

        for i in range(len(isbn_val)):
            dictionary_isbn[isbn_val[i]] = [id_val[i], title_val[i],
                                            publish_val[i], eans_val[i],
                                            ath_val[i], print_val[i],
                                            yr_of_publish_val[i],
                                            format_val[i], price_val[i]]

        print('Введите ISBN книги')
        isbn = str(input())
        while isbn not in isbn_val:
            print('Введите верный ISBN книги')
            isbn = str(input())

        for i in range(len(dictionary_isbn[isbn])):
            print(dictionary_isbn[isbn][i], '-', lst_turn[i])

    elif answer == 3:
        dictionary_year = {}
        for i in range(len(yr_of_publish_val)):
            if dictionary_year.get(yr_of_publish_val[i], '0') == '0':
                dictionary_year[yr_of_publish_val[i]] = 1
            else:
                dictionary_year[yr_of_publish_val[i]] += 1

        print('Введите год издания книги')
        year = str(input())
        while year not in yr_of_publish_val:
            print('Введите верный год издания книги')
            year = str(input())

        print(dictionary_year[year],
              '- суммарное количество книг, изданных в этом году')

    elif answer == 4:
        dictionary_publish = {}
        for i in range(len(yr_of_publish_val)):
            if dictionary_publish.get(publish_val[i], '0') == '0':
                dictionary_publish[publish_val[i]] = [float(price_val[i]), 1]
            else:
                dictionary_publish[publish_val[i]][0] += float(price_val[i])
                dictionary_publish[publish_val[i]][1] += 1

        sum_price = 0
        sum_count = 0
        keys = list(dictionary_publish.keys())
        for i in range(len(dictionary_publish)):
            sum_price += dictionary_publish[keys[i]][0]
            sum_count += dictionary_publish[keys[i]][1]
            print('суммарная стоимость книг издателя', keys[i], ':',
                  sum_price // sum_count)

    else:
        dictionary_publish_yr = {}
        for i in range(len(title_val)):
            yr = yr_of_publish_val[i]
            pb = publish_val[i]
            if dictionary_publish_yr.get(pb, '0') == '0':
                dictionary_publish_yr[pb] = {yr: [(id_val[i], float(price_val[i]))]}

            elif dictionary_publish_yr[pb].get(yr, '0') == '0':
                dictionary_publish_yr[pb][yr] = [(id_val[i], float(price_val[i]))]

            else:
                dictionary_publish_yr[pb][yr].append((id_val[i], float(price_val[i])))
                dictionary_publish_yr[pb][yr].sort(key=lambda i: -i[1])

        dictionary_id = {}
        lst_turn = ['Title', 'Publisher', 'EAN', 'ISBN', 'Author',
                    'Printing copies', 'Year of publishing', 'Format', 'Price']

        for i in range(len(id_val)):
            dictionary_id[id_val[i]] = [title_val[i], publish_val[i],
                                        eans_val[i], isbn_val[i],
                                        ath_val[i], print_val[i],
                                        yr_of_publish_val[i],
                                        format_val[i], price_val[i]]

        print('Введите издателя книги')
        publisher = str(input())
        while publisher not in publish_val:
            print('Введите верного издателя книги')
            publisher = str(input())

        print('Введите год издания книги')
        year = str(input())
        while year not in list(dictionary_publish_yr[publisher].keys()):
            print('Введите верный год издания книги')
            year = str(input())

        all_expensive_books = [dictionary_publish_yr[publisher][year][0][0]]
        for i in range(1, len(dictionary_publish_yr[publisher][year])):
            if dictionary_publish_yr[publisher][year][i][1] == dictionary_publish_yr[publisher][year][0][1]:
                all_expensive_books.append(dictionary_publish_yr[publisher][year][i][0])

        for i in all_expensive_books:
            for j in range(len(dictionary_id[i])):
                print(dictionary_id[i][j], '-', lst_turn[j])

main('books.xml')