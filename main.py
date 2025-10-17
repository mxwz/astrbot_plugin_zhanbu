import asyncio
import json
import os
import random
import time
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Tuple, Union
from PIL import Image

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
# from dataclasses import dataclass
from .xlr import XiaoLiuRen
from .meihua import Meihua, Search_txt, Search_line
from .xlr_shi import xiaoliuren
# from astrbot.core.star.filter.command_group import CommandGroupFilter
# from astrbot.core.star.star_handler import star_handlers_registry


class ResourceError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

    __repr__ = __str__


class EventNotSupport(Exception):
    pass

def all_strings_are_digits(string_list):
    return all(s.isdigit() for s in string_list)
def all_strings_are_numeric(string_list):
    return all(s.isnumeric() for s in string_list)
def all_chinese_chars(strings):
    """
    检查字符串列表中的每个字符串是否都只包含中文字符
    """
    return all(
        all(u'\u4e00' <= char <= u'\u9fa5' for char in string)
        for string in strings
    )
def all_single_chinese_chars(strings):
    """
    检查字符串列表中的每个字符串是否都只包含单个中文字符
    """
    return all(
        len(string) == 1 and (u'\u4e00' <= string <= u'\u9fa5')
        for string in strings
    )

def pick_theme(tarot_path: Path, tarot_official_themes: List[str]) -> str:
    '''
        Random choose a theme from the union of local & official themes
    '''
    sub_themes_dir: List[str] = [
        f.name for f in tarot_path.iterdir() if f.is_dir()]

    if len(sub_themes_dir) > 0:
        return random.choice(list(set(sub_themes_dir).union(tarot_official_themes)))

    return random.choice(tarot_official_themes)


def pick_sub_types(theme: str, tarot_path: Path) -> List[str]:
    '''
        Random choose a sub type of the "theme".
        If it is in official themes, all the sub types are available.
    '''
    all_sub_types: List[str] = ["MajorArcana",
                                "Cups", "Pentacles", "Sowrds", "Wands"]

    if theme == "BilibiliTarot":
        return all_sub_types

    if theme == "TouhouTarot":
        return ["MajorArcana"]

    sub_types: List[str] = [f.name for f in (
        tarot_path / theme).iterdir() if f.is_dir() and f.name in all_sub_types]

    return sub_types


