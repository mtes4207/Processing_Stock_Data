#%%
import pandas as pd
import os
import csv
from functools import partial


RED = '#ffbfbf'
BLUE = '#c3e3fa'
GREEN = '#defac3'
WHITE = '#ffffff'


def repeat_change_block_color(v, k, color):
    if v in k.tolist():
        repeat = True
    else:
        repeat = False
    return 'background-color: %s'%color if repeat else ''

def color_define(row):
    if row == 'Red':
        color = RED
    elif row == 'Blue':
        color = BLUE
    elif row == 'Green':
        color = GREEN
    else:
        color = WHITE

    return 'background-color: %s'%color

class ProcessingTransectionData:

    def __init__(self, csv_folder, output_path, head_num=30):
        self.processing_dictionary  = {"Credit":dict({}), "FNBS":dict({})}
        self.processing_dict_df(csv_folder, head_num)
        self.filter_credit_df(output_path)
        self.filter_FNBS_df(output_path)
        print('Processing Data Finish ')

    def processing_FNBS_data(self, path):
        csv_file = open(path, "r")
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for i in csv_reader:
            if len(i) != 13:
                continue
            data.append(i)
        df = pd.DataFrame(data[2:], columns=data[1])
        df["證券代號"] = df["證券代號"].apply(lambda x: x.replace("=", "").replace("\"", ""))
        df = pd.concat([df.iloc[:, 1:3], df.iloc[:, -4:]], axis=1)
        df = df.drop([""], axis=1)
        return df

    def processing_Credit_data(self, path):
        csv_file = open(path, "r")
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for i in csv_reader:
            if len(i) != 7:
                continue
            data.append(i)
        df = pd.DataFrame(data[1:], columns=data[0])
        df["證券代號"] = df["證券代號"].apply(lambda x: x.replace("=", "").replace("\"", ""))
        df = df.drop([""], axis=1)
        return df

    def processing_dict_df(self, csv_folder, head_num):
        for file_name in os.listdir(csv_folder):
            file_path = os.path.join(csv_folder, file_name)
            if "FNBS" in file_name:
                df = self.processing_FNBS_data(file_path)
                self.processing_dictionary ["FNBS"][file_name.split("_")[2].strip(".csv")] = df
                
            elif "Credit" in file_name:
                df = self.processing_Credit_data(file_path)
                self.processing_dictionary ["Credit"][file_name.split("_")[2].strip(".csv")] = df

        if len(self.processing_dictionary ["Credit"]) != 2:
            print('Credit data no enough 2 or exceed to analyze')
            exit()

        if len(self.processing_dictionary ["FNBS"]) != 2:
            print('FNBS data no enough 2 or exceed to analyze')
            exit()

        ### Sort by date
        key = sorted(self.processing_dictionary["Credit"].keys(), reverse=True)
        self.day_1st = key[0]
        self.day_2nd = key[1]

        ### DataFrame Procssing
        self.df_credit_day_1st = self.processing_dictionary ["Credit"][self.day_1st].head(head_num)
        self.df_credit_day_2nd = self.processing_dictionary ["Credit"][self.day_2nd].head(head_num)
        self.df_fnbs_day_1st = self.processing_dictionary ["FNBS"][self.day_1st].head(head_num)
        self.df_fnbs_day_2nd = self.processing_dictionary ["FNBS"][self.day_2nd].head(head_num)

        a = self.processing_dictionary ["Credit"][self.day_1st]
        b = self.processing_dictionary ["FNBS"][self.day_1st]

        self.sell_df_credit_day_1st = a[a["買賣超股數"].str.contains("-")]
        self.sell_df_fnbs_day_1st = b[b["買賣超股數"].str.contains("-")]

    # 投信
    def filter_credit_df(self, output_path):
        credit_output_df = self.df_credit_day_1st.copy()
        credit_output_df['Space'] = ''
        credit_output_df['Color'] = ''
        credit_output_df['Define'] = ''
        credit_output_df.loc[:2, 'Color'] = ['Red', 'Blue', 'Green']
        credit_output_df.loc[:2, 'Define'] = ['Date : %s 外資與投信都買超'%self.day_1st, 
                                              'Date : %s and %s 投信都買超'%(self.day_1st, self.day_2nd), 
                                              'Date : %s 投信買超 外資賣超'%self.day_1st]


        save_path = os.path.join(output_path, "投信買賣%s.xlsx"%self.day_1st)
        red_block = partial(repeat_change_block_color, k=self.df_fnbs_day_1st["證券名稱"], color=RED)
        blue_block = partial(repeat_change_block_color, k=self.df_credit_day_2nd["證券名稱"], color=BLUE)
        green_block = partial(repeat_change_block_color, k=self.sell_df_fnbs_day_1st["證券名稱"], color=GREEN)
        credit_output_df.style.applymap(green_block, subset=["證券名稱"]).applymap(blue_block, subset=["證券名稱"]).applymap(red_block, subset=["證券名稱"]).applymap(color_define, subset=["Color"]).to_excel(save_path, index=False)

    # 外資
    def filter_FNBS_df(self, output_path):
        fnbs_output_df = self.df_fnbs_day_1st.copy()
        fnbs_output_df['Space'] = ''
        fnbs_output_df['Color'] = ''
        fnbs_output_df['Define'] = ''
        fnbs_output_df.loc[:2, 'Color'] = ['Red', 'Blue', 'Green']
        fnbs_output_df.loc[:2, 'Define'] = ['Date : %s 外資與投信都買超'%self.day_1st, 
                                            'Date : %s and %s 外資都買超'%(self.day_1st, self.day_2nd), 
                                            'Date : %s 外資買超 投信賣超'%self.day_1st]

        save_path = os.path.join(output_path, "外資買賣%s.xlsx"%self.day_1st)
        red_block = partial(repeat_change_block_color, k=self.df_credit_day_1st["證券名稱"], color=RED)
        blue_block = partial(repeat_change_block_color, k=self.df_fnbs_day_2nd["證券名稱"], color=BLUE)
        green_block = partial(repeat_change_block_color, k=self.sell_df_credit_day_1st["證券名稱"], color=GREEN)
        fnbs_output_df.style.applymap(green_block, subset=["證券名稱"]).applymap(blue_block, subset=["證券名稱"]).applymap(red_block, subset=["證券名稱"]).applymap(color_define, subset=["Color"]).to_excel(save_path, index=False)



