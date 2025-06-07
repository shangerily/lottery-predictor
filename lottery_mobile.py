#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大乐透预测移动端应用
基于Kivy框架，可打包为安卓APK
"""

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.metrics import dp

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
from collections import Counter
import os
import json

class DataManager:
    """数据管理类"""
    
    def __init__(self):
        self.data = None
        self.data_file = "lottery_data.json"
        self.load_default_data()
    
    def load_default_data(self):
        """加载默认数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data_dict = json.load(f)
                self.data = pd.DataFrame(data_dict)
                self.data['date'] = pd.to_datetime(self.data['date'])
            except:
                self.create_sample_data()
        else:
            self.create_sample_data()
    
    def create_sample_data(self):
        """创建示例数据"""
        sample_data = [
            {'period': '24040', 'date': '2024-04-01', 'front_1': 7, 'front_2': 20, 'front_3': 21, 'front_4': 29, 'front_5': 35, 'back_1': 3, 'back_2': 11},
            {'period': '24041', 'date': '2024-04-03', 'front_1': 2, 'front_2': 15, 'front_3': 19, 'front_4': 26, 'front_5': 33, 'back_1': 5, 'back_2': 9},
            {'period': '24042', 'date': '2024-04-06', 'front_1': 8, 'front_2': 12, 'front_3': 18, 'front_4': 24, 'front_5': 31, 'back_1': 2, 'back_2': 7},
            {'period': '24043', 'date': '2024-04-08', 'front_1': 5, 'front_2': 16, 'front_3': 22, 'front_4': 28, 'front_5': 34, 'back_1': 4, 'back_2': 10},
            {'period': '24044', 'date': '2024-04-10', 'front_1': 9, 'front_2': 17, 'front_3': 23, 'front_4': 30, 'front_5': 32, 'back_1': 1, 'back_2': 8}
        ]
        
        self.data = pd.DataFrame(sample_data)
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.save_data()
    
    def save_data(self):
        """保存数据"""
        if self.data is not None:
            data_dict = self.data.copy()
            data_dict['date'] = data_dict['date'].dt.strftime('%Y-%m-%d')
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_dict.to_dict('records'), f, ensure_ascii=False, indent=2)
    
    def add_data(self, period, date, front_numbers, back_numbers):
        """添加新数据"""
        new_row = {
            'period': period,
            'date': date,
            'front_1': front_numbers[0],
            'front_2': front_numbers[1],
            'front_3': front_numbers[2],
            'front_4': front_numbers[3],
            'front_5': front_numbers[4],
            'back_1': back_numbers[0],
            'back_2': back_numbers[1]
        }
        
        if self.data is None:
            self.data = pd.DataFrame([new_row])
        else:
            new_df = pd.DataFrame([new_row])
            new_df['date'] = pd.to_datetime(new_df['date'])
            self.data = pd.concat([self.data, new_df], ignore_index=True)
        
        self.data = self.data.sort_values('date').reset_index(drop=True)
        self.save_data()
        return True

