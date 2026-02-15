"""
Main application window using CustomTkinter
"""
import customtkinter as ctk
from pathlib import Path
import threading
from tkinter import filedialog
import os
import sys

from src.ui.theme import COLORS, FONTS, SPACING, RADIUS
from src.core.validator import validate_url
from src.core.downloader import YouTubeDownloader, DownloadProgress
from src.core.processor import AudioProcessor, ProcessProgress


class App(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("YouTube to 60min MP3")
        self.geometry("600x410") # Compact size
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize variables
        self.output_folder = Path.home() / "Desktop"
        self.is_processing = False
        
        # Build UI
        self._build_ui()
        
    def _build_ui(self):
        """Build the user interface"""
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_primary'], corner_radius=0)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        # Removed spacer row weight to keep things tight at the top
        
        # 1. Input Section (Card)
        self._build_input_section()
        
        # 2. Settings Section (Card)
        self._build_settings_section()
        
        # 3. Action Section (Card)
        self._build_action_section()
        
        # 4. Footer/Status
        self._build_footer()
        
    def _build_input_section(self):
        """Build the URL input section"""
        card = ctk.CTkFrame(self.main_container, fg_color="transparent", corner_radius=RADIUS['lg'])
        card.grid(row=0, column=0, padx=SPACING['lg'], pady=(SPACING['lg'], 0), sticky="ew")
        
        label = ctk.CTkLabel(
            card,
            text="🔗 Link YouTube",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        label.pack(padx=SPACING['lg'], pady=(0, SPACING['sm']), anchor="w")
        
        self.url_entry = ctk.CTkEntry(
            card,
            placeholder_text="Dán link youtube vào đây...",
            font=FONTS['body'],
            height=36, # Compact input
            corner_radius=RADIUS['md'],
            border_width=1,
            border_color=COLORS['border'],
            fg_color=COLORS['bg_secondary'],
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_muted']
        )
        self.url_entry.pack(padx=SPACING['lg'], pady=(SPACING['sm'], 0), fill="x")
        
        self.validation_label = ctk.CTkLabel(
            card,
            text="",
            font=FONTS['caption'],
            text_color=COLORS['error'],
            height=14,
            anchor="w"
        )
        self.validation_label.pack(padx=SPACING['lg'], pady=(0, 0), fill="x")

    def _build_settings_section(self):
        """Build the settings section (Output folder)"""
        card = ctk.CTkFrame(self.main_container, fg_color="transparent", corner_radius=RADIUS['lg'])
        card.grid(row=1, column=0, padx=SPACING['lg'], pady=(0, SPACING['lg']), sticky="ew")
        
        label = ctk.CTkLabel(
            card,
            text="📂 Vị trí lưu",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        label.pack(padx=SPACING['lg'], pady=(0, SPACING['sm']), anchor="w")
        
        # Folder selection row
        folder_row = ctk.CTkFrame(card, fg_color=COLORS['bg_secondary'], corner_radius=RADIUS['lg'])
        folder_row.pack(padx=SPACING['lg'], pady=(SPACING['sm'], SPACING['md']), fill="x")
        
        self.folder_label = ctk.CTkLabel(
            folder_row,
            text=str(self.output_folder),
            font=FONTS['monospace'],
            text_color=COLORS['text_secondary'],
            fg_color=COLORS['bg_primary'],
            corner_radius=RADIUS['sm'],
            height=36, # Compact
            anchor="w",
            padx=SPACING['md']
        )
        self.folder_label.pack(side="left", fill="x", expand=True, padx=(SPACING['sm'], SPACING['md']), pady=SPACING['sm'])
        
        self.change_btn = ctk.CTkButton(
            folder_row,
            text="Thay đổi",
            font=FONTS['body_bold'],
            height=36, # Compact
            width=80,
            corner_radius=RADIUS['md'],
            fg_color=COLORS['bg_tertiary'],
            text_color=COLORS['text_primary'],
            hover_color=COLORS['border'],
            command=self._select_folder
        )
        self.change_btn.pack(side="right", padx=(0, SPACING['sm']), pady=SPACING['sm'])

    def _build_action_section(self):
        """Build the action button and section"""
        
        action_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        action_frame.grid(row=2, column=0, padx=SPACING['lg'], pady=(SPACING['md'], SPACING['lg']), sticky="ew")
        
        self.convert_button = ctk.CTkButton(
            action_frame,
            text="Bắt đầu chuyển đổi",
            font=FONTS['subheading'], # Slightly smaller than heading
            height=45, # Compact button
            width=200,
            corner_radius=RADIUS['lg'],
            fg_color=COLORS['accent_primary'],
            hover_color=COLORS['accent_hover'],
            text_color='#ffffff',
            command=self._start_conversion
        )
        self.convert_button.pack(pady=(0, SPACING['md']))
        
        # Progress UI
        self.progress_frame = ctk.CTkFrame(action_frame, fg_color="transparent", corner_radius=RADIUS['lg'])
        self.progress_frame.pack(fill="x")
        
        self.status_row = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.status_row.pack(fill="x", padx=SPACING['lg'], pady=(SPACING['sm'], 0))
        
        self.progress_label = ctk.CTkLabel(
            self.status_row,
            text="Quá trình",
            font=FONTS['body'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        self.progress_label.pack(side="left")
        
        self.percent_label = ctk.CTkLabel(
            self.status_row,
            text="0%",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            anchor="e"
        )
        self.percent_label.pack(side="right")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=8, # Thinner bar
            corner_radius=RADIUS['full'],
            progress_color=COLORS['accent_primary'],
            border_color=COLORS['bg_tertiary'],
            border_width=1,
            fg_color=COLORS['bg_tertiary']
        )
        self.progress_bar.pack(fill="x", padx=SPACING['lg'], pady=(SPACING['xs'], SPACING['md']))
        self.progress_bar.set(0)

    def _build_footer(self):
        """Build footer with status messages"""
        self.status_label = ctk.CTkLabel(
            self.main_container,
            text="",
            font=FONTS['caption'],
            text_color=COLORS['text_muted']
        )
        self.status_label.grid(row=3, column=0, pady=(0, SPACING['sm']))

    def _select_folder(self):
        """Open folder picker dialog"""
        folder = filedialog.askdirectory(
            title="Chọn thư mục lưu file",
            initialdir=str(self.output_folder)
        )
        if folder:
            self.output_folder = Path(folder)
            self.folder_label.configure(text=str(self.output_folder))
            
    def _start_conversion(self):
        """Start the conversion process"""
        # Validate URL
        url = self.url_entry.get().strip()
        is_valid, error = validate_url(url)
        
        if not is_valid:
            self.validation_label.configure(text=error)
            self.url_entry.configure(border_color=COLORS['error'])
            return
        
        self.validation_label.configure(text="")
        self.url_entry.configure(border_color=COLORS['border'])
        
        # Disable button and start processing
        if not self.is_processing:
            self.is_processing = True
            self.convert_button.configure(state="disabled", text="Đang xử lý...", fg_color=COLORS['accent_disabled'])
            self.url_entry.configure(state="disabled")
            self.change_btn.configure(state="disabled")
            self.percent_label.configure(text_color=COLORS['accent_primary'])
            
            # Run in background thread
            thread = threading.Thread(target=self._process_video, args=(url,), daemon=True)
            thread.start()
    
    def _process_video(self, url: str):
        """Process video in background thread"""
        try:
            # Step 1: Download
            self._update_ui("Đang tải audio từ YouTube...", 0.0)
            downloader = YouTubeDownloader()
            
            def download_callback(progress: DownloadProgress):
                p = progress.percent / 200 # 0-50%
                self._update_ui(f"Đang tải: {progress.percent:.1f}%", p)
            
            audio_file, title = downloader.download(url, download_callback)
            
            # Step 2: Process
            self._update_ui("Đang xử lý audio...", 0.5)
            processor = AudioProcessor()
            
            def process_callback(progress: ProcessProgress):
                # Map 0-100% of processing to 50-100% of overall progress
                overall_progress = 0.5 + (progress.percent / 200)
                self._update_ui(progress.current_step, overall_progress)
            
            # Generate output filename
            output_file = self.output_folder / f"{title}.mp3"
            
            processor.loop_to_60min(audio_file, output_file, process_callback)
            
            # Clean up temporary file
            if audio_file.exists():
                audio_file.unlink()
            
            # Success
            self._update_ui("✅ Hoàn thành!", 1.0, COLORS['success'])
            self._show_status(f"Đã lưu: {output_file.name}", COLORS['success'])
            
            # Open folder
            os.startfile(str(self.output_folder))
            
        except Exception as e:
            self._update_ui(f"❌ Lỗi: {str(e)}", 0.0, COLORS['error'])
            self._show_status(str(e), COLORS['error'])
        
        finally:
            # Re-enable button
            def reset_btn():
                self.convert_button.configure(state="normal", text="Bắt đầu chuyển đổi", fg_color=COLORS['accent_primary'])
                self.url_entry.configure(state="normal")
                self.change_btn.configure(state="normal")
                self.is_processing = False
            self.after(0, reset_btn)
    
    def _update_ui(self, message: str, progress: float, color: str = None):
        """Update UI from background thread"""
        def update():
            self.progress_label.configure(
                text=message,
                text_color=color or COLORS['text_secondary']
            )
            self.progress_bar.set(progress)
            self.percent_label.configure(
                text=f"{int(progress * 100)}%",
                text_color=color or COLORS['text_primary']
            )
        
        self.after(0, update)
    
    def _show_status(self, message: str, color: str):
        """Show status message"""
        def update():
            self.status_label.configure(text=message, text_color=color)
        
        self.after(0, update)