class Tarot:
    def __init__(self, tarot_path: Path):
        self.tarot_path: Path = tarot_path
        self.tarot_json: Path = Path(__file__).parent / "tarot.json"
        self.tarot_official_themes: List[str] = ["BilibiliTarot", "TouhouTarot"]

    def _random_cards(self,
                      all_cards: Dict[str, Dict[str, Dict[str, Union[str, Dict[str, str]]]]],
                      theme: str,
                      num: int = 1
                      ) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        '''
            Iterate the sub directory, get the subset of cards
        '''
        sub_types: List[str] = pick_sub_types(theme, self.tarot_path)

        if len(sub_types) < 1:
            raise ResourceError(f"本地塔罗牌主题 {theme} 为空！请检查资源！")

        subset: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = {
            k: v for k, v in all_cards.items() if v.get("type") in sub_types
        }

        # 2. Random sample the cards according to the num
        cards_index: List[str] = random.sample(list(subset), num)
        cards_info: List[Dict[str, Union[str, Dict[str, str]]]] = [
            v for k, v in subset.items() if k in cards_index]

        return cards_info

    async def _get_text_and_image(self,
                                  theme: str,
                                  card_info: Dict[str,
                                                  Union[str, Dict[str, str]]]
                                  ) -> Tuple[bool, str, bytes]:
        '''
            Get a tarot image & text according to the "card_info"
        '''
        _type: str = card_info.get("type")
        _name: str = card_info.get("pic")
        img_name: str = ""
        img_dir: Path = self.tarot_path / theme / _type

        # Consider the suffix of pictures
        for p in img_dir.glob(_name + ".*"):
            img_name = p.name

        if img_name == "":
            # Since we don't need online resources, raise ResourceError directly
            raise ResourceError(
                f"Tarot image {theme}/{_type}/{_name} doesn't exist! Make sure the type {_type} is complete.")
        else:
            img: Image.Image = Image.open(img_dir / img_name)
            # print(f"[Tarot] {theme}/{_type}/{img_name}")

        # 3. Choose up or down
        name_cn: str = card_info.get("name_cn")
        if random.random() < 0.5:
            # 正位
            meaning: str = card_info.get("meaning").get("up")
            msg = f"「{name_cn}正位」「{meaning}」\n"
        else:
            meaning: str = card_info.get("meaning").get("down")
            msg = f"「{name_cn}逆位」「{meaning}」\n"
            img = img.rotate(180)

        buf = BytesIO()
        img.save(buf, format='png')
        image_bytes = buf.getvalue()

        return True, msg, image_bytes

    async def divine(self, event: AstrMessageEvent, cardType: str) -> List[Tuple[str, bytes]]:
        '''
            General tarot divination.
            1. Choose a theme
            2. Open tarot.json and Random choose a formation
            3. Get the divined cards list and their text
            4. Generate message
        '''
        try:
            import ujson as json
        except ModuleNotFoundError:
            import json

        # 1. Pick a theme randomly
        theme: str = pick_theme(self.tarot_path, self.tarot_official_themes)

        with open(self.tarot_json, 'r', encoding='utf-8') as f:
            content = json.load(f)
            all_cards = content.get("cards")
            all_formations = content.get("formations")

            if cardType in list(all_formations.keys()):
                formation_name = cardType
            else:
                formation_name = random.choice(list(all_formations))
            formation = all_formations.get(formation_name)

        result = [(f"启用{formation_name}，正在洗牌中", None)]

        # 2. Get cards of "cards_num"
        cards_num: int = formation.get("cards_num")
        cards_info_list = self._random_cards(all_cards, theme, cards_num)

        # 3. Get the text of representations
        is_cut: bool = formation.get("is_cut")
        representations: List[Union[str, List[str]]] = random.choice(
            formation.get("representations"))

        # 4. Generate message
        for i in range(cards_num):
            # Select the #i tarot
            if is_cut and i == cards_num - 1:
                msg_header = f"切牌「{representations[i]}」\n"
            else:
                msg_header = f"第{i+1}张牌「{representations[i]}」\n"

            flag, msg_body, image_bytes = await self._get_text_and_image(theme, cards_info_list[i])
            if not flag:
                result.append((msg_body, None))
                break

            result.append((msg_header + msg_body, image_bytes))

            # Add delay between cards except for the last one
            if i < cards_num - 1:
                await asyncio.sleep(random.uniform(1, 2))

        return result

    async def onetime_divine(self) -> tuple[str, bytes]:
        '''
            One-time divination.
        '''
        try:
            import ujson as json
        except ModuleNotFoundError:
            import json

        # 1. Pick a theme randomly
        theme: str = pick_theme(self.tarot_path, self.tarot_official_themes)

        # 2. Get one card ONLY
        with open(self.tarot_json, 'r', encoding='utf-8') as f:
            content = json.load(f)
            all_cards = content.get("cards")
            card_info_list = self._random_cards(all_cards, theme)

        # 3. Get the text and image
        flag, body, image_bytes = await self._get_text_and_image(theme, card_info_list[0])

        return ("回应是：" + body if flag else body, image_bytes)


