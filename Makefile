all_data.csv:
	./proc_table.py > $@
	./proc_list.py >> $@
	./proc_2001.py >> $@
	./proc_text.py >> $@
