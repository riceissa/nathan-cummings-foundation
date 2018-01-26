all_data.csv:
	./proc_table.py > $@
	./proc_list.py >> $@
	./proc_text.py >> $@