class PredictionEngine:
    """预测引擎"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def statistical_prediction(self, periods=5):
        """统计分析预测"""
        if self.data_manager.data is None or len(self.data_manager.data) < 5:
            return []
        
        data = self.data_manager.data
        predictions = []
        
        # 分析历史频率
        front_cols = ['front_1', 'front_2', 'front_3', 'front_4', 'front_5']
        back_cols = ['back_1', 'back_2']
        
        all_front = []
        all_back = []
        
        for col in front_cols:
            all_front.extend(data[col].tolist())
        for col in back_cols:
            all_back.extend(data[col].tolist())
        
        front_freq = Counter(all_front)
        back_freq = Counter(all_back)
        
        # 获取最新期号
        last_period = int(data['period'].iloc[-1])
        
        for i in range(periods):
            # 基于频率和随机性生成预测
            front_candidates = [num for num, count in front_freq.most_common(15)]
            back_candidates = [num for num, count in back_freq.most_common(8)]
            
            # 添加随机性
            front_numbers = sorted(np.random.choice(front_candidates, 5, replace=False))
            back_numbers = sorted(np.random.choice(back_candidates, 2, replace=False))
            
            predictions.append({
                'period': f"{last_period + i + 1:05d}",
                'front': front_numbers,
                'back': back_numbers
            })
        
        return predictions
    
    def time_series_prediction(self, periods=5):
        """时间序列预测"""
        if self.data_manager.data is None or len(self.data_manager.data) < 5:
            return []
        
        data = self.data_manager.data
        predictions = []
        last_period = int(data['period'].iloc[-1])
        
        front_cols = ['front_1', 'front_2', 'front_3', 'front_4', 'front_5']
        back_cols = ['back_1', 'back_2']
        
        for i in range(periods):
            front_numbers = []
            back_numbers = []
            
            # 对每个位置进行简单的趋势预测
            for col in front_cols:
                series = data[col]
                recent_avg = series.tail(3).mean()
                trend = (series.tail(2).mean() - series.head(2).mean()) / len(series)
                pred = recent_avg + trend * (i + 1)
                pred = max(1, min(35, int(round(pred))))
                front_numbers.append(pred)
            
            for col in back_cols:
                series = data[col]
                recent_avg = series.tail(3).mean()
                trend = (series.tail(2).mean() - series.head(2).mean()) / len(series)
                pred = recent_avg + trend * (i + 1)
                pred = max(1, min(12, int(round(pred))))
                back_numbers.append(pred)
            
            # 确保唯一性
            front_numbers = self.ensure_unique(front_numbers, 1, 35, 5)
            back_numbers = self.ensure_unique(back_numbers, 1, 12, 2)
            
            predictions.append({
                'period': f"{last_period + i + 1:05d}",
                'front': sorted(front_numbers),
                'back': sorted(back_numbers)
            })
        
        return predictions
    
    def ensemble_prediction(self, periods=5):
        """集成预测"""
        stat_pred = self.statistical_prediction(periods)
        ts_pred = self.time_series_prediction(periods)
        
        if not stat_pred or not ts_pred:
            return stat_pred or ts_pred
        
        predictions = []
        last_period = int(self.data_manager.data['period'].iloc[-1])
        
        for i in range(periods):
            # 收集所有预测
            all_front = stat_pred[i]['front'] + ts_pred[i]['front']
            all_back = stat_pred[i]['back'] + ts_pred[i]['back']
            
            # 基于频率选择
            front_freq = Counter(all_front)
            back_freq = Counter(all_back)
            
            # 选择最高频的号码
            front_numbers = [num for num, count in front_freq.most_common(5)]
            back_numbers = [num for num, count in back_freq.most_common(2)]
            
            # 确保数量正确
            if len(front_numbers) < 5:
                remaining = [n for n in range(1, 36) if n not in front_numbers]
                front_numbers.extend(np.random.choice(remaining, 5-len(front_numbers), replace=False))
            
            if len(back_numbers) < 2:
                remaining = [n for n in range(1, 13) if n not in back_numbers]
                back_numbers.extend(np.random.choice(remaining, 2-len(back_numbers), replace=False))
            
            predictions.append({
                'period': f"{last_period + i + 1:05d}",
                'front': sorted(front_numbers[:5]),
                'back': sorted(back_numbers[:2])
            })
        
        return predictions
    
    def ensure_unique(self, numbers, min_val, max_val, count):
        """确保号码唯一性"""
        unique_numbers = list(set(numbers))
        
        while len(unique_numbers) < count:
            candidates = [n for n in range(min_val, max_val + 1) if n not in unique_numbers]
            if candidates:
                unique_numbers.append(np.random.choice(candidates))
            else:
                break
        
        return unique_numbers[:count]

class AddDataPopup(Popup):
    """添加数据弹窗"""
    
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.title = "添加新数据"
        self.size_hint = (0.9, 0.8)
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 期号输入
        period_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        period_layout.add_widget(Label(text="期号:", size_hint_x=0.3))
        self.period_input = TextInput(multiline=False, size_hint_x=0.7)
        period_layout.add_widget(self.period_input)
        main_layout.add_widget(period_layout)
        
        # 日期输入
        date_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        date_layout.add_widget(Label(text="日期:", size_hint_x=0.3))
        self.date_input = TextInput(text=datetime.now().strftime('%Y-%m-%d'), 
                                   multiline=False, size_hint_x=0.7)
        date_layout.add_widget(self.date_input)
        main_layout.add_widget(date_layout)
        
        # 前区号码
        front_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        front_layout.add_widget(Label(text="前区:", size_hint_x=0.3))
        self.front_inputs = []
        for i in range(5):
            input_widget = TextInput(multiline=False, size_hint_x=0.14)
            self.front_inputs.append(input_widget)
            front_layout.add_widget(input_widget)
        main_layout.add_widget(front_layout)
        
        # 后区号码
        back_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        back_layout.add_widget(Label(text="后区:", size_hint_x=0.3))
        self.back_inputs = []
        for i in range(2):
            input_widget = TextInput(multiline=False, size_hint_x=0.35)
            self.back_inputs.append(input_widget)
            back_layout.add_widget(input_widget)
        # 添加空白填充
        back_layout.add_widget(Label(text="", size_hint_x=0.3))
        main_layout.add_widget(back_layout)
        
        # 按钮
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        confirm_btn = Button(text="确定", size_hint_x=0.5)
        confirm_btn.bind(on_press=self.confirm)
        btn_layout.add_widget(confirm_btn)
        
        cancel_btn = Button(text="取消", size_hint_x=0.5)
        cancel_btn.bind(on_press=self.dismiss)
        btn_layout.add_widget(cancel_btn)
        
        main_layout.add_widget(btn_layout)
        
        self.content = main_layout
    
    def confirm(self, instance):
        """确认添加"""
        try:
            period = self.period_input.text.strip()
            date = self.date_input.text.strip()
            
            front_numbers = []
            for input_widget in self.front_inputs:
                num = int(input_widget.text.strip())
                if not (1 <= num <= 35):
                    raise ValueError("前区号码必须在1-35之间")
                front_numbers.append(num)
            
            back_numbers = []
            for input_widget in self.back_inputs:
                num = int(input_widget.text.strip())
                if not (1 <= num <= 12):
                    raise ValueError("后区号码必须在1-12之间")
                back_numbers.append(num)
            
            # 检查重复
            if len(set(front_numbers)) != 5:
                raise ValueError("前区号码不能重复")
            if len(set(back_numbers)) != 2:
                raise ValueError("后区号码不能重复")
            
            # 调用回调函数
            self.callback(period, date, front_numbers, back_numbers)
            self.dismiss()
            
        except ValueError as e:
            error_popup = Popup(title="输入错误", content=Label(text=str(e)), 
                               size_hint=(0.8, 0.3))
            error_popup.open()

class LotteryMobileApp(App):
    """主应用类"""
    
    def build(self):
        self.title = "大乐透预测系统"
        
        # 初始化组件
        self.data_manager = DataManager()
        self.prediction_engine = PredictionEngine(self.data_manager)
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 标题
        title_label = Label(text="大乐透智能预测系统", 
                           font_size=dp(20), 
                           size_hint_y=None, 
                           height=dp(50),
                           bold=True)
        main_layout.add_widget(title_label)
        
        # 数据管理区域
        data_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120))
        
        data_title = Label(text="数据管理", font_size=dp(16), size_hint_y=None, height=dp(30))
        data_frame.add_widget(data_title)
        
        data_btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(5))
        
        add_data_btn = Button(text="添加数据", size_hint_x=0.5)
        add_data_btn.bind(on_press=self.show_add_data_popup)
        data_btn_layout.add_widget(add_data_btn)
        
        refresh_btn = Button(text="刷新数据", size_hint_x=0.5)
        refresh_btn.bind(on_press=self.refresh_data)
        data_btn_layout.add_widget(refresh_btn)
        
        data_frame.add_widget(data_btn_layout)
        
        # 数据统计
        self.data_info_label = Label(text="", size_hint_y=None, height=dp(50))
        data_frame.add_widget(self.data_info_label)
        
        main_layout.add_widget(data_frame)
        
        # 预测控制区域
        predict_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120))
        
        predict_title = Label(text="预测设置", font_size=dp(16), size_hint_y=None, height=dp(30))
        predict_frame.add_widget(predict_title)
        
        # 算法选择
        algo_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        algo_layout.add_widget(Label(text="算法:", size_hint_x=0.3))
        
        self.algo_spinner = Spinner(text="统计分析", 
                                   values=["统计分析"],
                                   size_hint_x=0.7)
        algo_layout.add_widget(self.algo_spinner)
        predict_frame.add_widget(algo_layout)
        
        # 期数选择
        periods_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        periods_layout.add_widget(Label(text="期数:", size_hint_x=0.3))
        
        self.periods_input = TextInput(text="5", multiline=False, size_hint_x=0.7)
        periods_layout.add_widget(self.periods_input)
        predict_frame.add_widget(periods_layout)
        
        main_layout.add_widget(predict_frame)
        
        # 预测按钮
        self.predict_btn = Button(text="开始预测", size_hint_y=None, height=dp(50))
        self.predict_btn.bind(on_press=self.start_prediction)
        main_layout.add_widget(self.predict_btn)
        
        # 结果显示区域
        result_title = Label(text="预测结果", font_size=dp(16), size_hint_y=None, height=dp(30))
        main_layout.add_widget(result_title)
        
        # 滚动视图
        scroll = ScrollView()
        self.result_label = Label(text="点击开始预测查看结果...", 
                                 text_size=(None, None),
                                 halign="left",
                                 valign="top")
        scroll.add_widget(self.result_label)
        main_layout.add_widget(scroll)
        
        # 更新数据信息
        self.update_data_info()
        
        return main_layout
    
    def update_data_info(self):
        """更新数据信息"""
        if self.data_manager.data is not None:
            count = len(self.data_manager.data)
            latest = self.data_manager.data['period'].iloc[-1]
            self.data_info_label.text = f"当前数据: {count} 期 (最新: {latest}期)"
        else:
            self.data_info_label.text = "暂无数据"
    
    def show_add_data_popup(self, instance):
        """显示添加数据弹窗"""
        popup = AddDataPopup(self.add_data_callback)
        popup.open()
    
    def add_data_callback(self, period, date, front_numbers, back_numbers):
        """添加数据回调"""
        try:
            self.data_manager.add_data(period, date, front_numbers, back_numbers)
            self.update_data_info()
            
            success_popup = Popup(title="成功", 
                                 content=Label(text="数据添加成功！"), 
                                 size_hint=(0.8, 0.3))
            success_popup.open()
            Clock.schedule_once(lambda dt: success_popup.dismiss(), 2)
            
        except Exception as e:
            error_popup = Popup(title="错误", 
                               content=Label(text=f"添加失败: {e}"), 
                               size_hint=(0.8, 0.3))
            error_popup.open()
    
    def refresh_data(self, instance):
        """刷新数据"""
        self.data_manager.load_default_data()
        self.update_data_info()
        
        refresh_popup = Popup(title="提示", 
                             content=Label(text="数据已刷新！"), 
                             size_hint=(0.8, 0.3))
        refresh_popup.open()
        Clock.schedule_once(lambda dt: refresh_popup.dismiss(), 1)
    
    def start_prediction(self, instance):
        """开始预测"""
        if self.data_manager.data is None or len(self.data_manager.data) < 5:
            error_popup = Popup(title="错误", 
                               content=Label(text="数据不足，至少需要5期数据"), 
                               size_hint=(0.8, 0.3))
            error_popup.open()
            return
        
        self.predict_btn.text = "预测中..."
        self.predict_btn.disabled = True
        
        threading.Thread(target=self.run_prediction, daemon=True).start()
    
    def run_prediction(self):
        """运行预测"""
        try:
            periods = int(self.periods_input.text)
            predictions = self.prediction_engine.statistical_prediction(periods)
            
            Clock.schedule_once(lambda dt: self.display_predictions(predictions), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.prediction_error(str(e)), 0)
    
    def display_predictions(self, predictions):
        """显示预测结果"""
        self.predict_btn.text = "开始预测"
        self.predict_btn.disabled = False
        
        if not predictions:
            self.result_label.text = "预测失败，请检查数据"
            return
        
        result_text = "统计分析预测结果\n"
        result_text += "=" * 30 + "\n"
        result_text += f"预测时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for pred in predictions:
            front_str = " ".join([f"{num:02d}" for num in pred['front']])
            back_str = " ".join([f"{num:02d}" for num in pred['back']])
            result_text += f"{pred['period']}期: {front_str} + {back_str}\n"
        
        result_text += "\n投注建议:\n"
        result_text += "• 理性购彩，量力而行\n"
        result_text += "• 预测仅供参考\n"
        
        self.result_label.text = result_text
        self.result_label.text_size = (300, None)
    
    def prediction_error(self, error_msg):
        """预测错误处理"""
        self.predict_btn.text = "开始预测"
        self.predict_btn.disabled = False
        
        error_popup = Popup(title="预测错误", 
                           content=Label(text=f"预测失败: {error_msg}"), 
                           size_hint=(0.8, 0.4))
        error_popup.open()

if __name__ == "__main__":
    LotteryMobileApp().run() 