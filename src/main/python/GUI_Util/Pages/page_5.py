# Copyright (C) Siavoosh Payandeh Azad
from page_class import Page
import Tkinter as tk
import ttk


class Page5(Page):      # visualization

    # visualization
    viz_starting_row = 0
    viz_starting_col = 0

    # Animation Frame generation
    anim_starting_row = 0
    anim_starting_col = 4

    option_menu_width = 15
    entry_width = 10

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.all_viz = tk.BooleanVar(self)
        self.all_viz.set('False')
        all_viz_enable = tk.Checkbutton(self, text="Check/Un-check all reports",
                                        variable=self.all_viz, command=self._all_viz_func,
                                        wraplength=100)

        self.rg_draw = tk.BooleanVar(self)
        self.rg_draw.set('False')
        rg_draw_enable = tk.Checkbutton(self, text="Routing Graph", variable=self.rg_draw)

        self.shm_draw = tk.BooleanVar(self)
        self.shm_draw.set('False')
        shm_draw_enable = tk.Checkbutton(self, text="System Health Map", variable=self.shm_draw)

        self.mapping_Draw = tk.BooleanVar(self)
        self.mapping_Draw.set('False')
        mapping_draw_enable = tk.Checkbutton(self, text="Mapping Report", variable=self.mapping_Draw)

        self.pmcg_draw = tk.BooleanVar(self)
        self.pmcg_draw.set('False')
        pmcg_draw_enable = tk.Checkbutton(self, text="PMCG Report", variable=self.pmcg_draw)

        self.ttg_draw = tk.BooleanVar(self)
        self.ttg_draw.set('False')
        ttg_draw_enable = tk.Checkbutton(self, text="TTG Report", variable=self.ttg_draw)

        label = tk.Label(self, text="Visualization Config", font="-weight bold")
        label.grid(column=self.viz_starting_col, row=self.viz_starting_row, columnspan=2)
        all_viz_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+1, columnspan=1, sticky='w')

        shm_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+2, sticky='W')
        rg_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+3, sticky='W')
        mapping_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+4, sticky='W')
        pmcg_draw_enable.grid(column=self.viz_starting_col+1, row=self.viz_starting_row+3, sticky='W')
        ttg_draw_enable.grid(column=self.viz_starting_col+1, row=self.viz_starting_row+4, sticky='W')
        ttk.Separator(self, orient='vertical').grid(column=self.viz_starting_col+3,
                                                    row=self.viz_starting_row+1, rowspan=4, sticky="ns")

        # ---------------------------------------------
        #               Anim
        # ---------------------------------------------
        self.anim_enable = tk.BooleanVar(self)
        self.anim_enable.set('False')
        self.anim_enableBox = tk.Checkbutton(self, text="Generate Animation Frames",
                                             variable=self.anim_enable, command=self._animation_config)

        self.frame_rez_label = tk.Label(self, text="Frame Resolution(dpi):")
        self.frame_rez = tk.Entry(self, width=self.entry_width)
        self.frame_rez.insert(0, '20')

        tk.Label(self, text="Animation Frames Config", font="-weight bold").grid(column=self.anim_starting_col,
                                                                                 row=self.anim_starting_row,
                                                                                 columnspan=2)

        self.anim_enableBox.grid(column=self.anim_starting_col, row=self.anim_starting_row+1,
                                 sticky='W')

    def _animation_config(self):
        if self.anim_enable.get() is True:
            self.frame_rez_label.grid(column=self.anim_starting_col, row=self.anim_starting_row+2)
            self.frame_rez.grid(column=self.anim_starting_col+1, row=self.anim_starting_row+2)
        else:
            self.frame_rez.grid_forget()
            self.frame_rez_label.grid_forget()

    def _all_viz_func(self):
        if self.all_viz.get():
            self.pmcg_draw.set(True)
            self.mapping_Draw.set(True)
            self.rg_draw.set(True)
            self.shm_draw.set(True)
            self.ttg_draw.set(True)
        else:
            self.pmcg_draw.set(False)
            self.mapping_Draw.set(False)
            self.rg_draw.set(False)
            self.shm_draw.set(False)
            self.ttg_draw.set(False)