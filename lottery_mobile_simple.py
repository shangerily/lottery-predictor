#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大乐透预测系统 - 移动端简化版
不依赖pandas和numpy，使用纯Python实现
"""

import os
import sys
import random
import json
from datetime import datetime, timedelta
from collections import Counter

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window

# 设置窗口大小（移动端适配）
Window.size = (360, 640)

class LotteryData:
    """彩票数据管理类"""
    
    def __init__(self):
        self.data = []
        self.load_sample_data()
    
    def load_sample_data(self):
        """加载示例数据"""
        # 生成一些示例历史数据
        sample_data = [
            {'期号': '24001', '红球': [2, 5, 12, 18, 25], '蓝球': [3, 8]},
            {'期号': '24002', '红球': [7, 14, 19, 28, 33], '蓝球': [1, 12]},
            {'期号': '24003', '红球': [3, 9, 16, 22, 31], '蓝球': [5, 9]},
            {'期号': '24004', '红球': [1, 8, 15, 24, 35], '蓝球': [2, 11]},
            {'期号': '24005', '红球': [6, 11, 17, 26, 32], '蓝球': [4, 7]},
        ]
        self.data = sample_data
    
    def add_data(self, period, red_balls, blue_balls):
        """添加新数据"""
        self.data.append({
            '期号': period,
            '红球': red_balls,
            '蓝球': blue_balls
        })
    
    def get_recent_data(self, count=10):
        """获取最近的数据"""
        return self.data[-count:] if len(self.data) >= count else self.data

class LotteryPredictor:
    """彩票预测器"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def frequency_analysis(self):
        """频率分析预测"""
        recent_data = self.data_manager.get_recent_data(20)
        
        # 统计红球频率
        red_counter = Counter()
        blue_counter = Counter()
        
        for record in recent_data:
            red_counter.update(record['红球'])
            blue_counter.update(record['蓝球'])
        
        # 选择频率最高的号码
        most_common_red = [num for num, _ in red_counter.most_common(10)]
        most_common_blue = [num for num, _ in blue_counter.most_common(6)]
        
        # 随机选择5个红球和2个蓝球
        predicted_red = random.sample(most_common_red, min(5, len(most_common_red)))
        predicted_blue = random.sample(most_common_blue, min(2, len(most_common_blue)))
        
        # 如果不够，随机补充
        while len(predicted_red) < 5:
            num = random.randint(1, 35)
            if num not in predicted_red:
                predicted_red.append(num)
        
        while len(predicted_blue) < 2:
            num = random.randint(1, 12)
            if num not in predicted_blue:
                predicted_blue.append(num)
        
        predicted_red.sort()
        predicted_blue.sort()
        
        return predicted_red, predicted_blue
    
    def random_prediction(self):
        """随机预测"""
        red_balls = sorted(random.sample(range(1, 36), 5))
        blue_balls = sorted(random.sample(range(1, 13), 2))
        return red_balls, blue_balls
    
    def trend_analysis(self):
        """趋势分析预测"""
        recent_data = self.data_manager.get_recent_data(10)
        
        if len(recent_data) < 3:
            return self.random_prediction()
        
        # 分析最近的号码趋势
        recent_red = []
        recent_blue = []
        
        for record in recent_data[-3:]:  # 最近3期
            recent_red.extend(record['红球'])
            recent_blue.extend(record['蓝球'])
        
        # 避免最近出现的号码
        avoid_red = set(recent_red)
        avoid_blue = set(recent_blue)
        
        # 选择不在最近出现的号码
        available_red = [i for i in range(1, 36) if i not in avoid_red]
        available_blue = [i for i in range(1, 13) if i not in avoid_blue]
        
        if len(available_red) >= 5:
            predicted_red = sorted(random.sample(available_red, 5))
        else:
            predicted_red = sorted(random.sample(range(1, 36), 5))
        
        if len(available_blue) >= 2:
            predicted_blue = sorted(random.sample(available_blue, 2))
        else:
            predicted_blue = sorted(random.sample(range(1, 13), 2))
        
        return predicted_red, predicted_blue

