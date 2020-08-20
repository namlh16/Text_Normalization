from norm.read import *
from nltk import word_tokenize
from roman import fromRoman
import configparser
import csv
import pandas as pd
import copy
import norm.read as read
import norm.utils as utils



def norm_punct(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    punct = '! " “ \' ( ) , - . / : ; ? [ ] _ ` { | } ~ ” – `` '' – ” ...'.split()
    for e in punct:
        e = e.strip()
        input_str = input_str.replace(' ' + e + ' ', ' <PUNCT>' + e + '</PUNCT> ')
        output_str = output_str.replace(' ' + e + ' ', ' <PUNCT>' + 'sil' + '</PUNCT> ')
    return input_str, output_str


def norm_tag_verbatim(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    verbatim = '# $ % & * + < = > @ ^'.split()
    for e in verbatim:
        e = e.strip()
        input_str = input_str.replace(' ' + e + ' ', ' <VERBATIM>' + e + '</VERBATIM> ')
        if e == '#':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'thăng' + '</VERBATIM> ')
        elif e == '$':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'đô la' + '</VERBATIM> ')
        elif e == '%':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'phần trăm' + '</VERBATIM> ')
        elif e == '&':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'và' + '</VERBATIM> ')
        elif e == '*':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'nhân' + '</VERBATIM> ')
        elif e == '÷':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'chia' + '</VERBATIM> ')
        elif e == '+':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'cộng' + '</VERBATIM> ')
        elif e == '<':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'nhỏ hơn' + '</VERBATIM> ')
        elif e == '=':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'bằng' + '</VERBATIM> ')
        elif e == '>':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'lớn hơn' + '</VERBATIM> ')
        elif e == '@':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'a còng' + '</VERBATIM> ')
        elif e == '^':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'mũ' + '</VERBATIM> ')
        elif e == '\\':
            output_str = output_str.replace(' ' + e + ' ', ' <VERBATIM>' + 'trên' + '</VERBATIM> ')

    return input_str, output_str


