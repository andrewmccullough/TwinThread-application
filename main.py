import ssl
import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import json
import urllib.request

try:
	source = urllib.request.urlopen("https://www.twinthread.com/code-challenge/assets.txt", context = ssl._create_unverified_context())
	# source = open("assets.txt")
	db = json.load(source)
	source.close()

	classes = {}
	for each in db["assets"]:
		if "classList" in each.keys():
			if len(each["classList"]) > 0:
				for asset_class in each["classList"]:
					asset_class_id = asset_class["id"]
					if asset_class_id in classes.keys():
						classes[asset_class_id]["assets"].append(each)
					else:
						classes[asset_class_id] = {
							"name": asset_class["name"],
							"drill": asset_class["drill"],
							"id": asset_class_id,
							"assets": [each]
						}

	window = tk.Tk()
	window.minsize(250, 0)
	window.title("Home")

	# layer 3
	def asset_page(asset, origin, origin_details = None, original_origin = None):

		def open_class():
			selected = listbox.curselection()
			if selected:
				class_id = asset["classList"][selected[0]]["id"]
				class_page(class_id, origin = "asset", origin_details = asset_id, original_origin = original_origin)

		def return_to_layer_2_search_results():
			if origin_details:
				layer_2_search_results(origin_details)
			else:
				layer_1_search()

		def return_to_class_page():
			if origin_details:
				class_page(origin_details, "classes")
			else:
				layer_1_classes()

		def return_to_layer_2_critical_items():
			layer_1_critical()

		if not asset:
			return
		if isinstance(asset, int):
			asset_id = asset
			for obj in db["assets"]:
				if obj["assetId"] == asset_id:
					asset = obj
					break
		else:
			asset_id = asset["assetId"]

		for child in list(window.children.values()):
			child.destroy()

		layer_3 = tk.Frame(window)
		layer_3.pack()

		asset_detail_page = tk.Frame(layer_3)
		asset_detail_page.pack()
		window.title("Asset #" + str(asset_id))

		if origin == "search":
			tk.Button(asset_detail_page, text = "Back to search results", command = return_to_layer_2_search_results).pack()
		elif origin == "critical":
			tk.Button(asset_detail_page, text = "Back to critical items", command = return_to_layer_2_critical_items).pack()
		elif origin == "class":
			if origin_details:
				tk.Button(asset_detail_page, text = "Back to " + classes[origin_details]["name"] + " details", command = return_to_class_page).pack()
			else:
				tk.Button(asset_detail_page, text = "Back to classes", command = return_to_class_page).pack()
		else:
			tk.Button(asset_detail_page, text = "Go home", command = layer_0_home).pack()

		if "name" in asset.keys():
			tk.Label(asset_detail_page, text = "name: " + asset["name"]).pack()
		else:
			tk.Label(asset_detail_page, text = "(unnamed)").pack()

		tk.Label(asset_detail_page, text = "ID: " + str(asset_id)).pack()

		if "description" in asset.keys():
			tk.Label(asset_detail_page, text = "description:\n" + asset["description"]).pack()
		else:
			tk.Label(asset_detail_page, text = "description:\nnone").pack()

		if "classList" in asset.keys():
			tk.Label(asset_detail_page, text = "classes of this asset:").pack()
			if len(asset["classList"]) > 0:
				listbox = tk.Listbox(asset_detail_page, selectmode = tk.BROWSE, width = 40)
				listbox.pack()
				listbox.bind('<Double-1>', lambda x: open_class())
				for i, class_obj in enumerate(asset["classList"]):
					listbox.insert(i, class_obj["name"])
			else:
				tk.Label(asset_detail_page, text = "None").pack()
		else:
			tk.Label(asset_detail_page, text = "None").pack()

		tk.Label(asset_detail_page, text = "raw data about this asset:").pack()
		detail = ScrolledText(asset_detail_page)
		detail.pack()
		for attr, data in asset.items():
			if isinstance(data, dict):
				detail.insert(tk.INSERT, str(attr) + "\n")
				for key, val in data.items():
					detail.insert(tk.INSERT, (str(key) + ": " + str(val)) + "\n")
			elif isinstance(data, list):
				detail.insert(tk.INSERT, str(attr) + "\n")
				for val in data:
					detail.insert(tk.INSERT, str(val) + "\n")
			else:
				detail.insert(tk.INSERT, str(attr) + ": " + str(data) + "\n")

		detail.configure(state = "disabled")


	def class_page(class_id, origin, origin_details = None, original_origin = None):
		def return_to_asset_page():
			if origin_details:
				if original_origin:
					asset_page(origin_details, origin = original_origin, original_origin = original_origin)
				else:
					asset_page(origin_details, origin = "home")
			else:
				layer_1_classes()

		def open_asset():
			selected = listbox.curselection()
			if selected:
				asset = class_obj["assets"][selected[0]]
				asset_page(asset, "class", origin_details = class_id, original_origin = original_origin)

		if not class_id:
			return
		else:
			class_obj = classes[class_id]

		for child in list(window.children.values()):
			child.destroy()

		layer_3 = tk.Frame(window)
		layer_3.pack()

		class_detail_page = tk.Frame(layer_3)
		class_detail_page.pack()
		window.title("class " + class_obj["name"])

		if origin == "asset" and origin_details:
			tk.Button(class_detail_page, text = "Back to asset #" + str(origin_details), command = return_to_asset_page).pack()
		elif origin == "classes":
			tk.Button(class_detail_page, text = "Back to class list", command = layer_1_classes).pack()
		else:
			tk.Button(class_detail_page, text = "Go home", command = layer_0_home).pack()

		tk.Label(class_detail_page, text = "name: " + class_obj["name"]).pack()   # TODO : bold
		tk.Label(class_detail_page, text = "ID: " + str(class_id)).pack()
		tk.Label(class_detail_page, text = "drill: " + class_obj["drill"]).pack()
		tk.Label(class_detail_page, text = "assets in this class:").pack()

		listbox = tk.Listbox(class_detail_page, selectmode = tk.BROWSE, width = 40)
		listbox.pack()
		listbox.bind('<Double-1>', lambda x: open_asset())
		for i, asset in enumerate(class_obj["assets"]):
			listbox.insert(i, asset["name"])


	# layer 2
	def layer_2_search_results(query):

		def return_to_layer_1_search():
			layer_1_search(query)

		def open_asset():
			selected = listbox.curselection()
			if selected:
				asset = results[selected[0]]
				asset_page(asset, origin = "search", origin_details = query, original_origin = "search")

		for child in list(window.children.values()):
			child.destroy()

		layer_2 = tk.Frame(window)
		layer_2.pack()

		search_results_page = tk.Frame(layer_2)
		search_results_page.pack()
		window.title("Search results for " + query)

		tk.Button(search_results_page, text = "Back to search", command = return_to_layer_1_search).pack()

		results = []
		for asset in db["assets"]:
			if query.lower() in asset["name"].lower() or query in asset["description"].lower() or query in str(asset["assetId"]):
				results.append(asset)

		listbox = tk.Listbox(search_results_page, selectmode = tk.BROWSE, width = 40)
		listbox.pack()
		listbox.bind('<Double-1>', lambda x: open_asset())
		for i, res in enumerate(results):
			listbox.insert(i, res["name"])


	# layer 1
	def layer_1_search(autofill = None):

		def retrieve_query():
			query = bar.get().strip()
			if query:
				layer_2_search_results(query)

		for child in list(window.children.values()):
			child.destroy()

		layer_1 = tk.Frame(window)
		layer_1.pack()

		search_page = tk.Frame(layer_1)
		search_page.pack()
		window.title("Search")

		tk.Button(search_page, text = "Back to home", command = layer_0_home).pack()

		frame = tk.Frame(search_page)
		frame.pack()
		bar = tk.Entry(frame)
		bar.pack(side = tk.LEFT)
		tk.Button(frame, text = "Search", command = retrieve_query).pack(side = tk.LEFT)

		if autofill:
			bar.insert(tk.INSERT, autofill)


	def layer_1_critical():
		def open_asset():
			selected = listbox.curselection()
			if selected:
				asset = results[selected[0]]
				asset_page(asset, origin = "critical", original_origin = "critical")

		for child in list(window.children.values()):
			child.destroy()

		layer_1 = tk.Frame(window)
		layer_1.pack()

		critical_page = tk.Frame(layer_1)
		critical_page.pack()
		window.title("Critical items")

		tk.Button(critical_page, text = "Back to home", command = layer_0_home).pack()

		results = []
		for each in db["assets"]:
			if each["status"] == 3:
				results.append(each)

		listbox = tk.Listbox(critical_page, selectmode = tk.BROWSE, width = 40)
		listbox.pack()
		listbox.bind('<Double-1>', lambda x: open_asset())
		for i, each in enumerate(results):
			listbox.insert(i, each["name"])


	def layer_1_classes():
		def open_class():
			selected = listbox.curselection()
			if selected:
				class_id = list(classes.keys())[selected[0]]
				class_page(class_id, origin = "classes", original_origin = "classes")

		for child in list(window.children.values()):
			child.destroy()

		layer_1 = tk.Frame(window)
		layer_1.pack()

		classes_page = tk.Frame(layer_1)
		classes_page.pack()
		window.title("Classes")

		tk.Button(classes_page, text = "Back to home", command = layer_0_home).pack()
		tk.Label(classes_page, text = str(len(classes)) + " classes").pack()

		listbox = tk.Listbox(classes_page, selectmode = tk.BROWSE, width = 40)
		listbox.pack()
		listbox.bind('<Double-1>', lambda x: open_class())
		for i, each in enumerate(classes.values()):
			listbox.insert(i, each["name"])

	# layer 0
	def layer_0_home():
		for child in list(window.children.values()):
			child.destroy()

		layer_0 = tk.Frame(window)
		layer_0.pack()

		home_page = tk.Frame(layer_0)
		home_page.pack()
		window.title("Home")

		# tk.Label(home_page, text = "Home", underline = 1, font = ('bold')).pack()                      # TODO: bold font
		tk.Button(home_page, text = "Search", command = layer_1_search).pack()
		tk.Button(home_page, text = "Critical items", command = layer_1_critical).pack()
		tk.Button(home_page, text = "View classes", command = layer_1_classes).pack()


	layer_0_home()
	window.mainloop()
except KeyboardInterrupt:
	sys.exit()
