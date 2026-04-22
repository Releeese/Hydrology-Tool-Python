import csv
import pandas as pd
import os

def print_runtime_directory_info():
    """打印当前运行路径及该路径下的文件/文件夹列表。"""
    current_dir = os.getcwd()
    print(f"📁 当前运行路径: {current_dir}")
    print("📄 当前路径下的内容:")
    for name in sorted(os.listdir(current_dir)):
        full_path = os.path.join(current_dir, name)
        item_type = "[DIR]" if os.path.isdir(full_path) else "[FILE]"
        print(f"   {item_type} {name}")
    print("-" * 30)

def process_hydrology_data(file_path):
    """
    水文流域参数自动处理工具
    功能:读取GIS导出的流域CSV,进行面积统计、分级并生成报告
    """
    print(f"🚀 正在处理文件: {file_path}")
    
    # 1. 读取数据
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return

    # 2. 数据清洗：确保列名整洁 (处理可能存在的空格)
    df.columns = df.columns.str.strip()
    
    # 3. 核心逻辑：根据面积自动划分流域等级 (这在水文规划中很常见)
    # 假设：面积 > 100 为大流域，10-100 为中型，< 10 为小型
    def classify_area(area):
        if area > 100: return '大型流域'
        elif area > 10: return '中型流域'
        else: return '小型/支流'

    df['Scale_Type'] = df['Area-km2'].apply(classify_area)

    # 4. 统计汇总
    total_area = df['Area-km2'].sum()
    sub_count = len(df)
    avg_area = df['Area-km2'].mean()

    print("-" * 30)
    print(f"📊 流域统计摘要:")
    print(f"   - 总子流域数量: {sub_count}")
    print(f"   - 总汇水面积: {total_area:.2f} km²")
    print(f"   - 平均子流域面积: {avg_area:.2f} km²")
    print("-" * 30)

    # 5. 导出处理后的结果
    output_file = "Processed_Basin_Data.xlsx"
    df.to_excel(output_file, index=False)
    print(f"✅ 处理完成！结果已保存至: {output_file}")

if __name__ == "__main__":
    # 这里填入你要读取的 csv 文件名
    your_csv_file = "data.csv.csv"

    # 先打印当前运行目录和目录内容，便于排查找不到文件的问题
    print_runtime_directory_info()
    
    if os.path.exists(your_csv_file):
        process_hydrology_data(your_csv_file)
    else:
        print(f"⚠️ 请确保文件夹下存在 {your_csv_file} 文件")
