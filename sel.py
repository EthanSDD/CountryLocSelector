from collections import OrderedDict
from json import dump, load
from tkinter import BOTH, messagebox, Radiobutton
from PIL import Image, ImageTk
import tkinter as tk

import pycountry_convert as pc
from customtkinter import (
    CTk,
    CTkFrame,
    CTkImage,
    CTkInputDialog,
    CTkLabel,
    CTkRadioButton,
    IntVar,
)
from PIL import Image
from pywinstyles import set_opacity

MAPPING_PRECISION = 3

root = CTk()
root.geometry("1000x600")
#root.attributes("-fullscreen", True)


def get_country_mappings():
    try:
        with open("country_mappings.json") as f:
            return OrderedDict(
                sorted(
                    load(f).items(),
                    key=lambda entry: entry[1]["identifier"],
                )
            )
    except:
        with open("country_mappings.json", "w") as f:
            dump({}, f, indent=3)
            return OrderedDict({})


def write_country_mappings(data):
    with open("country_mappings.json", "w") as f:
        return dump(data, f, indent=3)


def get_continent(country):
    alpha2 = pc.country_name_to_country_alpha2(country)
    continent_code = pc.country_alpha2_to_continent_code(alpha2)
    continent = pc.convert_continent_code_to_continent_name(continent_code)
    return continent

def on_click(e):
    dialog = CTkInputDialog(
        text="Enter a country: ", title="Map Country Coordinates"
    )
    country = dialog.get_input()
    try:
        continent = get_continent(country)
    except Exception as ex:
        return messagebox.showerror(message=f"{type(ex).__name__}: {ex}")

    relx = round(e.x / root.winfo_screenwidth() - 0.09, MAPPING_PRECISION)
    rely = round(e.y / root.winfo_screenheight() - 0.325, MAPPING_PRECISION)

    append_country_mapping(
        get_country_mappings(),
        relx,
        rely,
        continent.casefold(),
        country.casefold(),
    )


def append_country_mapping(mappings, relx, rely, continent, country):
    if country in mappings:
        return messagebox.showerror(message="Country already in mappings")

    if len(mappings) != 0:
        last_identifier = int(
            mappings.copy().popitem(last=True)[1]["identifier"]
        )
    else:
        last_identifier = 0

    mappings[country] = {
        "identifier": last_identifier + 1,
        "continent": continent,
        "relCoords": [relx, rely],
    }
    write_country_mappings(mappings)


def on_selector_click(event, button, country):
    print(f"You clicked {country}")


container = CTkFrame(root)
image_original = Image.open("Europe.png").resize((1500, 1125))
image_tk = ImageTk.PhotoImage(image_original)
image = tk.Label(container, text="", image=image_tk)
image.place(relx=0.5, rely=0.5, anchor="c")
container.pack(expand=True, fill=BOTH)
image.bind("<Button-1>", lambda e: on_click(e))

selectors = []
data = get_country_mappings()
selected_button = IntVar()
for entry in data.items():
    country = entry[0]
    button_container = CTkFrame(root, width=25, height=25)
    button = CTkRadioButton(
        button_container,
        text="",
        variable=selected_button,
        value=entry[1]["identifier"],
        width=20,
        height=20,
        radiobutton_height=20,
        radiobutton_width=20,
        corner_radius=0,
    )
    button.place(relx=0.62, rely=0.499, anchor="c")
    coords = entry[1]["relCoords"]
    button.bind("<Button-1>", lambda e, b=button, c=country: on_selector_click(e, b, c))
    button_container.place(relx=coords[0], rely=coords[1], anchor="c")
    
    selectors.append(button)

root.mainloop()