class MainWidget(BoxLayout):
    """主界面组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # 初始化数据和预测器
        self.data_manager = LotteryData()
        self.predictor = LotteryPredictor(self.data_manager)
        
        self.build_ui()
    
    def build_ui(self):
        """构建用户界面"""
        # 标题
        title = Label(
            text='大乐透预测系统',
            size_hint_y=None,
            height=50,
            font_size=24,
            bold=True
        )
        self.add_widget(title)
        
        # 预测按钮区域
        button_layout = GridLayout(
            cols=2,
            size_hint_y=None,
            height=120,
            spacing=10
        )
        
        freq_btn = Button(
            text='频率分析\n预测',
            font_size=16
        )
        freq_btn.bind(on_press=self.frequency_predict)
        
        trend_btn = Button(
            text='趋势分析\n预测',
            font_size=16
        )
        trend_btn.bind(on_press=self.trend_predict)
        
        random_btn = Button(
            text='随机\n预测',
            font_size=16
        )
        random_btn.bind(on_press=self.random_predict)
        
        history_btn = Button(
            text='历史\n数据',
            font_size=16
        )
        history_btn.bind(on_press=self.show_history)
        
        button_layout.add_widget(freq_btn)
        button_layout.add_widget(trend_btn)
        button_layout.add_widget(random_btn)
        button_layout.add_widget(history_btn)
        
        self.add_widget(button_layout)
        
        # 预测结果显示区域
        self.result_label = Label(
            text='点击上方按钮开始预测',
            text_size=(None, None),
            halign='center',
            valign='middle',
            font_size=18
        )
        self.add_widget(self.result_label)
        
        # 数据输入区域
        input_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=200,
            spacing=5
        )
        
        input_title = Label(
            text='添加历史数据',
            size_hint_y=None,
            height=30,
            font_size=16,
            bold=True
        )
        input_layout.add_widget(input_title)
        
        # 期号输入
        period_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40
        )
        period_layout.add_widget(Label(text='期号:', size_hint_x=None, width=60))
        self.period_input = TextInput(
            multiline=False,
            hint_text='如: 24006'
        )
        period_layout.add_widget(self.period_input)
        input_layout.add_widget(period_layout)
        
        # 红球输入
        red_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40
        )
        red_layout.add_widget(Label(text='红球:', size_hint_x=None, width=60))
        self.red_input = TextInput(
            multiline=False,
            hint_text='如: 1,5,12,18,25'
        )
        red_layout.add_widget(self.red_input)
        input_layout.add_widget(red_layout)
        
        # 蓝球输入
        blue_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40
        )
        blue_layout.add_widget(Label(text='蓝球:', size_hint_x=None, width=60))
        self.blue_input = TextInput(
            multiline=False,
            hint_text='如: 3,8'
        )
        blue_layout.add_widget(self.blue_input)
        input_layout.add_widget(blue_layout)
        
        # 添加按钮
        add_btn = Button(
            text='添加数据',
            size_hint_y=None,
            height=40
        )
        add_btn.bind(on_press=self.add_data)
        input_layout.add_widget(add_btn)
        
        self.add_widget(input_layout)
    
    def frequency_predict(self, instance):
        """频率分析预测"""
        red, blue = self.predictor.frequency_analysis()
        self.show_prediction_result("频率分析预测", red, blue)
    
    def trend_predict(self, instance):
        """趋势分析预测"""
        red, blue = self.predictor.trend_analysis()
        self.show_prediction_result("趋势分析预测", red, blue)
    
    def random_predict(self, instance):
        """随机预测"""
        red, blue = self.predictor.random_prediction()
        self.show_prediction_result("随机预测", red, blue)
    
    def show_prediction_result(self, method, red_balls, blue_balls):
        """显示预测结果"""
        red_str = ' '.join([f'{num:02d}' for num in red_balls])
        blue_str = ' '.join([f'{num:02d}' for num in blue_balls])
        
        result_text = f"{method}\n\n"
        result_text += f"红球: {red_str}\n"
        result_text += f"蓝球: {blue_str}\n\n"
        result_text += f"预测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        self.result_label.text = result_text
    
    def add_data(self, instance):
        """添加历史数据"""
        try:
            period = self.period_input.text.strip()
            red_text = self.red_input.text.strip()
            blue_text = self.blue_input.text.strip()
            
            if not all([period, red_text, blue_text]):
                self.show_popup("错误", "请填写完整的数据")
                return
            
            # 解析红球
            red_balls = [int(x.strip()) for x in red_text.split(',')]
            if len(red_balls) != 5 or any(x < 1 or x > 35 for x in red_balls):
                self.show_popup("错误", "红球必须是5个1-35之间的数字")
                return
            
            # 解析蓝球
            blue_balls = [int(x.strip()) for x in blue_text.split(',')]
            if len(blue_balls) != 2 or any(x < 1 or x > 12 for x in blue_balls):
                self.show_popup("错误", "蓝球必须是2个1-12之间的数字")
                return
            
            # 添加数据
            self.data_manager.add_data(period, red_balls, blue_balls)
            
            # 清空输入框
            self.period_input.text = ''
            self.red_input.text = ''
            self.blue_input.text = ''
            
            self.show_popup("成功", "数据添加成功")
            
        except ValueError:
            self.show_popup("错误", "请输入正确的数字格式")
        except Exception as e:
            self.show_popup("错误", f"添加数据失败: {str(e)}")
    
    def show_history(self, instance):
        """显示历史数据"""
        recent_data = self.data_manager.get_recent_data(10)
        
        if not recent_data:
            self.show_popup("提示", "暂无历史数据")
            return
        
        history_text = "最近10期历史数据:\n\n"
        for record in recent_data:
            red_str = ' '.join([f'{num:02d}' for num in record['红球']])
            blue_str = ' '.join([f'{num:02d}' for num in record['蓝球']])
            history_text += f"{record['期号']}: {red_str} | {blue_str}\n"
        
        self.show_popup("历史数据", history_text)
    
    def show_popup(self, title, content):
        """显示弹窗"""
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content_label = Label(
            text=content,
            text_size=(300, None),
            halign='left',
            valign='top'
        )
        popup_content.add_widget(content_label)
        
        close_btn = Button(
            text='关闭',
            size_hint_y=None,
            height=40
        )
        popup_content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.9, 0.7)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

class LotteryApp(App):
    """主应用类"""
    
    def build(self):
        return MainWidget()
    
    def get_application_name(self):
        return "大乐透预测系统"

if __name__ == '__main__':
    LotteryApp().run() 