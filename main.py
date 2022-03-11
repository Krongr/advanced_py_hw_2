import csv
import re

if __name__ == '__main__':
    with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    general_info_pattern = re.compile(
        r'(^\w*)[\s,](\w*,?)[\s,](\w*,)([,]?)*'
        r'(\w*)[\s,]([,]?)*([a-zA-Zа-яёА-ЯЁ\s\–]*,)'
    )
    general_info_repl = r'\1,\2,\3\4\5,\7'
    phone_number_pattern = re.compile(
        r'(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\s?\-?(\d{2})\s?\-?(\d{2})'
    )
    phone_number_repl = r'+7(\2)\3-\4-\5'

    for i in range(0, len(contacts_list)):
        contacts_list[i] = ','.join(contacts_list[i])
        contacts_list[i] = general_info_pattern.sub(
            general_info_repl, 
            contacts_list[i]
        )
        contacts_list[i] = phone_number_pattern.sub(
            phone_number_repl,
            contacts_list[i]
        )
        contacts_list[i] = re.sub(
            r'\(?(доб.)\s(\d{4})\)?', 
            r'\1\2', 
            contacts_list[i]
        )
        contacts_list[i] = contacts_list[i].split(',')
        if len(contacts_list[i]) == 8:
            contacts_list[i].pop(-1)

    contacts_to_remove =[]
    for i in range(0, len(contacts_list)):
        for k in range(i+1, len(contacts_list)):
            if (
                contacts_list[i][0] == contacts_list[k][0] and 
                contacts_list[i][1] == contacts_list[k][1]
            ):                
                for field in range(2, len(contacts_list[0])):
                    if (
                        (contacts_list[i][field] !=
                         contacts_list[k][field]) and
                        contacts_list[i][field] != '' and
                        contacts_list[k][field] != ''
                    ):
                        print('Похожие строки невозможно совместить '
                              'из-за пресекающихся полей.'
                        )
                        print(f'Конфликтные строки: \n'
                              f'{contacts_list[i]} \n'
                              f'{contacts_list[k]}'
                        )
                        break
                    elif (
                        contacts_list[i][field] == '' and 
                        contacts_list[k][field] != ''
                    ):
                        contacts_list[i][field] = contacts_list[k][field]

                contacts_to_remove.append(contacts_list[k])
    
    for _contact in contacts_to_remove:
        contacts_list.remove(_contact)
    
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',', lineterminator='\r')  
        datawriter.writerows(contacts_list)