@register("占卜", "mxwz", "占卜插件", "v1.0.2")
class ZhanBuPlugin(Star):
    def __init__(self, context: Context, config):
        super().__init__(context)
        self.config = config
        self.enable_sent_picture = self.config.get("enable_sent_picture", False)
        self.enable_repost = self.config.get("enable_repost", False)

        self.xlr_manager = XiaoLiuRen()

        self.tarot_path: Path = Path(__file__).parent / "resource"
        self.tarot_manager = Tarot(self.tarot_path)

        # Check if tarot.json exists
        tarot_json_path: Path = Path(__file__).parent / "tarot.json"
        if not tarot_json_path.exists():
            logger.error("塔罗牌插件缺少必要的资源文件 tarot.json，请检查！")

        # Check if resource directory exists
        if not self.tarot_path.exists():
            logger.error("塔罗牌插件缺少必要的资源目录 resource，请检查！")

    @filter.command_group("塔罗牌")
    def tarot(self):
        """塔罗牌相关命令"""
        pass


    @tarot.command("塔罗牌阵")
    async def divine_command(self, event: AstrMessageEvent, cardType: str|None = None):
        """随机选取牌阵进行占卜

        :param cardType: 牌阵(不选择默认随机)
        """
        try:
            messages_and_images = await self.tarot_manager.divine(event, cardType)
            for msg, image_bytes in messages_and_images:
                yield event.plain_result(msg)

                # 如果有图片且启用了发送图片功能
                if image_bytes and self.enable_sent_picture:
                    # 创建临时文件夹（如果不存在）
                    temp_dir = Path(__file__).parent / "temp"
                    temp_dir.mkdir(exist_ok=True)

                    # 生成临时文件路径
                    temp_file = temp_dir / f"tarot_{int(time.time())}_{random.randint(1000, 9999)}.png"

                    # 将图片字节写入临时文件
                    with open(temp_file, "wb") as f:
                        f.write(image_bytes)

                    try:
                        # 发送图片文件
                        yield event.image_result(str(temp_file))
                    finally:
                        # 发送完成后删除临时文件
                        if temp_file.exists():
                            try:
                                os.remove(temp_file)
                            except Exception as e:
                                logger.warning(f"删除临时文件失败: {e}")

                # 在消息之间添加延迟
                await asyncio.sleep(random.uniform(1, 2))

        except ResourceError as e:
            yield event.plain_result(f"资源错误: {e.msg}")
        except Exception as e:
            logger.error(f"占卜过程中出现错误: {e}")
            yield event.plain_result("占卜失败，请稍后再试~")


    @tarot.command("抽卡")
    async def tarot_command(self, event: AstrMessageEvent):
        """得到单张塔罗牌回应"""
        try:
            msg, image_bytes = await self.tarot_manager.onetime_divine()
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(msg)

            if self.enable_sent_picture:
                # 创建临时文件夹（如果不存在）
                temp_dir = Path(__file__).parent / "temp"
                temp_dir.mkdir(exist_ok=True)

                # 生成临时文件路径
                temp_file = temp_dir / f"tarot_{int(time.time())}_{random.randint(1000, 9999)}.png"

                # 将图片字节写入临时文件
                with open(temp_file, "wb") as f:
                    f.write(image_bytes)

                try:
                    # 发送图片文件
                    yield event.image_result(str(temp_file))
                finally:
                    # 发送完成后删除临时文件
                    if temp_file.exists():
                        try:
                            os.remove(temp_file)
                        except Exception as e:
                            logger.warning(f"删除临时文件失败: {e}")

        except ResourceError as e:
            yield event.plain_result(f"资源错误: {e.msg}")
        except Exception as e:
            logger.error(f"抽取塔罗牌过程中出现错误: {e}")
            yield event.plain_result("抽取塔罗牌失败，请稍后再试~")

    @tarot.command("查看牌阵")
    async def tarot_list(self, event: AstrMessageEvent):
        """查看所有适配的塔罗牌阵型"""
        try:
            with open(self.tarot_manager.tarot_json, 'r', encoding='utf-8') as f:
                content = json.load(f)
                all_formations = content.get("formations")
                formation_name = list(all_formations.keys())
            formation_names = "以下是支持的塔罗牌型：\n"
            for id, i in enumerate(formation_name):
                formation_names += f"{id+1}: {i}\n"
            yield event.plain_result(formation_names)
        except ResourceError as e:
            yield event.plain_result(f"资源错误: {e.msg}")
        except Exception as e:
            logger.error(f"查看塔罗牌阵过程中出现错误: {e}")
            yield event.plain_result("查看塔罗牌阵失败，请稍后再试~")

    @filter.command_group("小六壬")
    def xlr(self):
        """小六壬相关命令"""
        pass

    @xlr.command("时辰")
    async def xlr_time(self, event: AstrMessageEvent, simple: str = "简短", problem: str = "无"):
        """时辰排盘

        :param problem: 问题
        :param simple: 是否详细输出，详细/简短
        """
        # texts = self.xlr_manager.xlr(f"/xlr {problem} 2 {simple}")
        texts = xiaoliuren(f"/xlr {problem} 2 {simple}")
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)

    @xlr.command("随机")
    async def xlr_random(self, event: AstrMessageEvent, sc: str = "", simple: str = "简短", problem: str = "无"):
        """随机抽取数字排盘

        :param problem: 问题
        :param sc: 单字时辰，例如"子"
        :param simple: 是否详细输出，0为详细，1为简短
        """
        if sc not in ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']:
            yield event.plain_result("请输入正确的单字时辰，例如“子”")
            return

        # texts = self.xlr_manager.xlr(f"/xlr {problem} 1 {sc} {simple}")
        texts = xiaoliuren(f"/xlr {problem} 1 {sc} {simple}")
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)

    @xlr.command("数字")
    async def xlr_number(self, event: AstrMessageEvent, number: str|None = None, sc: str|None = None, simple: str = "简短", problem: str = "无"):
        """数字排盘

        :param problem: 问题
        :param number: 自定义数字，英文逗号分隔
        :param sc: 单字时辰，例如"子"
        :param simple: 是否详细输出，0为详细，1为简短
        """
        try:
            err = list(map(int, number.split(",")))
            if type(err) != list:
                raise ValueError("请输入三位数字，英文逗号分隔")
            if len(err) != 3:
                raise ValueError("请输入三位数字，英文逗号分隔")
        except ValueError as e:
            yield event.plain_result(f"{e}")
            return
        except Exception as e:
            yield event.plain_result(f"请输入正确的数字，并英文逗号分隔: {e}")
            return
        if sc not in ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']:
            yield event.plain_result("请输入正确的单字时辰，例如“子”")
            return
        # texts = self.xlr_manager.xlr(f"/xlr {problem} 3 {number} {sc} {simple}")
        texts = xiaoliuren(f"/xlr {problem} 3 {number} {sc} {simple}")
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)

    @xlr.command("八卦")
    async def xlr_bauble(self, event: AstrMessageEvent, gua: str):
        """查询八卦内容

        :param gua: 八卦的名字
        """
        if gua not in ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]:
            yield event.plain_result("请输入正确的八卦名称，例如“乾”")
            return
        texts = self.xlr_manager.seach_bagua(gua)
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)

    @filter.command_group("梅花易数")
    def clover(self):
        """梅花易数相关命令"""
        pass

    # 1.时间起数；
    # 2.笔画起数（仅支持两字到六字）；
    # 3.随机数字起数；
    # 4.自定义数字起数;
    # 5.三数起数（第一个数字为上卦，第二个数字为下卦，第三个数字为动爻）

    @clover.command("时间")
    async def clover_time(self, event: AstrMessageEvent, problem: str = "无", gender: str = "男"):
        """以当前农历时间起数

        :param problem: 问题
        :param gender: 性别
        """
        if gender not in ["男", "女"]:
            yield event.plain_result("请输入正确的性别，男/女")
            return

        texts = Meihua(problem, gender, 1)
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)


    @clover.command("笔画")
    async def clover_strokes(self, event: AstrMessageEvent, problem: str = "无", gender: str = "男", strokes: str = "", sc = None):
        """输入两到六个字起数，英文逗号分隔

        :param problem: 问题
        :param gender: 性别
        :param strokes: 输入一个汉字，英文逗号分隔
        :param sc: 单字时辰，例如“子”
        """
        try:
            strokes_list = strokes.split(",")
            if type(strokes_list) != list:
                yield event.plain_result("请输入中文，英文逗号分隔")
                return
            if len(strokes_list) < 2 or len(strokes_list) > 6:
                yield event.plain_result("只能输入两字到六字")
                return
            if not all_chinese_chars(strokes_list):
                yield event.plain_result("只能输入中文")
                return
            if not all_single_chinese_chars(strokes_list):
                yield event.plain_result("只能存在单字")
                return
        except Exception as e:
            yield event.plain_result(f"输入两到六个字起数，英文逗号分隔: {e}")
            return
        if sc not in ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']:
            yield event.plain_result("请输入正确的单字时辰，例如“子”")
            return

        if gender not in ["男", "女"]:
            yield event.plain_result("请输入正确的性别，男/女")
            return


        texts = Meihua(problem, gender, 2, chars=strokes_list, sc=sc)
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)

    @clover.command("随机")
    async def clover_random(self, event: AstrMessageEvent, problem: str = "无", gender: str = "男", num: str = "", sc = None):
        """以随机数字(2~6)起数

        :param problem: 问题
        :param gender: 性别
        :param num: 单个数字，范围是2到6
        :param sc: 单字时辰，例如“子”
        """
        if gender not in ["男", "女"]:
            yield event.plain_result("请输入正确的性别，男/女")
            return
        if not num.isdigit():
            yield event.plain_result("请输入数字")
            return
        if not (2 <= int(num) <= 6):
            yield event.plain_result("请输入数字2~6")
            return
        if sc not in ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']:
            yield event.plain_result("请输入正确的单字时辰，例如“子”")
            return

        texts = Meihua(problem, gender, 3, count=int(num), sc=sc)
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)

    @clover.command("数字")
    async def clover_num(self, event: AstrMessageEvent, problem: str = "无", gender: str = "男", number: str = "", sc = None):
        """以自定义数字起数，不低于两位，不超过六位

        :param problem: 问题
        :param gender: 性别
        :param number: 输入2到6个数字，英文逗号分隔
        :param sc: 单字时辰，例如“子”
        """
        try:
            numbers = list(map(int, number.split(",")))
            if type(numbers) != list:
                raise ValueError("请输入2到6个数字，英文逗号分隔")
            if not (6 >= len(numbers) >= 2):
                raise ValueError("请输入2到6个数字，英文逗号分隔")
        except ValueError as e:
            yield event.plain_result(f"{e}")
            return
        except Exception as e:
            yield event.plain_result(f"请输入正确的数字，并英文逗号分隔: {e}")
            return

        if gender not in ["男", "女"]:
            yield event.plain_result("请输入正确的性别，男/女")
            return
        if sc not in ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']:
            yield event.plain_result("请输入正确的单字时辰，例如“子”")
            return

        texts = Meihua(problem, gender, 4, numbers=numbers, sc=sc)
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)

    @clover.command("三数")
    async def clover_three(self, event: AstrMessageEvent, problem: str = "无", gender: str = "男", number: str = "", use_shichen: str = "是", sc = None):
        """以自定义数字起数，不低于两位，不超过六位

        :param problem: 问题
        :param gender: 性别
        :param number: 输入3个数字，英文逗号分隔。如果输入-1为随机抽取
        :param use_shichen: 是否使用时辰+数字的形式计算动爻，填是/否，否则直接使用数字计算动爻
        :param sc: 单字时辰，例如“子”
        """
        if number == "-1":
            numbers = [random.randint(1, 20) for _ in range(3)]
        else:
            try:
                numbers = list(map(int, number.split(",")))
                if type(numbers) != list:
                    raise ValueError("请输入3个数字，英文逗号分隔")
                if len(numbers) != 3:
                    raise ValueError("请输入3个数字，英文逗号分隔")
            except ValueError as e:
                yield event.plain_result(f"{e}")
                return
            except Exception as e:
                yield event.plain_result(f"请输入正确的数字，并英文逗号分隔: {e}")
                return

        if use_shichen not in ["是", "否"]:
            yield event.plain_result("请输入正确的选项，是/否")
            return
        if gender not in ["男", "女"]:
            yield event.plain_result("请输入正确的性别，男/女")
            return
        if sc not in ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']:
            yield event.plain_result("请输入正确的单字时辰，例如“子”")
            return

        if use_shichen == "是":
            use_shichen = True
        else:
            use_shichen = False

        texts = Meihua(problem, gender, 4, num_up=numbers[0], num_down=numbers[1], num_yao_base=numbers[2], use_shichen=use_shichen, sc=sc)
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)

    @clover.command("64卦")
    async def clover_gua(self, event: AstrMessageEvent, gua: str = "", yao: str = ""):
        """查看64卦象和对应爻辞

        :param gua: 输入64卦名
        :param yao: 输入1~6爻
        """
        if not yao.isdigit():
            yield event.plain_result("请输入数字")
            return

        texts = [Search_txt(gua), Search_line(gua, yao)]
        for text in texts:
            await asyncio.sleep(random.uniform(1, 2))
            yield event.plain_result(text)