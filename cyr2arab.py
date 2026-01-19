#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈萨克语西里尔文→阿拉伯变体转换器
Kazakh Cyrillic to Arabic Script Converter
"""

import re
import json
from typing import Dict, Set


class CyrillicToArabicConverter:
    """哈萨克语西里尔文到阿拉伯变体转换器"""
    
    def __init__(self):
        # 海木宰符号
        self.HAMZA = '\u0674'  # ٴ
        
        # 专有名词词典（中文人名地名）
        self.PROPER_NOUNS = {
            # 中国领导人
            'си': 'شي', 'цзиньпин': 'جينپيڭ', 'си цзиньпин': 'شي جينپيڭ',
            'ли цян': 'لي چياڭ', 'ли': 'لي', 'цян': 'چياڭ',
            'чжао лэцзи': 'جاۋ لىجي', 'чжао': 'جاۋ', 'лэцзи': 'لىجي',
            'ван хунин': 'ۋاڭ حۋنيڭ', 'ван': 'ۋاڭ', 'хунин': 'حۋنيڭ',
            'цай ци': 'ساي چي', 'цай': 'ساي', 'ци': 'چي',
            'дин сюэсян': 'ديڭ شۋەشياڭ', 'дин': 'ديڭ', 'сюэсян': 'شۋەشياڭ',
            'ли си': 'لي شي',
            'шужи': 'شۋجي',
            # 地名
            'қазақстан': 'قازاقستان', 'алматы': 'الماتى', 'астана': 'استانا',
            'шымкент': 'شىمكەنت', 'жұңго': 'جۇڭگو',
            'чанцзян': 'چاڭجياڭ', 'чанцзянның': 'چاڭجياڭنىڭ',
            'пекин': 'بەيجيڭ',
            # 机构名
            'орталық комитет': 'ورتالىق كوميتەت'
        }
        
        # 常用词词典（包含特殊海木宰规则的词）
        self.COMMON_WORDS = {
            'сөз': f'{self.HAMZA}سوز',
            'біздің': f'{self.HAMZA}بىزدىڭ',
            'отанымыз': 'وتانىمىز',
            'өте': f'{self.HAMZA}وتە',  # 有е，词首ө → 加海木宰
            'көрікті': 'كورىكتى',
            'өмірімізді': 'ومىرىمىزدى',
            'өзгертеді': 'وزگەرتەدى',
            'білім': f'{self.HAMZA}بىلىم',
            'мен': 'مەن',
            'ғылым': 'عىلىم',
            'дамудың': 'دامۋدىڭ',
            'кілті': 'كىلتى',
            # бір 是前元音词，无信号字母，必须加海木宰
            'бір': f'{self.HAMZA}بىر',
            'әр': f'{self.HAMZA}ار',
            'іс': f'{self.HAMZA}ىس',
            # 新增常用词
            'өз': f'{self.HAMZA}وز',
            'үшін': f'{self.HAMZA}ۇشىن',
            'тіл': f'{self.HAMZA}تىل',
            'өмір': f'{self.HAMZA}ومىر',
            'әнші': f'{self.HAMZA}انشى',
            # 注意：өнер 系列词不再需要添加到词典
            # 新规则会自动处理：词首 ө/ү/і + 无к/г → 加海木宰
            # 复合词（首音节硬音，不加海木宰）
            'баспасөз': 'باسپاسوز',
            # 【修复】复合词后缀和谐问题（硬音词根+软音信号灯后缀）
            'емхана': 'ەمحانا',  # 软音词根 ем + 硬音后缀 -хана
            'өнерпаз': f'{self.HAMZA}ونەرپاز',  # 软音词根 өнер + 硬音后缀 -паз（词首ө → 加海木宰）
            'еңбекқор': 'ەڭبەكقور',  # 软音词根 еңбек + 硬音后缀 -қор
            'арбакеш': 'ارباكەش',  # 硬音词根 арба + 软音后缀 -кеш
            'талапкер': 'تالاپكەر',  # 硬音词根 талап + 软音后缀 -кер
            'суретші': 'سۋرەتشى',  # 软音后缀 -ші 在硬音环境下的还原
            'жауынгер': 'جاۋىنگەر',  # 硬音词根 жауын + 软音信号灯后缀 -гер
            # 【新增】借词（特殊映射）
            'бюджет': 'بۋدجەت',  # 借词：ю → ۋ
            'диагноз': 'دىياگنوز',  # 借词：и → ىي
            'токио': 'توكىيو',  # 地名：и → ىي
            'тиісінше': 'تىيىسىنشە',  # 原生词：и → ىي
            # 【新增】前软后硬的转折词
            'бірақ': 'بىراق',  # 前软后硬的转折连词
            # 【新增】软音词根+硬音后缀 -хана 的复合词
            'дәріхана': 'دارىحانا',  # 软音 дәрі + 硬音后缀 -хана
            # 【新增】借词特殊映射
            'сияз': 'سىيەز',  # 借词中的 и 与哈语 я 的特殊拼写
            'қияр': 'قىيار',  # 硬音还原：ия → ىيا
            'экологиялық': 'ەكولوگىيالىق',  # 借词：ия → ىيا
            # 【新增】带连字符的地名
            'нью-йорк': 'نىيۋ-يورك'  # 带连字符的混合元音地名
        }
        
        # 外来语辅音标记（非哈萨克原生辅音）
        self.LOANWORD_CONSONANTS: Set[str] = {'ф', 'Ф', 'в', 'В', 'ц', 'Ц', 'ч', 'Ч'}
        
        # 常见外来语后缀模式
        self.LOANWORD_SUFFIXES = [
            'ция', 'сия', 'ия', 'ология', 'графия', 'логия', 'ика', 'изм'
        ]
        
        # 词首И开头的原生哈萨克词（需要特殊处理海木宰）
        # 这些词的И实际上代表前元音，应加海木宰
        self.I_INITIAL_NATIVE_WORDS: Set[str] = {
            'иіс', 'ине', 'ит', 'ию', 'иір', 'иіл', 'ирі', 'иық', 'ин'
        }
        
        # 特殊复合词前缀（软音前缀+硬音词根）
        # 这些前缀后面跟硬音词根时，整词按硬音处理
        self.SOFT_PREFIXES_WITH_HARD_ROOT = {
            'бес': True,   # 五（如 бесжылдық）
            'екі': True,   # 二
            'жеті': True,  # 七
            'сегіз': True, # 八
            'тоғыз': True, # 九（虽然是硬音，但保留以防）
        }
        
        # 基础辅音映射
        self.CONSONANTS = {
            'б': 'ب', 'Б': 'ب',
            'в': 'ۆ', 'В': 'ۆ',
            'г': 'گ', 'Г': 'گ',
            'ғ': 'ع', 'Ғ': 'ع',
            'д': 'د', 'Д': 'د',
            'ж': 'ج', 'Ж': 'ج',
            'з': 'ز', 'З': 'ز',
            'й': 'ي', 'Й': 'ي',
            'к': 'ك', 'К': 'ك',
            'қ': 'ق', 'Қ': 'ق',
            'л': 'ل', 'Л': 'ل',
            'м': 'م', 'М': 'م',
            'н': 'ن', 'Н': 'ن',
            'ң': 'ڭ', 'Ң': 'ڭ',
            'п': 'پ', 'П': 'پ',
            'р': 'ر', 'Р': 'ر',
            'с': 'س', 'С': 'س',
            'т': 'ت', 'Т': 'ت',
            'ф': 'ف', 'Ф': 'ف',
            'х': 'ح', 'Х': 'ح',
            'һ': 'ھ', 'Һ': 'ھ',
            'ч': 'چ', 'Ч': 'چ',
            'ш': 'ش', 'Ш': 'ش'
        }
        
        # 元音映射（不包括И，И需要特殊处理）
        self.VOWELS = {
            'а': 'ا', 'А': 'ا',
            'ә': 'ا', 'Ә': 'ا',
            'е': 'ە', 'Е': 'ە',
            'о': 'و', 'О': 'و',
            'ө': 'و', 'Ө': 'و',
            'у': 'ۋ', 'У': 'ۋ',
            'ұ': 'ۇ', 'Ұ': 'ۇ',
            'ү': 'ۇ', 'Ү': 'ۇ',
            'ы': 'ى', 'Ы': 'ى',
            'і': 'ى', 'І': 'ى',
            'э': 'ە', 'Э': 'ە'
        }
        
        # 特殊组合
        self.COMBINATIONS = {
            'ц': 'تس', 'Ц': 'تس',
            'щ': 'شش', 'Щ': 'شش',
            'ю': 'يۋ', 'Ю': 'يۋ',
            'я': 'يا', 'Я': 'يا',
            'ё': 'يو', 'Ё': 'يو'
        }
        
        # 前元音集合
        self.FRONT_VOWELS: Set[str] = {'ә', 'Ә', 'е', 'Е', 'і', 'І', 'ө', 'Ө', 'ү', 'Ү'}
        
        # 后元音集合
        self.BACK_VOWELS: Set[str] = {'а', 'А', 'о', 'О', 'ұ', 'Ұ', 'ы', 'Ы', 'у', 'У'}
        
        # 所有元音集合（用于首音节检测）
        self.ALL_VOWELS: Set[str] = self.FRONT_VOWELS | self.BACK_VOWELS | {'и', 'И', 'э', 'Э', 'ю', 'Ю', 'я', 'Я', 'ё', 'Ё'}
        
        # 海木宰信号字母（阿拉伯文中自带前元音属性的字母）
        # 当转换结果中包含这些字母时，禁止使用海木宰
        self.HAMZA_SIGNAL_ARABIC: Set[str] = {'ك', 'گ', 'ە'}
        
        # 西里尔文中对应的信号字母（用于预判）
        self.HAMZA_SIGNAL_CYRILLIC: Set[str] = {'к', 'К', 'г', 'Г', 'е', 'Е'}
        
        # 标点符号映射
        self.PUNCTUATION = {
            ',': '،',  # 西里尔逗号 → 阿拉伯逗号
            '.': '.',
            ':': ':',
            ';': '؛',
            '?': '؟',
            '!': '!'
        }
    
    def is_front_vowel_word(self, word: str) -> bool:
        """判断词是否为前元音词"""
        word_lower = word.lower()
        return any(char in self.FRONT_VOWELS for char in word_lower)
    
    def get_initial_harmony(self, word: str) -> str:
        """获取首音节的音性（首音节优先级逻辑）
        
        根据第一个出现的元音来判定词的音性，而非扫描全词。
        这对于复合词（如 баспасөз = баспа + сөз）特别重要。
        
        特殊处理：
        1. 强辅音信号优先级最高（Қ/Ғ→硬音，К/Г→软音）
        2. 词首И开头的原生词视为前元音
        3. 软音数词前缀+硬音词根的复合词，检测词根音性
        """
        word_lower = word.lower()
        
        # 【优化点1】强辅音信号拦截优先级最高
        # Қ/Ғ 永远出现在硬音词，К/Г 永远出现在软音词
        # 这比元音判定更可靠，尤其是处理含有中性元音И的词
        if any(c in 'қғ' for c in word_lower):
            return 'back'  # 硬音
        if any(c in 'кг' for c in word_lower):
            return 'front'  # 软音
        
        # 特殊处理：词首И开头的原生哈萨克词
        if word_lower in self.I_INITIAL_NATIVE_WORDS:
            return 'front'
        
        # 特殊处理：软音数词前缀+硬音词根的复合词
        for prefix in self.SOFT_PREFIXES_WITH_HARD_ROOT:
            if word_lower.startswith(prefix) and len(word_lower) > len(prefix):
                # 检查词根部分的首元音
                root = word_lower[len(prefix):]
                for char in root:
                    if char in self.FRONT_VOWELS:
                        return 'front'
                    elif char in self.BACK_VOWELS:
                        return 'back'
        
        # 标准逻辑：找第一个元音
        for char in word_lower:
            if char in self.FRONT_VOWELS:
                return 'front'
            elif char in self.BACK_VOWELS:
                return 'back'
        return 'back'  # 默认后元音
    
    def is_i_initial_native(self, word: str) -> bool:
        """判断是否为词首И开头的原生哈萨克词"""
        return word.lower() in self.I_INITIAL_NATIVE_WORDS
    
    def is_loanword(self, word: str) -> bool:
        """判断是否为外来语
        
        外来语特征：
        1. 包含非哈萨克原生辅音（ф, в, ц, ч）
        2. 符合常见外来语后缀模式（-ция, -ия, -ология 等）
        3. 【优化A】元音丛（Hiatus）：哈萨克语原生词禁止元音连写
        4. 【优化B】三辅音连缀：原生词很少出现连续三个辅音
        """
        word_lower = word.lower()
        
        # 词首И原生词优先排除
        if word_lower in self.I_INITIAL_NATIVE_WORDS:
            return False
        
        # 检查外来语辅音
        if any(char in self.LOANWORD_CONSONANTS for char in word):
            return True
        
        # 检查外来语后缀
        for suffix in self.LOANWORD_SUFFIXES:
            if word_lower.endswith(suffix):
                return True
        
        # 【优化A】元音丛检测：哈萨克语原生词禁止元音连写
        # 注意：排除 и+і 和 і+и 的组合，这在哈萨克语中是合法的
        # 先移除合法的 иі 和 іи 组合，再检测
        temp_word = word_lower.replace('иі', '_').replace('іи', '_')
        if re.search(r'[аәеоөұүіыиэ]{2,}', temp_word):
            return True
        
        # 【优化B】三辅音连缀检测：原生词很少出现连续三个辅音
        # 定义元音集合用于检测
        vowels = set('аәеоөұүіыиэуюяё')
        consonant_count = 0
        for char in word_lower:
            if char.isalpha() and char not in vowels:
                consonant_count += 1
                if consonant_count >= 3:
                    return True
            else:
                consonant_count = 0
        
        return False
    
    def has_hamza_signal(self, word: str) -> bool:
        """判断西里尔词中是否包含海木宰信号字母（к, г, е）"""
        return any(char in self.HAMZA_SIGNAL_CYRILLIC for char in word)
    
    def has_hamza_signal_arabic(self, arabic_word: str) -> bool:
        """判断阿拉伯文中是否包含海木宰信号字母（ك, گ, ە）"""
        return any(char in self.HAMZA_SIGNAL_ARABIC for char in arabic_word)
    
    def apply_hamza_rule(self, arabic_word: str, word: str) -> str:
        """应用海木宰规则（后处理）
        
        新规则（按优先级）：
        1. 外来语 → 禁止海木宰
        2. 词首И开头的原生词 → 加海木宰（特殊处理）
        3. 全局к/г信号扫描 → 禁止海木宰（优先级最高）
        4. 【新规则】е信号处理：
           - 有е + 词首ө/ү/і → 加海木宰
           - 有е + 词首非ө/ү/і → 不加海木宰
        5. 无е + 词首ө/ү/і → 加海木宰
        6. 首音节为后元音 → 禁止海木宰
        7. 首音节为前元音且无е → 加海木宰
        """
        is_loanword = self.is_loanword(word)
        is_i_native = self.is_i_initial_native(word)
        
        # 1. 外来语强制不加海木宰
        if is_loanword:
            return arabic_word.replace(self.HAMZA, '')
        
        # 2. 词首И开头的原生词，强制加海木宰
        if is_i_native:
            if not arabic_word.startswith(self.HAMZA):
                return self.HAMZA + arabic_word
            return arabic_word
        
        # 3. 全局к/г信号扫描（优先级最高）
        has_k_or_g = any(char in 'кКгГ' for char in word)
        if has_k_or_g:
            return arabic_word.replace(self.HAMZA, '')
        
        # 4. 【新规则】е信号处理
        word_lower = word.lower()
        has_e = 'е' in word_lower or 'Е' in word
        
        if has_e:
            # 有е的情况
            if word_lower and word_lower[0] in 'өүі':
                # 有е + 词首ө/ү/і → 加海木宰
                if not arabic_word.startswith(self.HAMZA):
                    return self.HAMZA + arabic_word
                return arabic_word
            else:
                # 有е + 词首非ө/ү/і → 不加海木宰
                return arabic_word.replace(self.HAMZA, '')
        
        # 5. 无е + 词首ө/ү/і → 加海木宰
        if word_lower and word_lower[0] in 'өүі':
            if not arabic_word.startswith(self.HAMZA):
                return self.HAMZA + arabic_word
            return arabic_word
        
        # 6. 首音节为后元音 → 禁止海木宰
        initial_harmony = self.get_initial_harmony(word)
        if initial_harmony == 'back':
            return arabic_word.replace(self.HAMZA, '')
        
        # 7. 首音节为前元音且无е → 加海木宰
        if initial_harmony == 'front':
            if not arabic_word.startswith(self.HAMZA):
                return self.HAMZA + arabic_word
            return arabic_word
        
        return arabic_word
    
    def convert_word(self, word: str) -> str:
        """转换单词"""
        if not word:
            return word
        
        # 检查专有名词词典
        word_lower = word.lower()
        if word_lower in self.PROPER_NOUNS:
            return self.PROPER_NOUNS[word_lower]
        
        # 检查常用词词典（直接返回词典值，不再应用海木宰规则）
        if word_lower in self.COMMON_WORDS:
            return self.COMMON_WORDS[word_lower]
        
        # 使用首音节音性判断（而非全词）
        initial_harmony = self.get_initial_harmony(word)
        is_front = initial_harmony == 'front'
        result = []
        
        # 检查是否是借词（用于特殊处理）
        is_loanword = self.is_loanword(word)
        
        i = 0
        while i < len(word):
            char = word[i]
            char_lower = char.lower()
            
            # 跳过软硬音符（ь 和 ъ 不转换）
            if char_lower in ('ь', 'ъ'):
                i += 1
                continue
            
            # 处理 ю - 在借词中 ю 通常是 /u/ 音，写作 ۋ
            # 在原生词中 ю 是 /ju/ 音，写作 يۋ
            if char_lower == 'ю':
                if is_loanword:
                    result.append('ۋ')
                else:
                    result.append('يۋ')
                i += 1
                continue
            
            # 处理其他特殊组合（ц, щ, ё）- 注意：я 需要特殊处理
            if char_lower in ('ц', 'щ', 'ё'):
                result.append(self.COMBINATIONS[char_lower])
                i += 1
                continue
            
            # 处理 я - 特殊情况：如果前面是 и，则 я 只映射为 ا（因为 и 已经提供了 ي）
            if char_lower == 'я':
                # 检查前一个字符是否是 и
                if i > 0 and word[i-1].lower() == 'и':
                    result.append('ا')
                else:
                    result.append('يا')
                i += 1
                continue
            
            # 处理И - 在哈萨克语中，и 总是代表 /ij/ 音，写作 ىي
            # 无论前后元音，и 都应该转换为 ىي
            if char_lower == 'и':
                result.append('ىي')
                i += 1
                continue
            
            # 处理辅音
            if char in self.CONSONANTS:
                result.append(self.CONSONANTS[char])
                i += 1
                continue
            
            # 处理元音
            if char in self.VOWELS:
                result.append(self.VOWELS[char])
                i += 1
                continue
            
            # 其他字符保持不变
            result.append(char)
            i += 1
        
        # 应用海木宰规则（后处理）
        arabic_result = ''.join(result)
        return self.apply_hamza_rule(arabic_result, word)
    
    def convert_compound_word(self, word: str) -> str:
        """转换可能包含连字符的复合词"""
        if not word:
            return word
        
        # 先检查整个词（包括连字符）是否在词典中
        word_lower = word.lower()
        if word_lower in self.PROPER_NOUNS:
            return self.PROPER_NOUNS[word_lower]
        if word_lower in self.COMMON_WORDS:
            return self.COMMON_WORDS[word_lower]
        
        # 如果包含连字符，分别转换每个部分
        if '-' in word:
            parts = word.split('-')
            converted_parts = [self.convert_word(part) for part in parts]
            return '-'.join(converted_parts)
        
        # 否则直接转换
        return self.convert_word(word)
    
    def convert(self, text: str) -> str:
        """转换文本"""
        # 先转换标点符号
        for cyr, arab in self.PUNCTUATION.items():
            text = text.replace(cyr, arab)
        
        # 按词分割并转换（包括ъь以便在convert_word中跳过，支持连字符复合词）
        pattern = r'[а-яәіңғүұқөһёэъьА-ЯӘІҢҒҮҰҚӨҺЁЭЪЬ]+(?:-[а-яәіңғүұқөһёэъьА-ЯӘІҢҒҮҰҚӨҺЁЭЪЬ]+)*'
        return re.sub(pattern, lambda m: self.convert_compound_word(m.group(0)), text)


def main():
    """主函数"""
    converter = CyrillicToArabicConverter()
    
    print("=" * 60)
    print("哈萨克语西里尔文→阿拉伯变体转换器")
    print("Kazakh Cyrillic to Arabic Script Converter")
    print("=" * 60)
    
    # 测试示例
    test_cases = [
        "қазақстан",
        "сәлем",
        "кітап",
        "мектеп",
        "достық",
        "тәуелсіздік",
        "өкіз",
        "әліппе",
        "білім",
        "ғылым"
    ]
    
    print("\n转换示例：")
    print("-" * 60)
    for test in test_cases:
        converted = converter.convert(test)
        print(f"{test:20} → {converted}")
    
    print("\n" + "=" * 60)
    print("交互模式（输入 'quit' 或 'exit' 退出）")
    print("=" * 60)
    
    while True:
        try:
            text = input("\n请输入西里尔文本: ").strip()
            if text.lower() in ('quit', 'exit', ''):
                break
            result = converter.convert(text)
            print(f"转换结果: {result}")
        except KeyboardInterrupt:
            print("\n\n程序已退出")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == '__main__':
    main()
