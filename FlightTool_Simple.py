#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flight Tool - Simple GUI (without setup complexity)
All components should be installed before running this
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import sys
import os
import json
import threading
from datetime import datetime, timedelta

class FlightToolSimple:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flight Tool - Complete scraping tool")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Variables for process control
        self.extended_process = None
        self.excel_process = None
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup GUI"""
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Extended Scraper tab
        self.setup_extended_tab(notebook)
        
        # Excel Scraper tab
        self.setup_excel_tab(notebook)
        
        # Data Extractor tab
        self.setup_extractor_tab(notebook)
        
        # Test tab
        self.setup_test_tab(notebook)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Menu
        self.setup_menu()
    
    def setup_menu(self):
        """Setup menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Run System Test", command=self.run_system_test)
        tools_menu.add_command(label="Reinstall Components", command=self.reinstall_components)
        tools_menu.add_separator()
        tools_menu.add_command(label="About", command=self.show_about)
    
    def setup_extended_tab(self, notebook):
        """Setup Extended Scraper tab - improved layout"""
        extended_frame = ttk.Frame(notebook)
        notebook.add(extended_frame, text="Extended Scraper")
        
        # Main container with grid layout for better width usage
        main_container = ttk.Frame(extended_frame, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid columns to distribute space evenly
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_columnconfigure(2, weight=1)
        main_container.grid_columnconfigure(3, weight=1)
        main_container.grid_columnconfigure(4, weight=1)
        
        # Route frame
        route_frame = ttk.LabelFrame(main_container, text="Route", padding="10")
        route_frame.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 10))
        
        tk.Label(route_frame, text="Origin:").grid(row=0, column=0, sticky=tk.W)
        self.origin_var = tk.StringVar(value="WAW")
        ttk.Entry(route_frame, textvariable=self.origin_var, width=10).grid(row=0, column=1, padx=5)
        
        tk.Label(route_frame, text="Destination:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.dest_var = tk.StringVar(value="ICN") 
        ttk.Entry(route_frame, textvariable=self.dest_var, width=10).grid(row=0, column=3, padx=5)
        
        # Dates frame
        dates_frame = ttk.LabelFrame(main_container, text="Dates", padding="10")
        dates_frame.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 10))
        
        tk.Label(dates_frame, text="Departure FROM:").grid(row=0, column=0, sticky=tk.W)
        self.dep_start_var = tk.StringVar(value="2025-10-20")
        ttk.Entry(dates_frame, textvariable=self.dep_start_var, width=12).grid(row=0, column=1, padx=5)
        
        tk.Label(dates_frame, text="TO:").grid(row=0, column=2, sticky=tk.W, padx=(10,0))
        self.dep_end_var = tk.StringVar(value="2025-10-25")
        ttk.Entry(dates_frame, textvariable=self.dep_end_var, width=12).grid(row=0, column=3, padx=5)
        
        tk.Label(dates_frame, text="Return FROM:").grid(row=1, column=0, sticky=tk.W, pady=(5,0))
        self.ret_start_var = tk.StringVar(value="2025-11-10")
        ttk.Entry(dates_frame, textvariable=self.ret_start_var, width=12).grid(row=1, column=1, padx=5, pady=(5,0))
        
        tk.Label(dates_frame, text="TO:").grid(row=1, column=2, sticky=tk.W, padx=(10,0), pady=(5,0))
        self.ret_end_var = tk.StringVar(value="2025-11-15")
        ttk.Entry(dates_frame, textvariable=self.ret_end_var, width=12).grid(row=1, column=3, padx=5, pady=(5,0))
        
        # Trip duration frame
        duration_frame = ttk.LabelFrame(main_container, text="Trip duration (days)", padding="10")
        duration_frame.grid(row=2, column=0, columnspan=5, sticky="ew", pady=(0, 10))
        
        tk.Label(duration_frame, text="Min:").grid(row=0, column=0, sticky=tk.W)
        self.min_days_var = tk.StringVar(value="19")
        ttk.Entry(duration_frame, textvariable=self.min_days_var, width=8).grid(row=0, column=1, padx=5)
        
        tk.Label(duration_frame, text="Max:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.max_days_var = tk.StringVar(value="24")
        ttk.Entry(duration_frame, textvariable=self.max_days_var, width=8).grid(row=0, column=3, padx=5)
        
        tk.Label(duration_frame, text="Passengers:").grid(row=0, column=4, sticky=tk.W, padx=(20,0))
        self.passengers_var = tk.StringVar(value="2")
        ttk.Entry(duration_frame, textvariable=self.passengers_var, width=8).grid(row=0, column=5, padx=5)
        
        # Airlines frame with better layout
        airlines_frame = ttk.LabelFrame(main_container, text="Airlines", padding="10")
        airlines_frame.grid(row=3, column=0, columnspan=5, sticky="ew", pady=(0, 10))
        
        # Create airline checkboxes in 5 columns
        airlines = [
            "LOT", "Turkish", "Emirates", "Qatar", "Lufthansa", "KLM", 
            "Air_France", "British_Airways", "Etihad", "Air_China", 
            "Korean_Air", "All_Nippon", "Singapore", "Cathay_Pacific",
            "Swiss", "Austrian", "Finnair", "SAS", "Asiana"
        ]
        
        self.airline_vars = {}
        
        for i, airline in enumerate(airlines):
            var = tk.BooleanVar()
            self.airline_vars[airline] = var
            
            # Display name mapping
            display_names = {
                "LOT": "LOT Polish Airlines",
                "Turkish": "Turkish Airlines",
                "Emirates": "Emirates",
                "Qatar": "Qatar Airways", 
                "Lufthansa": "Lufthansa",
                "KLM": "KLM",
                "Air_France": "Air France",
                "British_Airways": "British Airways",
                "Etihad": "Etihad Airways",
                "Air_China": "Air China",
                "Korean_Air": "Korean Air",
                "All_Nippon": "All Nippon Airways",
                "Singapore": "Singapore Airlines",
                "Cathay_Pacific": "Cathay Pacific",
                "Swiss": "Swiss",
                "Austrian": "Austrian Airlines",
                "Finnair": "Finnair",
                "SAS": "SAS",
                "Asiana": "Asiana Airlines"
            }
            
            display_name = display_names.get(airline, airline.replace("_", " "))
            ttk.Checkbutton(airlines_frame, text=display_name, 
                           variable=var).grid(row=i//5, column=i%5, sticky=tk.W, padx=5, pady=2)
        
        # Select all/none buttons
        buttons_frame = tk.Frame(airlines_frame)
        buttons_frame.grid(row=(len(airlines)//5)+1, column=0, columnspan=5, pady=(10,0))
        
        ttk.Button(buttons_frame, text="Select All", 
                  command=self.select_all_airlines).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Select None", 
                  command=self.select_no_airlines).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Select Popular", 
                  command=self.select_popular_airlines).pack(side=tk.LEFT, padx=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_container, text="Settings", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=5, sticky="ew", pady=(0, 10))
        
        # Delay settings
        tk.Label(settings_frame, text="Delay (s):").grid(row=0, column=0, sticky=tk.W)
        self.delay_min_var = tk.StringVar(value="30")
        ttk.Entry(settings_frame, textvariable=self.delay_min_var, width=8).grid(row=0, column=1, padx=5)
        tk.Label(settings_frame, text="-").grid(row=0, column=2)
        self.delay_max_var = tk.StringVar(value="45")
        ttk.Entry(settings_frame, textvariable=self.delay_max_var, width=8).grid(row=0, column=3, padx=5)
        
        # Rolling mode
        self.rolling_var = tk.BooleanVar()
        rolling_check = ttk.Checkbutton(settings_frame, text="Rolling mode", 
                                       variable=self.rolling_var, command=self.toggle_rolling)
        rolling_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5,0))
        
        # Rolling mode settings
        self.rolling_frame = tk.Frame(settings_frame)
        self.rolling_frame.grid(row=2, column=0, columnspan=5, sticky=tk.W, pady=(5,0))
        
        tk.Label(self.rolling_frame, text="Break (min):").grid(row=0, column=0, sticky=tk.W)
        self.rolling_min_var = tk.StringVar(value="45")
        self.rolling_min_entry = ttk.Entry(self.rolling_frame, textvariable=self.rolling_min_var, width=8, state="disabled")
        self.rolling_min_entry.grid(row=0, column=1, padx=5)
        tk.Label(self.rolling_frame, text="-").grid(row=0, column=2)
        self.rolling_max_var = tk.StringVar(value="90")
        self.rolling_max_entry = ttk.Entry(self.rolling_frame, textvariable=self.rolling_max_var, width=8, state="disabled")
        self.rolling_max_entry.grid(row=0, column=3, padx=5)
        
        # Control buttons
        control_frame = ttk.LabelFrame(main_container, text="Control", padding="10")
        control_frame.grid(row=5, column=0, columnspan=5, sticky="ew", pady=(0, 10))
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Save Config", 
                  command=self.save_extended_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Config", 
                  command=self.load_extended_config).pack(side=tk.LEFT, padx=5)
        
        # Start/Stop buttons
        self.start_extended_btn = ttk.Button(button_frame, text="START SCRAPING", 
                                           command=self.run_extended_scraping)
        self.start_extended_btn.pack(side=tk.LEFT, padx=20)
        
        self.stop_extended_btn = ttk.Button(button_frame, text="STOP SCRAPING", 
                                          command=self.stop_extended_scraping, state="disabled")
        self.stop_extended_btn.pack(side=tk.LEFT, padx=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_container, text="Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=5, sticky="nsew", pady=(0, 0))
        
        main_container.grid_rowconfigure(6, weight=1)  # Make log frame expandable
        
        self.extended_log = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.extended_log.pack(fill=tk.BOTH, expand=True)
    
    def setup_excel_tab(self, notebook):
        """Setup Excel Scraper tab"""
        excel_frame = ttk.Frame(notebook)
        notebook.add(excel_frame, text="Excel Scraper")
        
        # Main container
        main_container = ttk.Frame(excel_frame, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = ttk.LabelFrame(main_container, text="Excel file", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.excel_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.excel_file_var, width=60).pack(side=tk.LEFT, padx=(0,10), fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse", command=self.browse_excel_file).pack(side=tk.RIGHT, padx=5)
        ttk.Button(file_frame, text="Create Sample", command=self.create_sample_excel).pack(side=tk.RIGHT, padx=5)
        
        # Control buttons
        control_frame = ttk.LabelFrame(main_container, text="Control", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack()
        
        self.start_excel_btn = ttk.Button(button_frame, text="START EXCEL SCRAPING", 
                                        command=self.run_excel_scraping)
        self.start_excel_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_excel_btn = ttk.Button(button_frame, text="STOP EXCEL SCRAPING", 
                                       command=self.stop_excel_scraping, state="disabled")
        self.stop_excel_btn.pack(side=tk.LEFT, padx=5)
        
        # Log
        log_frame = ttk.LabelFrame(main_container, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.excel_log = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.excel_log.pack(fill=tk.BOTH, expand=True)
    
    def setup_extractor_tab(self, notebook):
        """Setup Data Extractor tab"""
        extractor_frame = ttk.Frame(notebook)
        notebook.add(extractor_frame, text="Data Extractor")
        
        # Main container
        main_container = ttk.Frame(extractor_frame, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Source directory selection
        source_frame = ttk.LabelFrame(main_container, text="Source directory", padding="10")
        source_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.source_dir_var = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.source_dir_var, width=60).pack(side=tk.LEFT, padx=(0,10), fill=tk.X, expand=True)
        ttk.Button(source_frame, text="Browse", command=self.browse_source_dir).pack(side=tk.RIGHT, padx=5)
        ttk.Button(source_frame, text="Quick: rolling_mode", command=self.quick_rolling_mode).pack(side=tk.RIGHT, padx=5)
        
        # Control buttons
        control_frame = ttk.LabelFrame(main_container, text="Control", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Preview Data", 
                  command=self.preview_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="EXTRACT TO EXCEL", 
                  command=self.run_data_extraction).pack(side=tk.LEFT, padx=20)
        
        # Log
        log_frame = ttk.LabelFrame(main_container, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.extractor_log = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.extractor_log.pack(fill=tk.BOTH, expand=True)
    
    def setup_test_tab(self, notebook):
        """Setup Test tab"""
        test_frame = ttk.Frame(notebook)
        notebook.add(test_frame, text="Test")
        
        # Test buttons
        test_buttons_frame = ttk.LabelFrame(test_frame, text="System Tests", padding="10")
        test_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = tk.Frame(test_buttons_frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Quick ChromeDriver Test", 
                  command=self.quick_chromedriver_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Full System Test", 
                  command=self.run_system_test).pack(side=tk.LEFT, padx=5)
        
        # Test log
        log_frame = ttk.LabelFrame(test_frame, text="Test Results", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.test_log = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.test_log.pack(fill=tk.BOTH, expand=True)
    
    # GUI Helper Methods
    def toggle_rolling(self):
        """Toggle rolling mode settings"""
        if self.rolling_var.get():
            self.rolling_min_entry.config(state="normal")
            self.rolling_max_entry.config(state="normal")
        else:
            self.rolling_min_entry.config(state="disabled")
            self.rolling_max_entry.config(state="disabled")
    
    def select_all_airlines(self):
        """Select all airlines"""
        for var in self.airline_vars.values():
            var.set(True)
    
    def select_no_airlines(self):
        """Deselect all airlines"""
        for var in self.airline_vars.values():
            var.set(False)
    
    def select_popular_airlines(self):
        """Select popular airlines for WAW routes"""
        # First deselect all
        self.select_no_airlines()
        
        # Select popular ones
        popular_airlines = ["LOT", "Turkish", "Emirates", "Qatar", "Lufthansa"]
        for airline in popular_airlines:
            if airline in self.airline_vars:
                self.airline_vars[airline].set(True)
    
    # Configuration Methods
    def save_extended_config(self):
        """Save Extended configuration"""
        try:
            # Map GUI airline names to scraper format
            airline_mapping = {
                "Turkish": "Turkish",
                "Qatar": "Qatar", 
                "Emirates": "Emirates",
                "Lufthansa": "Lufthansa",
                "KLM": "KLM",
                "Air_France": "Air_France",
                "British_Airways": "British_Airways", 
                "Etihad": "Etihad",
                "Air_China": "Air_China",
                "Korean_Air": "Korean_Air",
                "All_Nippon": "All_Nippon",
                "Singapore": "Singapore",
                "Cathay_Pacific": "Cathay_Pacific"
            }
            
            # Convert selected airlines to scraper format
            selected_airlines = [airline_mapping.get(airline, airline) 
                               for airline, var in self.airline_vars.items() if var.get()]
            
            if not selected_airlines:
                messagebox.showwarning("Warning", "Select at least one airline")
                return
            
            config = {
                "scraping_config": {
                    "origin": self.origin_var.get().upper().strip(),
                    "destination": self.dest_var.get().upper().strip(),
                    "earliest_departure": self.dep_start_var.get().strip(),
                    "latest_return": self.ret_end_var.get().strip(),
                    "departure_start": self.dep_start_var.get().strip(),
                    "departure_end": self.dep_end_var.get().strip(),
                    "return_start": self.ret_start_var.get().strip(),
                    "return_end": self.ret_end_var.get().strip(),
                    "min_days": int(self.min_days_var.get()),
                    "max_days": int(self.max_days_var.get()),
                    "passengers": int(self.passengers_var.get()),
                    "selected_airlines": selected_airlines,
                    "delay_between_requests": [int(self.delay_min_var.get()), int(self.delay_max_var.get())],
                    "rolling_mode": self.rolling_var.get(),
                    "rolling_break_minutes": [int(self.rolling_min_var.get()), int(self.rolling_max_var.get())] if self.rolling_var.get() else [45, 90]
                }
            }
            
            with open("config_extended.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.extended_log.insert(tk.END, "OK Configuration saved to config_extended.json\n")
            self.extended_log.see(tk.END)
            self.status_var.set("Configuration saved")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
    
    def load_extended_config(self):
        """Load Extended configuration"""
        try:
            filename = filedialog.askopenfilename(
                title="Select configuration file",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            with open(filename, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Load values - check both old and new format
            if "scraping_config" in config:
                # New format
                scraping_config = config["scraping_config"]
                self.origin_var.set(scraping_config.get("origin", "WAW"))
                self.dest_var.set(scraping_config.get("destination", "ICN"))
                self.dep_start_var.set(scraping_config.get("departure_start", scraping_config.get("earliest_departure", "2025-10-20")))
                self.dep_end_var.set(scraping_config.get("departure_end", scraping_config.get("latest_return", "2025-10-25")))
                self.ret_start_var.set(scraping_config.get("return_start", scraping_config.get("earliest_departure", "2025-11-10")))
                self.ret_end_var.set(scraping_config.get("return_end", scraping_config.get("latest_return", "2025-11-15")))
                self.min_days_var.set(str(scraping_config.get("min_days", 19)))
                self.max_days_var.set(str(scraping_config.get("max_days", 24)))
                self.passengers_var.set(str(scraping_config.get("passengers", 2)))
                
                delay = scraping_config.get("delay_between_requests", [30, 45])
                self.delay_min_var.set(str(delay[0]))
                self.delay_max_var.set(str(delay[1]))
                
                # Airlines
                airlines = scraping_config.get("selected_airlines", [])
                for airline, var in self.airline_vars.items():
                    var.set(airline in airlines)
                
                # Rolling mode
                self.rolling_var.set(scraping_config.get("rolling_mode", False))
                self.toggle_rolling()
                
                rolling_break = scraping_config.get("rolling_break_minutes", [45, 90])
                self.rolling_min_var.set(str(rolling_break[0]))
                self.rolling_max_var.set(str(rolling_break[1]))
            
            self.extended_log.insert(tk.END, f"OK Configuration loaded from {filename}\n")
            self.extended_log.see(tk.END)
            self.status_var.set("Configuration loaded")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration:\n{str(e)}")
    
    # Scraping Methods
    def run_extended_scraping(self):
        """Run Extended Scraping"""
        # First save configuration
        self.save_extended_config()
        
        # Check if scraper file exists
        if not os.path.exists("scrap_only_extended.py"):
            messagebox.showerror("Error", "File scrap_only_extended.py not found\nMake sure you are in the project folder.")
            return
        
        # Update button states
        self.start_extended_btn.config(state="disabled")
        self.stop_extended_btn.config(state="normal")
        
        self.run_script_with_output("scrap_only_extended.py", self.extended_log, "Extended Scraping", "extended")
    
    def stop_extended_scraping(self):
        """Stop Extended Scraping"""
        if self.extended_process:
            try:
                self.extended_process.terminate()
                self.extended_log.insert(tk.END, "\nScraping stopped by user\n")
                self.extended_log.see(tk.END)
                self.status_var.set("Scraping stopped")
            except:
                pass
        
        # Reset button states
        self.start_extended_btn.config(state="normal")
        self.stop_extended_btn.config(state="disabled")
    
    def browse_excel_file(self):
        """Browse for Excel file"""
        filename = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.excel_file_var.set(filename)
    
    def create_sample_excel(self):
        """Create sample Excel file"""
        try:
            import pandas as pd
            
            sample_data = {
                "Origin": ["WAW", "WAW", "WAW", "WAW", "WAW"],
                "Destination": ["ICN", "ICN", "ICN", "ICN", "ICN"],
                "Departure_Date": ["2025-10-22", "2025-10-23", "2025-10-24", "2025-10-25", "2025-10-26"],
                "Return_Date": ["2025-11-10", "2025-11-11", "2025-11-12", "2025-11-13", "2025-11-14"],
                "Passengers": [2, 2, 2, 2, 2],
                "Airline_Filter": ["Turkish", "Qatar", "Emirates", "Etihad", "Air_China"]
            }
            
            df = pd.DataFrame(sample_data)
            filename = filedialog.asksaveasfilename(
                title="Save sample Excel file",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialvalue="flights_list.xlsx"
            )
            
            if filename:
                df.to_excel(filename, index=False)
                self.excel_file_var.set(filename)
                self.excel_log.insert(tk.END, f"OK Sample file created: {filename}\n")
                self.excel_log.insert(tk.END, "Edit the file and run scraping\n")
                self.excel_log.see(tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Excel file:\n{str(e)}")
    
    def run_excel_scraping(self):
        """Run Excel Scraping"""
        if not os.path.exists(self.excel_file_var.get()):
            messagebox.showerror("Error", f"File not found: {self.excel_file_var.get()}")
            return
        
        if not os.path.exists("kayak_excel_scraper.py"):
            messagebox.showerror("Error", "File kayak_excel_scraper.py not found\nMake sure you are in the project folder.")
            return
        
        # Update button states
        self.start_excel_btn.config(state="disabled")
        self.stop_excel_btn.config(state="normal")
        
        self.run_script_with_output(f"kayak_excel_scraper.py {self.excel_file_var.get()}", self.excel_log, "Excel Scraping", "excel")
    
    def stop_excel_scraping(self):
        """Stop Excel Scraping"""
        if self.excel_process:
            try:
                self.excel_process.terminate()
                self.excel_log.insert(tk.END, "\nExcel scraping stopped by user\n")
                self.excel_log.see(tk.END)
                self.status_var.set("Excel scraping stopped")
            except:
                pass
        
        # Reset button states
        self.start_excel_btn.config(state="normal")
        self.stop_excel_btn.config(state="disabled")
    
    def browse_source_dir(self):
        """Browse for source directory"""
        directory = filedialog.askdirectory(title="Select data directory")
        if directory:
            # Fix for paths with spaces and special characters
            directory = os.path.normpath(directory)
            self.source_dir_var.set(directory)
    
    def quick_rolling_mode(self):
        """Quick select rolling_mode directory"""
        if os.path.exists("rolling_mode"):
            self.source_dir_var.set("rolling_mode")
            self.extractor_log.insert(tk.END, "OK Selected: rolling_mode\n")
            self.extractor_log.see(tk.END)
        else:
            messagebox.showwarning("Warning", "rolling_mode directory does not exist")
    
    def preview_data(self):
        """Preview data in directory"""
        source_dir = self.source_dir_var.get()
        if not source_dir or not os.path.exists(source_dir):
            messagebox.showwarning("Warning", "Select valid directory")
            return
        
        try:
            txt_files = [f for f in os.listdir(source_dir) if f.endswith('.txt')]
            
            self.extractor_log.delete(1.0, tk.END)
            self.extractor_log.insert(tk.END, f"Directory: {source_dir}\n")
            self.extractor_log.insert(tk.END, f"Found {len(txt_files)} .txt files\n\n")
            
            # Show first 10 files
            for i, filename in enumerate(txt_files[:10]):
                file_size = os.path.getsize(os.path.join(source_dir, filename))
                self.extractor_log.insert(tk.END, f"  {i+1:2d}. {filename} ({file_size} bytes)\n")
            
            if len(txt_files) > 10:
                self.extractor_log.insert(tk.END, f"  ... and {len(txt_files)-10} more files\n")
            
            self.extractor_log.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview data:\n{str(e)}")
    
    def run_data_extraction(self):
        """Run data extraction"""
        source_dir = self.source_dir_var.get()
        if not source_dir or not os.path.exists(source_dir):
            messagebox.showwarning("Warning", "Select valid directory")
            return
        
        if not os.path.exists("simple_kayak_extractor.py"):
            messagebox.showerror("Error", "File simple_kayak_extractor.py not found\nMake sure you are in the project folder.")
            return
        
        # Fix path for command line - use quotes for paths with spaces
        if " " in source_dir:
            source_dir_quoted = f'"{source_dir}"'
        else:
            source_dir_quoted = source_dir
        
        self.run_script_with_output(f"simple_kayak_extractor.py {source_dir_quoted}", self.extractor_log, "Data Extraction", "extractor")
    
    # Test Methods
    def quick_chromedriver_test(self):
        """Quick ChromeDriver test"""
        self.test_log.delete(1.0, tk.END)
        self.test_log.insert(tk.END, "Testing ChromeDriver...\n")
        self.test_log.see(tk.END)
        
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            self.test_log.insert(tk.END, "✓ Selenium imports successful\n")
            
            options = Options()
            options.add_argument('--headless')
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            self.test_log.insert(tk.END, "✓ ChromeDriver initialized\n")
            
            driver.get('data:text/html,<h1>Test</h1>')
            driver.quit()
            
            self.test_log.insert(tk.END, "✓ ChromeDriver test PASSED\n")
            self.status_var.set("ChromeDriver test passed")
            
        except Exception as e:
            self.test_log.insert(tk.END, f"✗ ChromeDriver test FAILED: {e}\n")
            self.status_var.set("ChromeDriver test failed")
        
        self.test_log.see(tk.END)
    
    def run_system_test(self):
        """Run full system test"""
        self.run_script_with_output("test_system.py", self.test_log, "System Test", "test")
    
    def reinstall_components(self):
        """Reinstall components"""
        if messagebox.askyesno("Reinstall", "Run component setup again?"):
            self.run_script_with_output("setup_components.py", self.test_log, "Component Setup", "test")
    
    # Utility Methods
    def run_script_with_output(self, script_command, log_widget, operation_name, process_type=None):
        """Run a script and show output in real time"""
        def script_worker():
            try:
                self.root.after(0, lambda: log_widget.insert(tk.END, f"Starting {operation_name}...\n"))
                self.root.after(0, lambda: log_widget.see(tk.END))
                self.root.after(0, lambda: self.status_var.set(f"{operation_name} in progress..."))
                
                # Split command for subprocess
                if " " in script_command:
                    cmd_parts = script_command.split(" ", 1)
                    cmd = [sys.executable, cmd_parts[0]] + cmd_parts[1].split()
                else:
                    cmd = [sys.executable, script_command]
                
                # Handle quoted paths properly
                if script_command.startswith("simple_kayak_extractor.py"):
                    # For extractor, handle the path argument specially
                    parts = script_command.split(" ", 1)
                    if len(parts) > 1:
                        path_arg = parts[1].strip('"')  # Remove quotes
                        cmd = [sys.executable, parts[0], path_arg]
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    text=True, 
                    bufsize=1, 
                    universal_newlines=True
                )
                
                # Store process reference for stopping
                if process_type == "extended":
                    self.extended_process = process
                elif process_type == "excel":
                    self.excel_process = process
                
                # Read output in real time
                for line in process.stdout:
                    self.root.after(0, lambda l=line: log_widget.insert(tk.END, l))
                    self.root.after(0, lambda: log_widget.see(tk.END))
                
                process.wait()
                
                if process.returncode == 0:
                    self.root.after(0, lambda: log_widget.insert(tk.END, f"{operation_name} completed successfully!\n"))
                    self.root.after(0, lambda: self.status_var.set(f"{operation_name} completed"))
                else:
                    self.root.after(0, lambda: log_widget.insert(tk.END, f"{operation_name} ended with code: {process.returncode}\n"))
                    self.root.after(0, lambda: self.status_var.set(f"{operation_name} error"))
                    
            except Exception as e:
                self.root.after(0, lambda: log_widget.insert(tk.END, f"Error: {str(e)}\n"))
                self.root.after(0, lambda: self.status_var.set("Error"))
            
            finally:
                # Reset button states when process ends
                if process_type == "extended":
                    self.root.after(0, lambda: self.start_extended_btn.config(state="normal"))
                    self.root.after(0, lambda: self.stop_extended_btn.config(state="disabled"))
                    self.extended_process = None
                elif process_type == "excel":
                    self.root.after(0, lambda: self.start_excel_btn.config(state="normal"))
                    self.root.after(0, lambda: self.stop_excel_btn.config(state="disabled"))
                    self.excel_process = None
            
            self.root.after(0, lambda: log_widget.see(tk.END))
        
        threading.Thread(target=script_worker, daemon=True).start()
    
    def show_about(self):
        """Show program information"""
        about_text = """Flight Tool v1.0

Complete flight price scraping tool

Features:
• Extended Scraper - scraping multiple combinations
• Excel Scraper - scraping from Excel file  
• Data Extractor - analyzing results to Excel

Author: Flight Tool Team
License: MIT

Setup: Use setup_and_run.bat for easy installation
"""
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Run application"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = FlightToolSimple()
        app.run()
    except Exception as e:
        print(f"Startup error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()