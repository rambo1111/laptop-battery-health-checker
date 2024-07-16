import subprocess
from bs4 import BeautifulSoup
import re
import sys
import os
import tkinter as tk
from tkinter import ttk

report_file = 'battery-report.html'
batch_file = 'generate_battery_report.bat'

def create_batch_file(batch_file):
    with open(batch_file, 'w') as file:
        file.write("@echo off\n")
        file.write("powercfg /batteryreport\n")
        file.write("exit\n")

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run_batch_file(batch_file):
    result = subprocess.run(batch_file, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"Failed to run batch file. Error: {result.stderr}")
        return False
    return True

def extract_battery_capacities(report_file):
    try:
        with open(report_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'lxml')

        tables = soup.find_all('table')
        design_capacity = full_charge_capacity = None

        for table in tables:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) > 1:
                    header = cols[0].text.strip().upper()
                    value = cols[1].text.strip()
                    if 'DESIGN CAPACITY' in header:
                        design_capacity = value
                    elif 'FULL CHARGE CAPACITY' in header:
                        full_charge_capacity = value

                    if design_capacity and full_charge_capacity:
                        return design_capacity, full_charge_capacity

    except Exception as e:
        print(f"Error extracting capacities: {e}")

    return None, None

def clean_capacity(value):
    value = re.sub(r'[^\d,]', '', value)
    value = value.replace(',', '')
    return int(value)

def cleanup_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def generate_report():
    create_batch_file(batch_file)
    
    if run_batch_file(batch_file):
        design_capacity, full_charge_capacity = extract_battery_capacities(report_file)
        
        if design_capacity and full_charge_capacity:
            try:
                design_capacity_int = clean_capacity(design_capacity)
                full_charge_capacity_int = clean_capacity(full_charge_capacity)
                
                battery_life_percentage = (full_charge_capacity_int / design_capacity_int) * 100
                
                result_text = (
                    f'Design Capacity: {design_capacity}\n'
                    f'Full Charge Capacity: {full_charge_capacity}\n'
                    f'Battery life left is: {battery_life_percentage:.2f}%'
                )
            except ValueError as e:
                result_text = "Error processing capacity values."
        else:
            result_text = "Could not extract battery capacities."
        
        output_text.delete(1.0, tk.END)  # Clear previous output
        output_text.insert(tk.END, result_text)  # Insert new output
        cleanup_files(batch_file, report_file)
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Failed to generate the battery report.")

if __name__ == "__main__":
    # Setting up the Tkinter UI
    root = tk.Tk()
    root.title("Battery Report(By: vibhaw-kureel)")
    root.iconbitmap(resource_path("battery.ico"))

    button = ttk.Button(root, text="Generate Battery Report", command=generate_report)
    button.pack(pady=10)

    output_text = tk.Text(root, wrap=tk.WORD, width=40, height=10)
    output_text.pack(padx=10, pady=10)

    root.geometry("400x200")
    root.mainloop()