def normalize_letters(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    match_in = re.search('(?=(\s[BCDĐFGHJKLMNPQRSTVWXZ]{2,50}\s))', input_str)
    match_out = re.search('(?=(\s[BCDĐFGHJKLMNPQRSTVWXZ]{2,50}\s))', output_str)
    while match_in is not None and match_out is not None:
        start_match_in = match_in.start(1)
        end_match_in = match_in.end(1)
        term_in = input_str[start_match_in:end_match_in]
        input_str = replace_str(input_str, start_match_in, end_match_in, term_in, '<LETTER>', '</LETTER>')

        start_match_out = match_out.start(1)
        end_match_out = match_out.end(1)
        term_out = output_str[start_match_out :end_match_out]
        term_norm_out = term_out.replace(term_out , ' '.join(list(term_out )))
        output_str = replace_str(output_str, start_match_out , end_match_out , term_norm_out , '<LETTER>', '</LETTER>')

        match_in = re.search('(?=(\s[BCDĐFGHJKLMNPQRSTVWXZ]{2,50}\s))', input_str)
        match_out = re.search('(?=(\s[BCDĐFGHJKLMNPQRSTVWXZ]{2,50}\s))', output_str)

    return input_str, output_str



def norm_measure(str, config_norm):

    str = ' ' + str + ' '
    norm_str = norm_measure_generic(str, config_norm['km_pattern'], 'km', ' ki lô mét ')
    norm_str = norm_measure_generic(norm_str, config_norm['m3_pattern'], 'm3', ' mét khối ')
    norm_str = norm_measure_generic(norm_str, config_norm['m2_pattern'], 'm2', ' mét vuông ')
    norm_str = norm_measure_generic(norm_str, config_norm['m_pattern'], 'm', ' mét')
    norm_str = norm_measure_generic(norm_str, config_norm['cm_pattern'], 'cm', ' xen ti mét ')
    norm_str = norm_measure_generic(norm_str, config_norm['mm_pattern'], 'mm', ' mi li mét ')
    norm_str = norm_measure_generic(norm_str, config_norm['mm_pattern'], 'ms', ' mi li giây ')
    norm_str = norm_measure_generic(norm_str, config_norm['nm_pattern'], 'nm', ' na nô mét ')
    norm_str = norm_measure_generic(norm_str, config_norm['ha_pattern'], 'ha', ' héc ta mét ')
    norm_str = norm_measure_generic(norm_str, config_norm['l_pattern'], 'l', ' lít ')
    norm_str = norm_measure_generic(norm_str, config_norm['kg_pattern'], 'kg', ' ki lô gam ')
    norm_str = norm_measure_generic(norm_str, config_norm['g_pattern'], 'g', ' gam ')
    norm_str = norm_measure_generic(norm_str, config_norm['gr_pattern'], 'gram', ' gờ ram ')
    norm_str = norm_measure_generic(norm_str, config_norm['mg_pattern'], 'mg', ' mi li gam ')
    norm_str = norm_measure_generic(norm_str, config_norm['s_pattern'], 's', ' giây ')
    norm_str = norm_measure_generic(norm_str, config_norm['p_pattern'], 'p', ' phút ')
    norm_str = norm_measure_generic(norm_str, config_norm['m_odd_pattern'], 'm', ' mét ')
    norm_str = read.unit2words('', norm_str)[1]
    norm_str = utils.remove_tag(norm_str)

    return norm_str

# print(norm_measure('   <MEASURE>ki lô mét trên giờ</MEASURE>    '))

def norm_measure_generic(str, pattern, term, repl):
    matches = re.findall(pattern, str)
    if len(matches) > 0:
        for item in matches:
            item_norm_out = item.replace(term, repl)
            str = str.replace(item, item_norm_out)

    return replace_multi_space(str)



def normalize_date(input_str, output_str):
    """
    Normalize dates.
    """
    input_str, output_str = norm_date_type_1(input_str, output_str)
    input_str, output_str = norm_date_type_2(input_str, output_str)
    input_str, output_str = norm_date_type_3(input_str, output_str)
    input_str, output_str = norm_date_type_4(input_str, output_str)

    return input_str, output_str


def norm_date_type_1(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize dd/mm/yy[yy] (dmy) form of dates
    # Note: '8-6-2019' format này để riêng vì tránh cases "từ '8-6/2019' mây thay đổi nhiều"
    date_dmy_pattern = re.compile(r'\s(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])[\/.](\d{2}|\d{4})\s|\s(0?[1-9]|[12]\d|3[01])[\-](0?[1-9]|[1][0-2])[\-](\d{2}|\d{4})\s')
    temp_str_date_dmy = input_str
    dates_dmy = []
    while(date_dmy_pattern.search(temp_str_date_dmy)):
        date = date_dmy_pattern.search(temp_str_date_dmy)
        dates_dmy.append(date.group())
        temp_str_date_dmy = temp_str_date_dmy[date.span()[1]-1:]

    if len(dates_dmy) > 0:
        for date in dates_dmy:
            date_str = date_dmy2words(date)
            # print('date_dd/mm/[yy]yy:', date, '-', input_str)
            input_str = input_str.replace(date, ' <DATE>' + date + '</DATE> ')
            output_str = output_str.replace(date, ' <DATE>' + 'ngày ' + date_str + '</DATE> ')

    return input_str, output_str


def norm_date_type_2(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize dd/mm (dm) form of dates
    date_dm_pattern = re.compile(r'(sau , |mai , |qua , |nay , |sớm|đến hết|[Đđ]ường|[Pp]hiên|[Nn]gày|[Ss]áng|[Tt]rưa|[Cc]hiều|[Tt]ối|[Đđ]êm|[Mm]ùng|[Hh]ôm|nay|[Ss]áng qua|[Tt]ưa qua|[Cc]hiều qua|[Tt]ối qua|[Đđ]êm qua|[Hh]ôm qua|[Hh]ôm sau|mai|[Vv]ào|kéo dài tới|dự kiến tới|đến|tới|[Tt]ừ)\s\(*\s*(0?[1-9]|[12]\d|3[01])[\/\-.](0?[1-9]|[1][0-2])\s\)*')
    temp_str_date_dm = input_str
    dates_dm = []
    while(date_dm_pattern.search(temp_str_date_dm)):
        date = date_dm_pattern.search(temp_str_date_dm)
        if ')' in date.group():
            dates_dm.append(date.group().strip().split()[-2])
        else:
            dates_dm.append(date.group().strip().split()[-1])
        temp_str_date_dm = temp_str_date_dm[date.span()[1]-1:]

    # Cases: "số ra các ngày 28 29-2 và 1-3", "ngày 19 và 20.3 tới"
    dates_dm_special = re.findall('[Nn]gày .+ và (\d{1,2}[\/\-.]\d{1,2})\s', input_str)
    if len(dates_dm_special) > 0:
        dates_dm += dates_dm_special
    if len(dates_dm) > 0:
        for date in dates_dm:
            date_str = date_dm2words(date)
            # print('date_dd/mm:', date, '-', input_str)
            input_str = input_str.replace(' ' + date + ' ', ' <DATE>' + date + '</DATE> ')
            output_str = output_str.replace(' ' + date + ' ', ' <DATE>' + date_str + '</DATE> ')

    return input_str, output_str



def norm_date_type_3(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize dd/mm form without clear rules
    # Cám ơn cha dành cho Ngày của cha (16/6) tới đây của Hồ Ngọc Hà...
    p = re.compile(r'[Nn]gày .+\s\(*\s*(0?[1-9]|[12]\d|3[01])\s*\/\s*(0?[1-9]|[1][0-2])\s*\)')
    l = []
    temp_line = input_str
    while(p.search(temp_line)):
        item = p.search(temp_line)
        l.append(item.group())
        temp_line = temp_line[item.span()[1]-1:]

    dates_dm_ = []
    if len(l) > 0:
        temp_str = l[0]
        p = re.compile(r'\s(0?[1-9]|[12]\d|3[01])\s*\/\s*(0?[1-9]|[1][0-2])\s')
        while(p.search(temp_str)):
            date = p.search(temp_str)
            dates_dm_.append(date.group())
            temp_str = temp_str[date.span()[1]-1:]

    if len(dates_dm_) > 0:
        for date in dates_dm_:
            date_str = date_dm2words(date)
            input_str = input_str.replace(date, ' <DATE>' + date + '</DATE> ')
            output_str = output_str.replace(date, ' <DATE>' + date_str + '</DATE> ')

    return input_str, output_str



def norm_date_type_4(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize mm/yyyy (my) form of dates
    # @improve:
    # những cases không có [Tt]háng ở trước --> thêm 'tháng' ở date_my2word()
    # trong read.py  nhưng tránh các trường hợp Quý 2/2018, đợt 3/2019, tỷ lệ 1/2000
    date_my_pattern = re.compile(r'\s(0?[1-9]|[1][0-2])[\/\-.](\d{4})\s')
    temp_str_date_my = input_str
    dates_my = []
    while(date_my_pattern.search(temp_str_date_my)):
        date = date_my_pattern.search(temp_str_date_my)
        dates_my.append(date.group().strip())
        temp_str_date_my = temp_str_date_my[date.span()[1]-1:]
    if len(dates_my) > 0:
        for date in dates_my:
            date_str = date_my2words(date)
            # print('date_mm/yyyy:', date, '-', input_str)
            input_str = input_str.replace(' ' + date + ' ', ' <DATE>' + date + '</DATE> ')
            output_str = output_str.replace(' ' + date + ' ', ' <DATE>' + date_str + '</DATE> ')

    return input_str, output_str


def normalize_date_range(input_str, output_str):
    input_str, output_str = norm_date_range_type_1(input_str, output_str)
    input_str, output_str = norm_date_range_type_2(input_str, output_str)
    input_str, output_str = norm_date_range_type_3(input_str, output_str)
    input_str, output_str = norm_date_range_type_4(input_str, output_str)
    input_str, output_str = norm_date_range_type_5(input_str, output_str)
    input_str, output_str = norm_date_range_type_6(input_str, output_str)

    return input_str, output_str



def norm_date_range_type_1(input_str, output_str):
    """
    Normalize date ranges.
    """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize yyyy-yyyy forms: 2016-2017, 1912-1982 ngày sinh, v.v.
    # @improve:
    # Khi nào thì chèn từ vào ví dụ 'năm học 2018-2019' thì đọc luôn tên năm còn
    # 'công ty thu thiếu hụt khoản này từ năm 2012-2017 là 11,3 tỷ đồng'
    # thì cần thêm từ "đến": từ năm 2012 đến 2017
    year_range_pattern = re.compile(r'\s(\d{4})\s*\-\s*(\d{4})\s')
    temp_str = input_str
    year_range_list = []
    while(year_range_pattern.search(temp_str)):
        year_range = year_range_pattern.search(temp_str)
        year_range_list.append(year_range.group())
        temp_str = temp_str[year_range.span()[1]-1:]

    if len(year_range_list) > 0:
        # print(str(year_range_list), " : ", input_str)
        for year_range in year_range_list:
            year_range_norm = year_range.replace('-', ' - ')
            year_range_norm = " ".join(year_range_norm.split())
            start_year = year_range_norm.split('-')[0]
            end_year = year_range_norm.split('-')[1]
            year_range_str = num2words_fixed(start_year) + ' đến ' + num2words_fixed(end_year)
            input_str = input_str.replace(year_range, ' <DATE>' + year_range + '</DATE> ')
            output_str = output_str.replace(year_range, ' <DATE>' + year_range_str + '</DATE> ')

    return input_str, output_str



# Normalize mm/yyyy-mm/yyyy forms


def norm_date_range_type_2(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize dd/mm/yyyy-dd/mm/yyyy forms
    date_range_dmy_pattern = re.compile(r'\s(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])[\/.](\d{4})\s*\-\s*(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])[\/.](\d{4})\s')
    temp_str = input_str
    date_range_dmy_list = []
    while(date_range_dmy_pattern.search(temp_str)):
        date_range_dmy = date_range_dmy_pattern.search(temp_str)
        date_range_dmy_list.append(date_range_dmy.group())
        temp_str = temp_str[date_range_dmy.span()[1]-1:]

    if len(date_range_dmy_list) > 0:
        # print(str(date_range_dmy_list), " : ", input_str)
        for date_range_dmy in date_range_dmy_list:
            start_date = date_range_dmy.split('-')[0]
            end_date = date_range_dmy.split('-')[1]
            date_range_dmy_str = date_dmy2words(start_date) + ' đến ' + date_dmy2words(end_date)
            input_str = input_str.replace(date_range_dmy, ' <DATE>' + date_range_dmy + '</DATE> ')
            output_str = output_str.replace(date_range_dmy, ' <DATE>' + date_range_dmy_str + '</DATE> ')

    return input_str, output_str


def norm_date_range_type_3(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize dd-dd/mm/yyyy forms
    date_range_dmy1_pattern = re.compile(r'\s(0?[1-9]|[12]\d|3[01])\s*\-\s*(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])[\/.](\d{4})\s')
    temp_str = input_str
    date_range_dmy1_list = []
    while(date_range_dmy1_pattern.search(temp_str)):
        date_range_dmy1 = date_range_dmy1_pattern.search(temp_str)
        date_range_dmy1_list.append(date_range_dmy1.group())
        temp_str = temp_str[date_range_dmy1.span()[1]-1:]

    if len(date_range_dmy1_list) > 0:
        # print(str(date_range_dmy1_list), " : ", input_str)
        for date_range_dmy1 in date_range_dmy1_list:
            start_date = date_range_dmy1.split('-')[0]
            end_date = date_range_dmy1.split('-')[1]
            date_range_dmy1_str = num2words_fixed(start_date) + ' đến ' + date_dmy2words(end_date)
            input_str = input_str.replace(date_range_dmy1, ' <DATE>' + date_range_dmy1 + '</DATE> ')
            output_str = output_str.replace(date_range_dmy1, ' <DATE>' + date_range_dmy1_str + '</DATE> ')

    return input_str, output_str


def norm_date_range_type_4(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize dd/mm-dd/mm/yyyy forms
    date_range_dmy2_pattern = re.compile(r'\s(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])\s*\-\s*(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])[\/.](\d{4})\s')
    temp_str = input_str
    date_range_dmy2_list = []
    while(date_range_dmy2_pattern.search(temp_str)):
        date_range_dmy2 = date_range_dmy2_pattern.search(temp_str)
        date_range_dmy2_list.append(date_range_dmy2.group())
        temp_str = temp_str[date_range_dmy2.span()[1]-1:]

    if len(date_range_dmy2_list) > 0:
        # print(str(date_range_dmy2_list), " : ", input_str)
        for date_range_dmy2 in date_range_dmy2_list:
            start_date = date_range_dmy2.split('-')[0]
            end_date = date_range_dmy2.split('-')[1]
            date_range_dmy2_str = date_dm2words(start_date) + ' đến ' + date_dmy2words(end_date)
            input_str = input_str.replace(date_range_dmy2, ' <DATE>' + date_range_dmy2 + '</DATE> ')
            output_str = output_str.replace(date_range_dmy2, ' <DATE>' + date_range_dmy2_str + '</DATE> ')

    return input_str, output_str



def norm_date_range_type_5(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize dd/mm-dd/mm forms: 20/1-18/2
    date_range_dm1_pattern = re.compile(r'\s(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])\s*\-\s*(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])\s')
    temp_str = input_str
    date_range_dm1_list = []
    while(date_range_dm1_pattern.search(temp_str)):
        date_range_dm1 = date_range_dm1_pattern.search(temp_str)
        date_range_dm1_list.append(date_range_dm1.group())
        temp_str = temp_str[date_range_dm1.span()[1]-1:]

    if len(date_range_dm1_list) > 0:
        # print(str(date_range_dm1_list), " : ", input_str)
        for date_range_dm1 in date_range_dm1_list:
            start_date = date_range_dm1.split('-')[0]
            end_date = date_range_dm1.split('-')[1]
            date_range_dm1_str = date_dm2words(start_date) + ' đến ' + date_dm2words(end_date)
            input_str = input_str.replace(date_range_dm1, ' <DATE>' + date_range_dm1 + '</DATE> ')
            output_str = output_str.replace(date_range_dm1, ' <DATE>' + date_range_dm1_str + '</DATE> ')

    return input_str, output_str



def norm_date_range_type_6(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize dd-dd/mm forms: 15-18/6, 15 -18/6, 15- 18/6
    date_range_dm2_pattern = re.compile(r'\s(0?[1-9]|[12]\d|3[01])\s*\-\s*(0?[1-9]|[12]\d|3[01])[\/.](0?[1-9]|[1][0-2])\s')
    temp_str = input_str
    date_range_dm2_list = []
    while(date_range_dm2_pattern.search(temp_str)):
        date_range_dm2 = date_range_dm2_pattern.search(temp_str)
        date_range_dm2_list.append(date_range_dm2.group())
        temp_str = temp_str[date_range_dm2.span()[1]-1:]

    if len(date_range_dm2_list) > 0:
        # print(str(date_range_dm2_list), " : ", input_str)
        for date_range_dm2 in date_range_dm2_list:
            start_date = date_range_dm2.split('-')[0]
            end_date = date_range_dm2.split('-')[1]
            date_range_dm2_str = num2words(int(start_date), lang='vi') + ' đến ' + date_dm2words(end_date)
            input_str = input_str.replace(date_range_dm2, ' <DATE>' + date_range_dm2 + '</DATE> ')
            output_str = output_str.replace(date_range_dm2, ' <DATE>' + date_range_dm2_str + '</DATE> ')

    return input_str, output_str



def norm_tag_roman_num(input_str, output_str):
    """
    Normalize roman numerals.
    """
    # @improve: 'Nữ hoàng Anh Elizabeth II thường đi lại trên chiếc xe của Land
    # Rovers và Jaguars' --> II đọc thành là 'đệ nhị'
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    roman_numeral_p = re.compile('\s(X{0,3})(IX|IV|V?I{0,3})\s|\s(x{0,3})(ix|iv|v?i{0,3})\s')

    # For double check if the string is roman numeral or not
    roman_numeral_check = re.compile('(thế hệ|nhóm|số|đại hội|thứ|giai đoạn|quý|cấp|quận|kỳ|khóa|quy định|và|vành đai|vùng|thế kỷ|loại|khu vực|khu|đợt|hạng|báo động|tập|lần|trung ương|tw|chương)(\s(X{0,3})(IX|IV|V?I{0,3})\s|\s(x{0,3})(ix|iv|v?i{0,3})\s)', re.IGNORECASE)

    temp_str = input_str
    temp_str = " " + " ".join(word_tokenize(temp_str)) + " "
    roman_numeral_list = []
    while(roman_numeral_p.search(temp_str, re.IGNORECASE)):
        roman_numeral = roman_numeral_p.search(temp_str)
        # print("roman_numeral: ", roman_numeral)
        roman_numeral_list.append(roman_numeral.group().strip())
        temp_str = temp_str[roman_numeral.span()[1]-1:]

    if len(roman_numeral_list) > 0:
        # print('roman_numeral_list:', str(roman_numeral_list), " : ", input_str)
        for roman_numeral in roman_numeral_list:
            # if roman_numeral in ['X', 'V', 'x', 'v']:
            if (roman_numeral_check.search(input_str, re.IGNORECASE)):
                roman2int = fromRoman(roman_numeral.upper())
                roman_numeral_str = num2words(roman2int, lang='vi')
                input_str = input_str.replace(' ' + roman_numeral + ' ', ' <ROMAN>' + roman_numeral + '<ROMAN> ')
                output_str = output_str.replace(' ' + roman_numeral + ' ', ' <ROMAN>' + roman_numeral_str + '<ROMAN> ')
            # else:
            #     roman2int = fromRoman(roman_numeral.upper())
            #     roman_numeral_str = num2words(roman2int, lang='vi')
            #     input_str = input_str.replace(' ' + roman_numeral + ' ', ' <ROMAN>' + roman_numeral + '</ROMAN> ')
            #     output_str = output_str.replace(' ' + roman_numeral + ' ', ' <ROMAN>' + roman_numeral_str + '</ROMAN> ')

    return input_str, output_str


def norm_tag_roman_num_v2(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    roman_numeral_p = re.compile('\s(\(\s*X{0,3})(IX|IV|V?I{0,3})\s*\)\s|\s(\(\s*x{0,3})(ix|iv|v?i{0,3})\s*\)\s')
    temp_str = input_str
    temp_str = " " + " ".join(word_tokenize(temp_str)) + " "
    roman_numeral_list = []
    while (roman_numeral_p.search(temp_str, re.IGNORECASE)):
        roman_numeral = roman_numeral_p.search(temp_str)
        # print("roman_numeral: ", roman_numeral)
        roman_numeral_list.append(roman_numeral.group().strip())
        temp_str = temp_str[roman_numeral.span()[1] - 1:]
    if len(roman_numeral_list) > 0:
        for roman_numeral in roman_numeral_list:
            roman = roman_numeral.replace('(','').replace(')','').strip()
            roman2int = fromRoman(roman.upper())
            roman_numeral_str = num2words(roman2int, lang='vi')
            input_str = input_str.replace(' ' + roman_numeral + ' ', ' <ROMAN>' + roman_numeral + '<ROMAN> ')
            output_str = output_str.replace(' ' + roman_numeral + ' ', ' <ROMAN>, ' + roman_numeral_str + ' ,<ROMAN> ')

    return input_str, output_str


def normalize_phone_number(input_str, output_str):
    """
    Normalize phone numbers
    """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    p = re.compile(r"(hotline|tổng đài|chi tiết|hỗ trợ|tư vấn|điện thoại|đường dây nóng|liên hệ|gọi|ĐKKD)+\s*\:*\s*(\d{8,12}|\d{3}\s\d{4}\s\d{4}|\d{4}\.\d{3}\.\d{3}|\d{4}\s\d{3}\s\d{3,4}|\d{3,4}\s\d{6,7}|\d{3,4}\b)")
    # phone_numbers = re.findall(r"\d{10,12}|\d{4}\s\d{3}\s\d{3,4}|\d{3,4}\s\d{6,7}", input_str)
    # phone_numbers = re.findall(r"((09|03|07|08|05)+([0-9]{8})\b)", input_str)
    # phone_numbers = re.findall(r"((09|03|07|08|05)+([0-9]{8})\b)|(1900|1800|024|028)+\s*\)*\s*(\d{8})", input_str)

    temp_str = input_str
    phone_number_list = []
    while(p.search(temp_str)):
        phone_number = p.search(temp_str)
        term = phone_number.group()
        x = re.search(r"\d{8,12}|\d{3}\s\d{4}\s\d{4}|\d{4}\.\d{3}\.\d{3}|\d{4}\s\d{3}\s\d{3,4}|\d{3,4}\s\d{6,7}|\d{3,4}\b",term)
        phone_number_list.append(x.group())
        temp_str = temp_str[phone_number.span()[1]-1:]
    if len(phone_number_list) > 0:
        for phone_number in phone_number_list:
            phone_number_str = phone2words(phone_number)
            # print('phone_number:', phone_number, '-', phone_number_str)
            input_str = input_str.replace(' ' + phone_number + ' ', ' <DIGIT>' + phone_number + '</DIGIT> ')
            output_str = output_str.replace(' ' + phone_number + ' ', ' <DIGIT>' + phone_number_str + '</DIGIT> ')

    return input_str, output_str

def phone_single(input_str, output_str):
    """
        Normalize CMT, STK
        """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    phone_numbers = re.findall(r"((09|03|07|08|05|1900|1800|024|028|84)+([0-9]{4})\b)", input_str)
    if len(phone_numbers) > 0:
        for digit in phone_numbers:
            digits_str = phone2words(digit)
            # print('phone_number:', phone_number, '-', phone_number_str)
            input_str = input_str.replace(digit, ' <DIGIT>' + digit + '</DIGIT> ')
            output_str = output_str.replace(digit, ' <DIGIT>' + digits_str + '</DIGIT> ')

    return input_str, output_str

def normalize_number_plate(input_str, output_str):
    """
        Normalize CMT, STK
        """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    p = re.compile(r"([0-9]+[a-zA-Z]+[0-9]*)+\s*\-\s*(\d{3}\.\d{2}|\d{4}\b)")
    temp_str = input_str
    number_plate_list = []
    while(p.search(temp_str)):
        number_plate = p.search(temp_str)
        x = number_plate.group()
        number_plate_list.append(x.split("-")[-1])
        temp_str = temp_str[number_plate.span()[1]-1:]
    if len(number_plate_list) > 0:
        for number_plate in number_plate_list:
            number_plate_str = phone2words(number_plate)
            # print('phone_number:', phone_number, '-', phone_number_str)
            input_str = input_str.replace(number_plate, ' <DIGIT>' + number_plate + '</DIGIT> ')
            output_str = output_str.replace(number_plate, ' <DIGIT>' + number_plate_str + '</DIGIT> ')

    return input_str, output_str

def norm_digit(input_str, output_str):
    """
        Normalize CMT, STK
        """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # p = re.compile(r"[\d ]{9,20}")
    p = re.compile(r"(chứng minh nhân dân|chứng minh thư|mã thẻ|số thẻ|số tài khoản|căn cước|mã số thuế|mã số|nhân viên|mã)+\s*\:*\s*(\d{2,20}\b)")  
    temp_str = input_str
    digits_list = []
    while(p.search(temp_str)):
        digit = p.search(temp_str)
        term = digit.group()
        x = re.search(r"\d{2,20}\b",term)
        digits_list.append(x.group())
        temp_str = temp_str[digit.span()[1]-1:]
    # digits = re.findall(r"[\d ]{9,20}", input_str)
    if len(digits_list) > 0:
        for digit in digits_list:
            print(digit)
            digits_str = phone2words(digit)
            # print('phone_number:', phone_number, '-', phone_number_str)
            input_str = input_str.replace(digit, ' <DIGIT>' + digit + '</DIGIT> ')
            output_str = output_str.replace(digit, ' <DIGIT>' + digits_str + '</DIGIT> ')

    return input_str, output_str

def normalize_negative_number(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # p = re.compile(r'\s\-([\d]+)\s')
    p = re.compile(r"(là|kết quả|âm|dưới|lạnh|xuống|nhiệt độ|áp suất)+\s*\:*\-\s*[0-9]*,*[0-9]+\s")
    temp_str = input_str
    neg_numbers = []
    while (p.search(temp_str)):
        numbers = p.search(temp_str)
        term = numbers.group()
        neg_numbers.append(term.split("-")[-1])
        temp_str = temp_str[numbers.span()[1] - 1:]
    if len(neg_numbers) > 0:
        for number in neg_numbers:
            if ',' in number:
                numbers_str = num2words_float(number)
            else:
                numbers_str = num2words_fixed(number)
            numbers_str = ' âm ' + numbers_str
            input_str = input_str.replace(number, ' <CARDINAL>' + number + '</CARDINAL> ')
            output_str = output_str.replace(number, ' <CARDINAL>' + numbers_str + '</CARDINAL> ')

    return input_str, output_str

def normalize_number_range(input_str, output_str):
    """
    Normalize number ranges
    """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    p = re.compile(r"(hơn|kém|gấp|tăng|tầm|giảm|nhất|tới|có|sau|mức|tuổi|[Tt]ừ|tăng tốc|được|[Kk]hoảng)\s+[0-9]*,*[0-9]+\s*\-\s*[0-9]*,*[0-9]+\s")
    temp_str = input_str
    number_range_list = []
    while(p.search(temp_str)):
        number_range = p.search(temp_str)
        term = number_range.group()
        x = re.search(r"[0-9]*,*[0-9]+\s*\-\s*[0-9]*,*[0-9]+\s", term)
        number_range_list.append(x.group())
        temp_str = temp_str[number_range.span()[1]-1:]

    if len(number_range_list) > 0:
        # print(str(number_range_list), ' : ', input_str)
        for number_range in number_range_list:
            start_num = number_range.split('-')[0]
            end_num = number_range.split('-')[1]
            if ',' in start_num:
                start_num = num2words_float(start_num)
            else:
                start_num = num2words_fixed(start_num)

            if ',' in end_num:
                end_num = num2words_float(end_num)
            else:
                end_num = num2words_fixed(end_num)

            number_range_str = start_num + ' đến ' + end_num
            input_str = input_str.replace(number_range, ' <CARDINAL>' + number_range + '</CARDINAL> ')
            output_str = output_str.replace(number_range, ' <CARDINAL>' + number_range_str + '</CARDINAL> ')

    return input_str, output_str


def normalize_version(input_str):
    """
    Normalize many kinds of version, such as softwares, models, etc
    """
    return input_str

def norm_x(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    vi_numbers = re.findall(r'[0-9]*[.,]*[0-9]+\s*x\s*[0-9]*[.,]*[0-9]+\s*x\s*[0-9]*[.,]*[0-9]|[0-9]*[.,]*[0-9]+\s*x\s*[0-9]*[.,]*[0-9]', output_str)
    if len(vi_numbers) > 0:
        for vi_number in vi_numbers:
            vi_number_ver = multiple1(vi_number)
            input_str = input_str.replace(vi_number, ' ' + vi_number + ' ')
            print(input_str)
            output_str = output_str.replace(vi_number, ' ' + vi_number_ver + ' ')
            print(output_str)

    return input_str, output_str


def normalize_number(input_str, output_str):
    input_str, output_str = norm_number_type_1(input_str, output_str)
    input_str, output_str = norm_number_type_2(input_str, output_str)
    input_str, output_str = norm_number_type_3(input_str, output_str)

    return input_str, output_str


def norm_number_type_1(input_str, output_str):
    """
    Normalize number
    """
    # Normalize vi-style numbers: '2.300 Euro', '25.320 vé', etc
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    vi_numbers = re.findall(r'\s([\d]+\.[\d]+\.*[\d]*\.*[\d]*\.*[\d]*)\s', output_str)
    if len(vi_numbers) > 0:
        for vi_number in vi_numbers:
            vi_number_norm = "".join(vi_number.split('.'))
            if int(vi_number_norm) >= 1000:
                input_str = input_str.replace(' ' + vi_number + ' ', ' ' + vi_number + ' ')
                output_str = output_str.replace(' ' + vi_number + ' ', ' ' + vi_number_norm + ' ')
            else:
                vi_number_ver = version2words(vi_number)
                input_str = input_str.replace(' ' + vi_number + ' ', ' ' + vi_number + ' ')
                output_str = output_str.replace(' ' + vi_number + ' ', ' ' + vi_number_ver + ' ')

    return input_str, output_str


def norm_number_type_2(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # Normalize numbers with comma format: '224,3 tỷ', '16,2 phần trăm', etc
    numbers_w_comma = re.findall(r'\s([\d]+,[\d]+)\s', output_str)
    if len(numbers_w_comma) > 0:
        for number in numbers_w_comma:
            number_str = num2words_float(number)
            # print(number, ":", number_str)
            input_str = input_str.replace(' ' + number + ' ',' ' + number + ' ')
            output_str = output_str.replace(' ' + number + ' ',' ' + number_str + ' ')

    return input_str, output_str


def norm_number_type_3(input_str, output_str):
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    numbers = re.findall(r'(\d+)', output_str)
    if len(numbers) > 0:
        for number in numbers:
            number_str = num2words_fixed(number)
            input_str = input_str.replace(' '+number +' ',' ' + number + ' ')
            output_str = output_str.replace(' '+number +' ',' ' + number_str + ' ')

    return input_str, output_str
    


def normalize_time(input_str, output_str):
    """
    Normalize time
    """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    # time_patterns = re.compile(r'\b(0?[0-9]|1\d|2[0-4])[:hg](0?[0-9]|[1-5]\d|)\b')
    # time_patterns = re.compile(r'(\d+)(\:|h|giờ)(0?[0-9]|[1-5][0-9])(\:|p|phút)([1-5][0-9]|0?[0-9])|(\d+)(\:|h)([1-5][0-9]|0?[0-9])|(\d+)h')
    # time_patterns = re.compile(r'(\d+)(\:|h|giờ)(0?[0-9]|[1-5][0-9])(\:|p|phút)|(\d+)(\:|h)([1-5][0-9]|0?[0-9])|(\d+)h')
    time_patterns = re.compile(r'(\d+)(\:|h)(0?[0-9]|[1-5][0-9])(\:|p)|(\d+)(\:|h)([1-5][0-9]|0?[0-9])|(\d+)h')


    temp_str_time = input_str
    times = []
    while(time_patterns.search(temp_str_time)):
        time = time_patterns.search(temp_str_time)
        times.append(time.group())
        temp_str_time = temp_str_time[time.span()[1]:]

    times = [time for time in times if not(time.startswith('24') and (time[3:]>'00')) ]
    if len(times) > 0:
        for time in times:
            time_str = time2words(time)
            # print('time:', time, '-', time_str)
            input_str = input_str.replace(' ' + time + ' ', ' <TIME>' + time + '</TIME> ')
            output_str = output_str.replace(' ' + time + ' ', ' <TIME>' + time_str + '</TIME> ')

    return input_str, output_str


def normalize_sport_score(input_str, output_str):
    """
    Normalize sport scores
    """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    scores = re.findall('\s[0-9]+\-[0-9]+\s', input_str)
    sport_ngrams = ['tỷ số', 'chiến thắng', 'trận đấu', 'tỉ số', 'bàn thắng', 'trên sân', 'đội bóng', 'thi đấu', 'cầu thủ',\
                    'vô địch', 'mùa giải', 'đánh bại', 'đối thủ', 'bóng đá', 'gỡ hòa', 'chung kết', 'bán kết', 'ghi bàn', \
                    'chủ nhà', 'tiền đạo', 'dứt điểm', 'tiền vệ', 'tiền đạo', 'thua']
    is_sport = 0
    for item in sport_ngrams:
        if (input_str.find(item)) != -1:
            is_sport = 1
            break
    if is_sport == 1 and len(scores) > 0:
        for score in scores:
            lscore = int(score.split('-')[0])
            rscore = int(score.split('-')[1])
            score_norm = num2words(lscore, lang='vi') + ' ' + num2words(rscore, lang='vi')
            input_str = input_str.replace(score, ' <CARDINAL>' + score + '</CARDINAL> ')
            output_str = output_str.replace(score, ' <CARDINAL>' + score_norm + '</CARDINAL> ')

    return input_str, output_str


def norm_tag_fraction(input_str, output_str):
    """
    Normalize number range.
    """
    input_str = ' ' + input_str + ' '
    output_str = ' ' + output_str + ' '
    p = re.compile(r"(thứ|hơn|gần|:|hạng|được|tới|góp|là|có|lên|bằng|[Cc]hiếm|giảm|tỷ lệ|tỉ lệ|khoảng)\s[0-9]+\s*\/\s*[0-9]+\s")
    temp_str = input_str
    ratio_list = []
    while(p.search(temp_str)):
        ratio = p.search(temp_str)
        x = ratio.group().replace(' / ', '/').replace(' /', '/').replace('/ ', '/')
        ratio_list.append(x.split()[-1])
        temp_str = temp_str[ratio.span()[1]-1:]

    ratio_list = [item for item in ratio_list if int(item.split('/')[0]) < int(item.split('/')[1])]

    if len(ratio_list) > 0:
        # print(str(ratio_list), ' : ', input_str)
        for ratio in ratio_list:
            first_num = ratio.split('/')[0]
            second_num = ratio.split('/')[1]
            if int(second_num) > 10:
                ratio_str = num2words_fixed(first_num) + ' trên ' + num2words_fixed(second_num)
            else:
                ratio_str = num2words_fixed(first_num) + ' phần ' + num2words_fixed(second_num)

            input_str = input_str.replace(ratio, ' <FRACTION>' + ratio + '</FRACTION> ')
            output_str = output_str.replace(ratio, ' <FRACTION>' + ratio_str + '</FRACTION> ')

    return input_str, output_str



def norm_code_type_1(input_str, output_str):
    # pattern = '(?=(\s[a-zA-Z]+[0-9]+\s|\s[0-9]+[a-zA-Z]+\s|\s[a-zA-Z]+[0-9]+[a-zA-Z]+\s))'
    pattern = '(?=(\s[a-zA-Z]+[0-9]+\s|\s[0-9]+[a-zA-Z]+\s|\s[a-zA-Z]+[0-9]+[a-zA-Z]+\s|\s[0-9]+[a-zA-Z]+[0-9]\s))'
    output_str = ' ' + output_str + ' '
    match_out = re.search(pattern, output_str)
    while match_out is not None:
        start_match_out = match_out.start(1)
        end_match_out = match_out.end(1)
        term_out = output_str[start_match_out:end_match_out]
        term_norm_out = term_out.replace(term_out, ' '.join(list(term_out)))
        term_norm_out = re.sub('(?<=\d)\s(?=\d)', '', term_norm_out) # remove space between number
        output_str = replace_str(output_str, start_match_out, end_match_out, term_norm_out, '', '')

        match_out = re.search(pattern, output_str)

    return input_str, output_str

# print(norm_code_type_1('', 'BDC20'))
# print(norm_code_type_1('', '20BDC'))
# print(norm_code_type_1('', 'BDC20BDC'))
# print(norm_code_type_1('', 'BCD20 CD30 B25D'))