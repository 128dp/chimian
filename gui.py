"""
Simple GUI for plastic material data extraction
"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
from pathlib import Path
from enhanced_extractor import EnhancedPDFExtractor
from excel_writer import DataOrganizer, ExcelWriter
from unit_converter import UnitConverter
import threading
from collections import defaultdict

class MaterialExtractorGUI:
    """GUI for plastic material metric extraction"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Plastic Material Metrics Extractor")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.pdf_files = []
        self.selected_output_path = None
        self.converter = UnitConverter()
        
        self._create_ui()
    
    def _create_ui(self):
        """Create user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Plastic Material Metrics Extractor", 
                                font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Step 1: Select PDF Files", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        file_frame.columnconfigure(0, weight=1)
        
        ttk.Button(file_frame, text="Select PDF Files", 
                   command=self._select_files).pack(side=tk.LEFT, padx=5)
        
        self.file_count_label = ttk.Label(file_frame, text="No files selected")
        self.file_count_label.pack(side=tk.LEFT, padx=20)
        
        ttk.Button(file_frame, text="Clear Files", 
                   command=self._clear_files).pack(side=tk.LEFT, padx=5)
        
        # Output location frame
        output_frame = ttk.LabelFrame(main_frame, text="Step 2: Select Output Location", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Button(output_frame, text="Choose Output Path", 
                   command=self._select_output).pack(side=tk.LEFT, padx=5)
        
        self.output_label = ttk.Label(output_frame, text="No output location selected", 
                                      foreground="gray")
        self.output_label.pack(side=tk.LEFT, padx=20)
        
        # Progress and log frame
        log_frame = ttk.LabelFrame(main_frame, text="Step 3: Processing Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD, 
                                                   state=tk.DISABLED, font=("Courier", 9))
        self.log_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress = ttk.Progressbar(log_frame, mode='indeterminate', length=400)
        self.progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        button_frame.columnconfigure(1, weight=1)
        
        ttk.Button(button_frame, text="Extract & Generate Excel", 
                   command=self._run_extraction).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Exit", 
                   command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        self._log("Ready to process PDF files.\n" + 
                 "1. Select your PDF files\n" +
                 "2. Choose output Excel file location\n" +
                 "3. Click 'Extract & Generate Excel'\n")
    
    def _log(self, message: str, add_newline: bool = True):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + ("\n" if add_newline else ""))
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def _select_files(self):
        """Select PDF files for extraction"""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if files:
            self.pdf_files = list(files)
            self.file_count_label.config(
                text=f"{len(self.pdf_files)} file(s) selected",
                foreground="green"
            )
            self._log(f"Selected {len(self.pdf_files)} PDF file(s)")
    
    def _clear_files(self):
        """Clear selected files"""
        self.pdf_files = []
        self.file_count_label.config(text="No files selected", foreground="gray")
        self._log("Cleared file selection")
    
    def _select_output(self):
        """Select output Excel file location"""
        output_path = filedialog.asksaveasfilename(
            title="Save as Excel file",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if output_path:
            self.selected_output_path = output_path
            filename = Path(output_path).name
            self.output_label.config(text=filename, foreground="green")
            self._log(f"Output location: {output_path}")
    
    def _run_extraction(self):
        """Run extraction in a separate thread"""
        if not self.pdf_files:
            messagebox.showwarning("No Files", "Please select PDF files first")
            return
        
        if not self.selected_output_path:
            messagebox.showwarning("No Output", "Please select output location first")
            return
        
        # Run extraction in background thread
        thread = threading.Thread(target=self._extraction_worker)
        thread.daemon = True
        thread.start()
    
    def _extraction_worker(self):
        """Background worker for extraction"""
        try:
            self.progress.start()
            self._log("\n" + "="*60)
            self._log("Starting extraction process...")
            self._log("="*60 + "\n")
            
            # Collect results by material
            materials_data = defaultdict(list)
            
            for idx, pdf_path in enumerate(self.pdf_files, 1):
                try:
                    filename = Path(pdf_path).name
                    self._log(f"[{idx}/{len(self.pdf_files)}] {filename}...", 
                             add_newline=False)
                    
                    extractor = EnhancedPDFExtractor(pdf_path)
                    result = extractor.extract_all()
                    
                    if result and result.get('metrics'):
                        metrics_count = len(result['metrics'])
                        self._log(f" ✓ Found {metrics_count} metric(s)")
                        
                        # Store for Excel generation
                        materials_data[f"Material_{len(materials_data)}"].append(result)
                    else:
                        self._log(f" ✗ No metrics found")
                
                except Exception as e:
                    self._log(f" ✗ Error: {str(e)}")
            
            if not any(materials_data.values()):
                self._log("\n" + "-"*60)
                self._log("⚠ No metrics could be extracted from any files")
                self.progress.stop()
                messagebox.showwarning("No Data", "No metrics were found in the selected PDFs")
                return
            
            self._log("\n" + "-"*60)
            self._log("Generating Excel file...")
            
            # Create Excel writer
            excel_writer = ExcelWriter(self.selected_output_path)
            
            # Process all results
            for material_key, results in materials_data.items():
                for result in results:
                    company = result.get('file', 'Unknown').split('\\')[-1]
                    material = f"Material_{len(excel_writer.materials_data)}"
                    
                    for metric_key, (original_value, original_unit) in result.get('metrics', {}).items():
                        metric_name = self._get_metric_name(metric_key)
                        
                        # Convert to standard units
                        if metric_key in ['tensile_strength', 'flexural_strength', 
                                         'tensile_modulus', 'flexural_modulus']:
                            std_value, std_unit = self.converter.convert_stress(original_value, original_unit)
                        
                        elif metric_key == 'density':
                            std_value, std_unit = self.converter.convert_density(original_value, original_unit)
                        
                        elif metric_key == 'elongation':
                            std_value, std_unit = self.converter.convert_elongation(original_value, original_unit)
                        
                        else:
                            std_value, std_unit = original_value, original_unit
                        
                        excel_writer.add_record(
                            company=company,
                            material=material,
                            metric_name=metric_name,
                            original_value=original_value,
                            original_unit=original_unit,
                            standard_value=std_value,
                            standard_unit=std_unit
                        )
            
            # Create sheets and save
            excel_writer.create_sheets()
            excel_writer.save()
            
            self._log("✓ Excel file successfully created!")
            self._log(f"Location: {self.selected_output_path}")
            self._log("="*60 + "\n")
            
            self.progress.stop()
            messagebox.showinfo("Success", 
                              f"Excel file created successfully!\n\n{self.selected_output_path}")
        
        except Exception as e:
            self.progress.stop()
            self._log(f"\n✗ Fatal error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
    
    def _get_metric_name(self, metric_key: str) -> str:
        """Convert metric key to display name"""
        names = {
            'tensile_strength': 'Tensile Strength',
            'flexural_strength': 'Flexural Strength',
            'density': 'Density',
            'tensile_modulus': 'Tensile Modulus',
            'flexural_modulus': 'Flexural Modulus',
            'elongation': 'Elongation'
        }
        return names.get(metric_key, metric_key.replace('_', ' ').title())


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = MaterialExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
