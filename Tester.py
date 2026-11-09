"""Visual live-input tester for DualShock 4 and Xbox-compatible controllers."""

import tkinter as tk
from tkinter import ttk

try:
	import pygame
except ImportError:
	pygame = None


BG, CARD, TEXT, MUTED = "#10151d", "#1c2734", "#e8eef5", "#91a1b3"
GREEN, BLUE, DIM = "#49d6a5", "#63a9ff", "#465465"


class Tester:
	def __init__(self, root):
		self.root = root
		self.root.title("Controller Tester")
		self.root.geometry("900x660")
		self.root.minsize(720, 560)
		self.root.configure(bg=BG)
		self.joystick = None
		self.devices = []
		self.indicators = []
		self._ui()
		if pygame:
			pygame.init()
			pygame.joystick.init()
			self.refresh()
		else:
			self.device.set("pygame is not installed")
			self.status.config(text="● INPUT UNAVAILABLE", fg="#ffb454")
		self.update()

	def _ui(self):
		style = ttk.Style()
		style.theme_use("clam")
		style.configure("TCombobox", fieldbackground=CARD, background=CARD,
						foreground=TEXT, arrowcolor=TEXT)
		style.configure("Horizontal.TProgressbar", troughcolor=BG,
						background=GREEN, bordercolor=BG)

		top = tk.Frame(self.root, bg=BG)
		top.pack(fill="x", padx=24, pady=(20, 12))
		tk.Label(top, text="CONTROLLER TESTER", bg=BG, fg=TEXT,
				 font=("Segoe UI", 21, "bold")).pack(side="left")
		self.status = tk.Label(top, text="● NO CONTROLLER", bg=BG, fg="#ffb454",
							   font=("Segoe UI", 9, "bold"))
		self.status.pack(side="right", pady=9)

		bar = tk.Frame(self.root, bg=CARD, padx=14, pady=12)
		bar.pack(fill="x", padx=24)
		tk.Label(bar, text="DEVICE", bg=CARD, fg=MUTED,
				 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))
		self.device = tk.StringVar(value="Connect a controller")
		self.selector = ttk.Combobox(bar, textvariable=self.device, state="readonly")
		self.selector.pack(side="left", fill="x", expand=True)
		self.selector.bind("<<ComboboxSelected>>", self.select)
		tk.Button(bar, text="REFRESH", command=self.refresh, bg="#2a3949", fg=TEXT,
				  activebackground="#35495e", activeforeground=TEXT, relief="flat",
				  padx=14, pady=7, cursor="hand2").pack(side="right", padx=(10, 0))
		self.details = tk.Label(self.root, text="Connect a controller and press a button.",
								bg=BG, fg=MUTED, anchor="w", font=("Segoe UI", 10))
		self.details.pack(fill="x", padx=24, pady=12)

		body = tk.Frame(self.root, bg=BG)
		body.pack(fill="both", expand=True, padx=24, pady=(0, 16))
		left = tk.Frame(body, bg=BG)
		left.pack(side="left", fill="both", expand=True, padx=(0, 12))
		right = tk.Frame(body, bg=BG)
		right.pack(side="right", fill="both", expand=True, padx=(12, 0))

		self._heading(left, "STICK POSITION")
		box = tk.Frame(left, bg=CARD, padx=12, pady=12)
		box.pack(fill="both", expand=True)
		self.canvas = tk.Canvas(box, bg=CARD, height=230, highlightthickness=0)
		self.canvas.pack(fill="both", expand=True)
		self.canvas.bind("<Configure>", lambda _e: self.draw_sticks())

		self._heading(left, "TRIGGERS")
		trigger_box = tk.Frame(left, bg=CARD, padx=14, pady=12)
		trigger_box.pack(fill="x")
		self.trigger_widgets = {}
		for label, axis in (("LT", 4), ("RT", 5)):
			row = tk.Frame(trigger_box, bg=CARD)
			row.pack(fill="x", pady=5)
			tk.Label(row, text=label, width=4, anchor="w", bg=CARD, fg=TEXT,
					 font=("Segoe UI", 9, "bold")).pack(side="left")
			progress = ttk.Progressbar(row, maximum=100)
			progress.pack(side="left", fill="x", expand=True, padx=8)
			value = tk.Label(row, text="0%", width=5, bg=CARD, fg=MUTED)
			value.pack(side="right")
			self.trigger_widgets[axis] = (progress, value)

		self._heading(right, "BUTTONS")
		button_box = tk.Frame(right, bg=CARD, padx=10, pady=10)
		button_box.pack(fill="both", expand=True)
		names = ["A / Cross", "B / Circle", "X / Square", "Y / Triangle",
				 "LB / L1", "RB / R1", "Back / Share", "Start / Options",
				 "L3", "R3", "Guide / PS", "Touchpad"]
		for i, name in enumerate(names):
			row, col = divmod(i, 2)
			cell = tk.Frame(button_box, bg="#253241", padx=8, pady=9)
			cell.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
			tk.Label(cell, text=name, bg="#253241", fg=MUTED,
					 font=("Segoe UI", 9)).pack(side="left")
			dot = tk.Label(cell, text="●", bg="#253241", fg=DIM,
						   font=("Segoe UI", 12, "bold"))
			dot.pack(side="right")
			self.indicators.append(dot)
		button_box.columnconfigure(0, weight=1)
		button_box.columnconfigure(1, weight=1)

		self._heading(right, "D-PAD")
		dpad = tk.Frame(right, bg=CARD, padx=10, pady=10)
		dpad.pack(fill="x")
		self.dpad = tk.Label(dpad, text="—", bg=CARD, fg=TEXT,
							 font=("Segoe UI", 11, "bold"))
		self.dpad.pack()
		tk.Label(self.root, text="Live input • Stick values normalized", bg=BG,
				 fg="#667789", font=("Segoe UI", 9)).pack(anchor="w", padx=24, pady=(0, 12))

	@staticmethod
	def _heading(parent, text):
		tk.Label(parent, text=text, bg=BG, fg=MUTED,
				 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(12, 7))

	def refresh(self):
		if pygame is None:
			return
		try:
			pygame.event.pump()
			pygame.joystick.quit()
			pygame.joystick.init()
			self.devices = [pygame.joystick.Joystick(i)
							for i in range(pygame.joystick.get_count())]
			labels = [f"{i + 1}. {joy.get_name()}" for i, joy in enumerate(self.devices)]
			self.selector.configure(values=labels, state="readonly" if labels else "disabled")
			if labels:
				self.selector.current(0)
				self.select()
			else:
				self.joystick = None
				self.device.set("No controller detected")
				self.status.config(text="● NO CONTROLLER", fg="#ffb454")
				self.details.config(text="Connect a controller, then select REFRESH.")
		except pygame.error as exc:
			self.details.config(text=f"Controller scan failed: {exc}")

	def select(self, _event=None):
		index = self.selector.current()
		if index < 0 or index >= len(self.devices):
			return
		try:
			self.joystick = self.devices[index]
			if not self.joystick.get_init():
				self.joystick.init()
			self.status.config(text="● CONNECTED", fg=GREEN)
			self.details.config(text=f"{self.joystick.get_name()}  •  "
									 f"{self.joystick.get_numaxes()} axes  •  "
									 f"{self.joystick.get_numbuttons()} buttons")
		except pygame.error as exc:
			self.joystick = None
			self.details.config(text=f"Could not open controller: {exc}")

	def update(self):
		if pygame and self.joystick:
			try:
				pygame.event.pump()
				self.read_input()
			except pygame.error:
				self.joystick = None
				self.status.config(text="● DISCONNECTED", fg="#ffb454")
				self.details.config(text="Controller disconnected. Select REFRESH to reconnect.")
		self.root.after(16, self.update)

	def read_input(self):
		joy = self.joystick
		axes = [joy.get_axis(i) for i in range(joy.get_numaxes())]
		self.draw_sticks(axes)
		# XInput commonly reports triggers on axes 4/5; layouts differ by device.
		for axis, (bar, value) in self.trigger_widgets.items():
			amount = max(0, min(100, (axes[axis] + 1) * 50)) if axis < len(axes) else 0
			bar.configure(value=amount)
			value.config(text=f"{round(amount)}%")

		xbox = any(word in joy.get_name().lower() for word in ("xbox", "xinput"))
		mapping = list(range(12)) if xbox else [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13]
		for i, dot in enumerate(self.indicators):
			pressed = mapping[i] < joy.get_numbuttons() and joy.get_button(mapping[i])
			dot.config(fg=GREEN if pressed else DIM)

		if joy.get_numhats():
			x, y = joy.get_hat(0)
			directions = (["UP"] if y > 0 else []) + (["DOWN"] if y < 0 else [])
			directions += (["LEFT"] if x < 0 else []) + (["RIGHT"] if x > 0 else [])
			self.dpad.config(text="  +  ".join(directions) if directions else "—",
							 fg=BLUE if directions else TEXT)
		else:
			self.dpad.config(text="Not reported by device", fg=MUTED)

	def draw_sticks(self, axes=None):
		axes = axes if axes is not None else [0.0] * 4
		if axes is None:
			axes = []
		canvas = self.canvas
		canvas.delete("all")
		width, height = max(canvas.winfo_width(), 240), max(canvas.winfo_height(), 180)
		radius = min(width * .17, height * .32, 72)
		for cx, label, offset, color in ((width * .27, "LEFT STICK", 0, GREEN),
										 (width * .73, "RIGHT STICK", 2, BLUE)):
			cy = height * .52
			canvas.create_text(cx, 16, text=label, fill=MUTED,
							   font=("Segoe UI", 9, "bold"))
			canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
							   outline="#405064", width=2)
			canvas.create_line(cx-radius, cy, cx+radius, cy, fill="#2a3949")
			canvas.create_line(cx, cy-radius, cx, cy+radius, fill="#2a3949")
			x = axes[offset] if len(axes) > offset else 0.0
			y = axes[offset + 1] if len(axes) > offset + 1 else 0.0
			px, py = cx + x * radius, cy + y * radius
			canvas.create_oval(px-8, py-8, px+8, py+8, fill=color, outline="")
			canvas.create_text(cx, cy+radius+17, text=f"X {x:+.2f}   Y {-y:+.2f}",
							   fill=TEXT, font=("Consolas", 9))


if __name__ == "__main__":
	root = tk.Tk()
	Tester(root)
	root.mainloop()
